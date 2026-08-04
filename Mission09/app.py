import streamlit as st
import cv2
import pandas as pd
import numpy as np
import tempfile
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import google.generativeai as genai
from ultralytics import YOLO
from tracking_utils import map_pixels_to_pitch

# Application Setup
st.set_page_config(page_title="Soccer Vision Lab", page_icon="⚽", layout="wide")
st.title("⚽ Soccer Vision Lab: AI Tactical Analyst")
st.write("Upload match footage to track player movement, draw professional heatmaps, and generate UEFA Pro tactical insights.")

# Sidebar configuration
st.sidebar.header("⚙️ Tracking Settings")
target_player_id = st.sidebar.number_input("Target Player Track ID", min_value=1, value=1, step=1)

# Configure Gemini AI
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ai_model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    st.sidebar.warning("⚠️ GEMINI_API_KEY missing in st.secrets. AI Report disabled.")
    ai_model = None

uploaded_file = st.file_uploader("Upload Match Video Clip (.mp4, .mov)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    st.info("📹 Video loaded. Processing frames with YOLO Tracker...")
    
    cap = cv2.VideoCapture(tfile.name)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    yolo_model = YOLO('yolov8n.pt')
    tracking_records = []
    frame_idx = 0
    progress_bar = st.progress(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx >= 150: # Limit processing frame window for fast demo response
            break
            
        frame_idx += 1
        if total_frames > 0:
            progress_bar.progress(min(frame_idx / min(total_frames, 150), 1.0))
            
        results = yolo_model.track(frame, persist=True, verbose=False)[0]
        
        if results.boxes is not None and results.boxes.id is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            track_ids = results.boxes.id.cpu().numpy()
            clss = results.boxes.cls.cpu().numpy()
            
            for box, track_id, cls in zip(boxes, track_ids, clss):
                # Class index 0 corresponds to 'person'
                if int(cls) == 0 and int(track_id) == target_player_id:
                    x1, y1, x2, y2 = box
                    center_x = (x1 + x2) / 2.0
                    center_y = y2 # Base feet position for spatial mapping
                    
                    pitch_x, pitch_y = map_pixels_to_pitch(
                        center_x, center_y, frame_width, frame_height
                    )
                    
                    tracking_records.append({
                        "frame": frame_idx,
                        "pitch_x": pitch_x,
                        "pitch_y": pitch_y
                    })
    
    cap.release()
    st.success("✅ Processing completed successfully!")
    
    if tracking_records:
        df_tracking = pd.DataFrame(tracking_records)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📍 Tactical Heatmap")
            pitch = Pitch(pitch_type='statsbomb', pitch_color='#aabb97', line_color='white')
            fig, ax = pitch.draw(figsize=(8, 5))
            bin_statistic = pitch.bin_statistic(
                df_tracking['pitch_x'], df_tracking['pitch_y'], statistic='count', bins=(12, 8)
            )
            pitch.heatmap(bin_statistic, ax=ax, cmap='Reds', alpha=0.6)
            pitch.scatter(df_tracking['pitch_x'], df_tracking['pitch_y'], c='black', s=25, ax=ax)
            st.pyplot(fig)
            
        with col2:
            st.subheader("📋 Trajectory Summary")
            avg_x = df_tracking['pitch_x'].mean()
            avg_y = df_tracking['pitch_y'].mean()
            st.metric("Avg Position X (Length)", f"{avg_x:.1f} yds")
            st.metric("Avg Position Y (Width)", f"{avg_y:.1f} yds")
            st.metric("Logged Detections", f"{len(df_tracking)} frames")
            
        st.divider()
        st.subheader("🤖 UEFA Pro AI Tactical Assessment")
        
        if ai_model and st.button("Generate AI Report"):
            prompt = f"""
            You are an elite UEFA Pro soccer analyst.
            
            Review this positional tracking log for Player Track ID #{target_player_id}:
            - Average Pitch Length (X, 0-120 yds): {avg_x:.1f}
            - Average Pitch Width (Y, 0-80 yds): {avg_y:.1f}
            - Tracking Frame Sample Count: {len(df_tracking)}
            - Range X: {df_tracking['pitch_x'].min():.1f} to {df_tracking['pitch_x'].max():.1f}
            - Range Y: {df_tracking['pitch_y'].min():.1f} to {df_tracking['pitch_y'].max():.1f}
            
            Provide a structured, professional tactical assessment containing:
            1. Key Positional Strengths
            2. Tactical Weaknesses / Structural Flaws
            3. Direct Coaching Advice for future matches
            4. World-Class Player Comparison
            """
            with st.spinner("Generating AI Tactical Report..."):
                response = ai_model.generate_content(prompt)
                st.markdown(response.text)
    else:
        st.warning(f"No tracking records found for Target Player Track ID #{target_player_id}. Try changing the ID in the sidebar.")
