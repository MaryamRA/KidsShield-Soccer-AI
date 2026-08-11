# ============================================================
# ⚽ MISSION 13
# Artin FC AI Player Tracking Center
# ============================================================
#
# Mission 13 pipeline:
#
# Video
#   ↓
# YOLO Player Detection
#   ↓
# ByteTrack
#   ↓
# Find Tracking IDs
#   ↓
# Select Artin
#   ↓
# Track Artin
#   ↓
# Feet Position
#   ↓
# Pitch Coordinates
#   ↓
# Distance
#   ↓
# Estimated Speed
#   ↓
# Tactical Zones
#   ↓
# Movement Trajectory
#   ↓
# Heatmap
#   ↓
# CSV
#
# IMPORTANT:
# Pitch coordinates and speed are educational estimates.
# Accurate physical measurements require camera calibration
# / perspective transformation (homography).
# ============================================================


# ============================================================
# PHASE 1 — IMPORT LIBRARIES
# ============================================================

import cv2
import math
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import tempfile

from ultralytics import YOLO
from mplsoccer import Pitch


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Artin FC AI Tracking Center",
    page_icon="⚽",
    layout="wide"
)


st.title("⚽ Artin FC AI Tracking Center")

st.write(
    "Track a soccer player and analyze their movement."
)

st.info(
    "Mission 13 uses YOLO + ByteTrack to follow a selected "
    "player through a soccer video."
)


# ============================================================
# PHASE 2 — PLAYER INFORMATION
# ============================================================

st.header("👤 Player Information")


player_name = st.text_input(
    "Player Name",
    value="Artin"
)


position = st.selectbox(
    "Player Position",
    [
        "Forward",
        "Midfielder",
        "Defender",
        "Winger"
    ]
)


# ============================================================
# PHASE 3 — UPLOAD VIDEO
# ============================================================

st.header("🎥 Upload Soccer Video")


uploaded_video = st.file_uploader(
    "Choose a soccer video",
    type=["mp4", "mov", "avi"]
)


if uploaded_video is None:

    st.warning(
        "Please upload a soccer video to begin."
    )

    st.stop()


# ============================================================
# SAVE UPLOADED VIDEO
# ============================================================

temp_file = tempfile.NamedTemporaryFile(
    delete=False,
    suffix=".mp4"
)


temp_file.write(
    uploaded_video.getbuffer()
)


temp_file.close()


video_path = temp_file.name


# ============================================================
# VIDEO PREVIEW
# ============================================================

st.subheader("🎬 Video Preview")

st.video(uploaded_video)


# ============================================================
# PHASE 4 — INSPECT VIDEO
# ============================================================

cap = cv2.VideoCapture(
    video_path
)


if not cap.isOpened():

    st.error(
        "Could not open the uploaded video."
    )

    st.stop()


fps = cap.get(
    cv2.CAP_PROP_FPS
)


width = int(
    cap.get(
        cv2.CAP_PROP_FRAME_WIDTH
    )
)


height = int(
    cap.get(
        cv2.CAP_PROP_FRAME_HEIGHT
    )
)


total_frames = int(
    cap.get(
        cv2.CAP_PROP_FRAME_COUNT
    )
)


cap.release()


if fps <= 0:

    st.error(
        "The video FPS could not be read."
    )

    st.stop()


duration = total_frames / fps


st.subheader("📹 Video Information")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Frames",
    total_frames
)


col2.metric(
    "FPS",
    round(fps, 1)
)


col3.metric(
    "Resolution",
    f"{width} × {height}"
)


col4.metric(
    "Duration",
    f"{duration:.1f} sec"
)


# ============================================================
# PHASE 5 — LOAD YOLO
# ============================================================

st.header("🤖 Find Player Tracking IDs")


st.write(
    """
YOLO does not know which player is Artin.

ByteTrack gives detected players numerical tracking IDs.

First we will inspect the beginning of the video and
display the IDs on the players.
"""
)


# Fresh YOLO model
model = YOLO(
    "yolov8n.pt"
)


# ============================================================
# FIND TRACKING IDs
# ============================================================

find_ids_button = st.button(
    "🔎 Find Players and Tracking IDs"
)


if find_ids_button:

    # --------------------------------------------------------
    # Fresh video
    # --------------------------------------------------------

    cap = cv2.VideoCapture(
        video_path
    )


    if not cap.isOpened():

        st.error(
            "Could not open the video."
        )

        st.stop()


    # --------------------------------------------------------
    # Fresh model = fresh tracker
    # --------------------------------------------------------

    model = YOLO(
        "yolov8n.pt"
    )


    frame_number = 0

    detected_ids = set()

    first_frame = None

    first_frame_result = None


    # --------------------------------------------------------
    # Inspect first 100 frames
    # --------------------------------------------------------

    frames_to_check = min(
        100,
        total_frames
    )


    while frame_number < frames_to_check:

        ret, frame = cap.read()


        if not ret:

            break


        frame_number += 1


        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            verbose=False
        )


        result = results[0]


        # ----------------------------------------------------
        # Save the first frame that contains tracking IDs
        # ----------------------------------------------------

        if (
            first_frame is None
            and
            result.boxes.id is not None
        ):

            first_frame = frame.copy()

            first_frame_result = result


        # ----------------------------------------------------
        # Collect IDs
        # ----------------------------------------------------

        if result.boxes.id is not None:

            ids = (
                result.boxes.id
                .cpu()
                .tolist()
            )


            for player_id in ids:

                detected_ids.add(
                    int(player_id)
                )


    cap.release()


    detected_ids = sorted(
        detected_ids
    )


    # --------------------------------------------------------
    # Store detected IDs in session state
    # --------------------------------------------------------

    st.session_state[
        "detected_ids"
    ] = detected_ids


    # --------------------------------------------------------
    # Display IDs
    # --------------------------------------------------------

    if first_frame is not None:

        display_frame = first_frame.copy()


        boxes = (
            first_frame_result
            .boxes
            .xyxy
            .cpu()
            .tolist()
        )


        ids = (
            first_frame_result
            .boxes
            .id
            .cpu()
            .tolist()
        )


        # ----------------------------------------------------
        # Draw every player and tracking ID
        # ----------------------------------------------------

        for box, player_id in zip(
            boxes,
            ids
        ):

            player_id = int(
                player_id
            )


            x1, y1, x2, y2 = map(
                int,
                box
            )


            # Bounding box
            cv2.rectangle(
                display_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # Tracking ID
            label = (
                f"Player ID: {player_id}"
            )


            cv2.putText(
                display_frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )


        st.subheader(
            "👀 Identify Artin"
        )


        st.write(
            "Look at the frame below and identify "
            "which Tracking ID belongs to Artin."
        )


        # Convert BGR → RGB
        display_frame = cv2.cvtColor(
            display_frame,
            cv2.COLOR_BGR2RGB
        )


        st.image(
            display_frame,
            caption="Detected Players and Tracking IDs",
            use_container_width=True
        )


    # --------------------------------------------------------
    # Show IDs
    # --------------------------------------------------------

    st.write(
        "Tracking IDs found:"
    )


    st.write(
        detected_ids
    )


    if not detected_ids:

        st.error(
            "No players were detected."
        )

    else:

        st.success(
            "Players detected successfully. "
            "Select Artin's ID below."
        )


# ============================================================
# PHASE 6 — SELECT ARTIN'S TRACKING ID
# ============================================================

if "detected_ids" in st.session_state:

    detected_ids = st.session_state[
        "detected_ids"
    ]


    if len(detected_ids) > 0:

        st.header(
            "🎯 Select Artin's Tracking ID"
        )


        st.write(
            """
Choose the number that appears on Artin
in the player-identification image above.
"""
        )


        artin_id = st.selectbox(
            "Artin's Tracking ID",
            detected_ids
        )


        st.success(
            f"{player_name} is assigned Tracking ID "
            f"{artin_id}."
        )


        # ====================================================
        # PHASE 7 — ATTACK DIRECTION
        # ====================================================
        ]



        st.header(
            "⚽ Team Attacking Direction"
        )


        st.write(
            """
The computer does not automatically know which
direction Artin's team is attacking.

Look at the video and select the direction.
"""
        )


        attack_direction = st.radio(
            "Artin's team attacks toward:",
            [
                "Right",
                "Left"
            ],
            horizontal=True
        )


        # ====================================================
        # PHASE 8 — START TRACKING
        # ====================================================

        start_tracking = st.button(
            "▶️ Start Tracking Artin",
            type="primary"
        )


        if start_tracking:

            # ------------------------------------------------
            # Fresh model
            # ------------------------------------------------
            #
            # We start again from frame 1.
            #
            # This is important because the tracking IDs
            # are created by the tracker from the beginning.
            # ------------------------------------------------

            model = YOLO(
                "yolov8n.pt"
            )


            # ------------------------------------------------
            # Fresh video
            # ------------------------------------------------

            cap = cv2.VideoCapture(
                video_path
            )


            if not cap.isOpened():

                st.error(
                    "Could not open the video for tracking."
                )

                st.stop()


            # ------------------------------------------------
            # Tracking list
            # ------------------------------------------------

            artin_positions = []


            frame_number = 0


            progress_bar = st.progress(
                0
            )


            status = st.empty()


            # =================================================
            # TRACK EVERY FRAME
            # =================================================

            while True:

                ret, frame = cap.read()


                if not ret:

                    break


                frame_number += 1


                # ------------------------------------------------
                # YOLO tracking
                # ------------------------------------------------

                results = model.track(
                    frame,
                    persist=True,
                    tracker="bytetrack.yaml",
                    classes=[0],
                    verbose=False
                )


                result = results[0]


                # ------------------------------------------------
                # Check whether tracking IDs exist
                # ------------------------------------------------

                if result.boxes.id is not None:


                    boxes = (
                        result.boxes
                        .xyxy
                        .cpu()
                        .tolist()
                    )


                    ids = (
                        result.boxes.id
                        .cpu()
                        .tolist()
                    )


                    # ------------------------------------------------
                    # Search for Artin
                    # ------------------------------------------------

                    for box, player_id in zip(
                        boxes,
                        ids
                    ):


                        player_id = int(
                            player_id
                        )


                        if player_id != int(
                            artin_id
                        ):

                            continue


                        # --------------------------------------------
                        # Bounding box
                        # --------------------------------------------

                        x1, y1, x2, y2 = box


                        # --------------------------------------------
                        # IMPORTANT:
                        #
                        # Use bottom-center of bounding box.
                        #
                        # This approximates the player's feet.
                        # --------------------------------------------

                        foot_x = (
                            x1 + x2
                        ) / 2


                        foot_y = y2


                        # --------------------------------------------
                        # Time
                        # --------------------------------------------

                        time_seconds = (
                            frame_number - 1
                        ) / fps


                        # --------------------------------------------
                        # Save tracking information
                        # --------------------------------------------

                        artin_positions.append({

                            "frame":
                                frame_number,

                            "time":
                                time_seconds,

                            "player_id":
                                player_id,

                            "pixel_x":
                                foot_x,

                            "pixel_y":
                                foot_y
                        })


                        break


                # ------------------------------------------------
                # Progress
                # ------------------------------------------------

                progress = (
                    frame_number /
                    max(total_frames, 1)
                )


                progress_bar.progress(
                    min(progress, 1.0)
                )


                status.write(
                    f"Tracking frame "
                    f"{frame_number} / "
                    f"{total_frames}"
                )


            cap.release()


            status.empty()


            # =================================================
            # PHASE 9 — CREATE DATAFRAME
            # =================================================

            artin_df = pd.DataFrame(
                artin_positions
            )


            st.session_state[
                "artin_df"
            ] = artin_df


            # ------------------------------------------------
            # Check result
            # ------------------------------------------------

            if artin_df.empty:

                st.error(
                    f"Tracking ID {artin_id} "
                    "was not found during the tracking pass."
                )


                st.warning(
                    """
This can happen when the tracking ID changes
between the ID-preview pass and the full video pass.

Try the following:

1. Click Find Players and Tracking IDs again.
2. Look carefully at the displayed frame.
3. Select the correct ID.
4. Start tracking again.
"""
                )


                st.stop()


            st.success(
                f"Successfully tracked "
                f"{player_name} in "
                f"{len(artin_df)} frames."
            )


            # =================================================
            # PHASE 10 — DISPLAY TRACKING DATA
            # =================================================

            st.header(
                "📊 Player Tracking Data"
            )


            st.dataframe(
                artin_df,
                use_container_width=True
            )


            # =================================================
            # PHASE 11 — CONVERT TO PITCH COORDINATES
            # =================================================

            st.header(
                "⚽ Convert Pixel Coordinates "
                "to Pitch Coordinates"
            )


            def convert_coordinates(
                pixel_x,
                pixel_y,
                frame_width,
                frame_height
            ):

                if frame_width <= 0:

                    raise ValueError(
                        "Frame width must be positive."
                    )


                if frame_height <= 0:

                    raise ValueError(
                        "Frame height must be positive."
                    )


                pitch_x = (
                    pixel_x /
                    frame_width
                ) * 120


                pitch_y = (
                    pixel_y /
                    frame_height
                ) * 80


                return (
                    pitch_x,
                    pitch_y
                )


            # ------------------------------------------------
            # Apply conversion
            # ------------------------------------------------

            artin_df[
                [
                    "pitch_x",
                    "pitch_y"
                ]
            ] = artin_df.apply(

                lambda row:

                pd.Series(

                    convert_coordinates(

                        row["pixel_x"],

                        row["pixel_y"],

                        width,

                        height
                    )
                ),

                axis=1
            )


            # =================================================
            # PHASE 12 — DISTANCE
            # =================================================

            st.header(
                "📏 Calculate Distance"
            )


            artin_df[
                "frame_gap"
            ] = artin_df[
                "frame"
            ].diff()


            artin_df[
                "distance_yards"
            ] = 0.0


            # ------------------------------------------------
            # IMPORTANT
            #
            # This is an educational filter.
            #
            # We do not allow impossible jumps to create
            # enormous distances.
            # ------------------------------------------------

            MAX_REASONABLE_SPEED = 12.0


            frame_time = (
                1 / fps
            )


            MAX_FRAME_DISTANCE = (
                MAX_REASONABLE_SPEED *
                frame_time
            )


            rejected_movements = 0


            for i in range(
                1,
                len(artin_df)
            ):


                # Only consecutive frames
                if (
                    artin_df.loc[
                        i,
                        "frame_gap"
                    ] != 1
                ):

                    continue


                x1 = artin_df.loc[
                    i - 1,
                    "pitch_x"
                ]


                y1 = artin_df.loc[
                    i - 1,
                    "pitch_y"
                ]


                x2 = artin_df.loc[
                    i,
                    "pitch_x"
                ]


                y2 = artin_df.loc[
                    i,
                    "pitch_y"
                ]


                distance = math.sqrt(

                    (x2 - x1) ** 2 +

                    (y2 - y1) ** 2
                )


                # ------------------------------------------------
                # Reject obvious tracking jumps
                # ------------------------------------------------

                if (
                    distance <=
                    MAX_FRAME_DISTANCE
                ):

                    artin_df.loc[
                        i,
                        "distance_yards"
                    ] = distance

                else:

                    rejected_movements += 1

                    artin_df.loc[
                        i,
                        "distance_yards"
                    ] = 0.0


            total_distance_yards = (
                artin_df[
                    "distance_yards"
                ].sum()
            )


            # =================================================
            # PHASE 13 — SPEED
            # =================================================

            st.header(
                "🏃 Estimated Speed"
            )


            artin_df[
                "time_difference"
            ] = artin_df[
                "time"
            ].diff()


            artin_df[
                "speed_yards_per_second"
            ] = 0.0


            for i in range(
                1,
                len(artin_df)
            ):


                if (
                    artin_df.loc[
                        i,
                        "frame_gap"
                    ] != 1
                ):

                    continue


                dt = artin_df.loc[
                    i,
                    "time_difference"
                ]


                distance = artin_df.loc[
                    i,
                    "distance_yards"
                ]


                if (
                    pd.notna(dt)
                    and
                    dt > 0
                ):


                    speed = (
                        distance /
                        dt
                    )


                    if (
                        speed <=
                        MAX_REASONABLE_SPEED
                    ):

                        artin_df.loc[
                            i,
                            "speed_yards_per_second"
                        ] = speed


            # ------------------------------------------------
            # Speed statistics
            # ------------------------------------------------

            moving_speeds = (
                artin_df.loc[
                    artin_df[
                        "speed_yards_per_second"
                    ] > 0,
                    "speed_yards_per_second"
                ]
            )


            if len(
                moving_speeds
            ) > 0:

                average_speed = (
                    moving_speeds.mean()
                )


                maximum_speed = (
                    moving_speeds.max()
                )

            else:

                average_speed = 0.0

                maximum_speed = 0.0


            # =================================================
            # PHASE 14 — TACTICAL ZONES
            # =================================================

            st.header(
                "🗺️ Tactical Movement Zones"
            )


            st.write(
                f"""
Artin's team is attacking toward the
**{attack_direction.lower()}** side of the video.

The pitch is divided into:

- Defense
- Midfield
- Final Third
"""
            )


            def get_zone(
                pitch_x,
                attack_direction
            ):

                # --------------------------------------------
                # Attacking RIGHT
                # --------------------------------------------

                if attack_direction == "Right":

                    if pitch_x < 40:

                        return "Defense"

                    elif pitch_x < 80:

                        return "Midfield"

                    else:

                        return "Final Third"


                # --------------------------------------------
                # Attacking LEFT
                # --------------------------------------------

                else:

                    if pitch_x > 80:

                        return "Defense"

                    elif pitch_x > 40:

                        return "Midfield"

                    else:

                        return "Final Third"


            artin_df[
                "zone"
            ] = artin_df[
                "pitch_x"
            ].apply(

                lambda x:

                get_zone(
                    x,
                    attack_direction
                )
            )


            # ------------------------------------------------
            # Zone percentages
            # ------------------------------------------------

            zone_percent = (

                artin_df[
                    "zone"
                ]
                .value_counts(
                    normalize=True
                )
                * 100
            )


            most_common_zone = (

                artin_df[
                    "zone"
                ]
                .value_counts()
                .idxmax()
            )


            final_third_percentage = (

                (
                    artin_df[
                        "zone"
                    ]
                    ==
                    "Final Third"
                )
                .mean()
                * 100
            )


            # =================================================
            # PHASE 15 — PERFORMANCE DASHBOARD
            # =================================================

            st.header(
                "📊 Player Performance"
            )


            col1, col2, col3, col4 = (
                st.columns(4)
            )


            col1.metric(
                "Distance Covered",
                f"{total_distance_yards:.1f} yd"
            )


            col2.metric(
                "Average Speed",
                f"{average_speed:.2f} yd/s"
            )


            col3.metric(
                "Maximum Speed",
                f"{maximum_speed:.2f} yd/s"
            )


            col4.metric(
                "Most Occupied Zone",
                most_common_zone
            )


            st.metric(
                "Final Third",
                f"{final_third_percentage:.1f}%"
            )


            st.caption(
                "⚠️ Distance and speed are educational "
                "estimates based on simplified pitch "
                "coordinate conversion."
            )


            # =================================================
            # PHASE 16 — MOVEMENT TRAJECTORY
            # =================================================

            st.header(
                "⚽ Movement Tragectory on the Soccer Pitch"
            )


            pitch = Pitch(

                pitch_type="statsbomb",

                pitch_color="#aabb97",

                line_color="white"
            )


            fig, ax = pitch.draw(
                figsize=(10, 7)
            )


            pitch.plot(

                artin_df[
                    "pitch_x"
                ],

                artin_df[
                    "pitch_y"
                ],

                ax=ax,

                linewidth=2
            )


            pitch.scatter(

                artin_df[
                    "pitch_x"
                ],

                artin_df[
                    "pitch_y"
                ],

                ax=ax,

                s=15
            )


            ax.set_title(
                f"{player_name}'s Movement"
            )


            st.pyplot(
                fig
            )


            plt.close(
                fig
            )


            # =================================================
            # PHASE 18 — HEATMAP
            # =================================================

            st.header(
                "🔥 Movement Heatmap"
            )


            pitch = Pitch(

                pitch_type="statsbomb",

                pitch_color="#aabb97",

                line_color="white"
            )


            fig, ax = pitch.draw(
                figsize=(10, 7)
            )


            bin_statistic = (
                pitch.bin_statistic(

                    artin_df[
                        "pitch_x"
                    ],

                    artin_df[
                        "pitch_y"
                    ],

                    statistic="count",

                    bins=(12, 8)
                )
            )


            pitch.heatmap(

                bin_statistic,

                ax=ax,

                cmap="Reds",

                alpha=0.6
            )


            pitch.scatter(

                artin_df[
                    "pitch_x"
                ],

                artin_df[
                    "pitch_y"
                ],

                ax=ax,

                s=15
            )


            ax.set_title(
                f"{player_name}'s Movement Heatmap"
            )


            st.pyplot(
                fig
            )


            plt.close(
                fig
            )


            # =================================================
            # PHASE 19 — ZONE ANALYSIS
            # =================================================

            st.header(
                "🗺️ Zone Analysis"
            )


            st.dataframe(
                zone_percent.round(1)
                .rename(
                    "Percentage"
                ),
                use_container_width=True
            )


            # =================================================
            # PHASE 20 — TRACKING TABLE
            # =================================================

            st.header(
                "📋 Complete Tracking Dataset"
            )


            st.dataframe(
                artin_df,
                use_container_width=True
            )


            # =================================================
            # PHASE 21 — DOWNLOAD DATA
            # =================================================

            st.header(
                "💾 Save Tracking Data"
            )


            csv_data = (
                artin_df.to_csv(
                    index=False
                )
            )


            st.download_button(

                label=
                    "⬇️ Download Artin Tracking CSV",

                data=
                    csv_data,

                file_name=
                    f"{player_name.lower()}_tracking.csv",

                mime=
                    "text/csv"
            )


            # =================================================
            # PHASE 22 — PERFORMANCE SUMMARY
            # =================================================

            st.header(
                "🏆 Performance Summary"
            )


            performance_summary = {

                "Player":
                    player_name,

                "Position":
                    position,

                "Tracking ID":
                    int(artin_id),

                "Tracked Frames":
                    len(artin_df),

                "Distance Covered (yards)":
                    round(
                        total_distance_yards,
                        2
                    ),

                "Average Estimated Speed (yd/s)":
                    round(
                        average_speed,
                        2
                    ),

                "Maximum Estimated Speed (yd/s)":
                    round(
                        maximum_speed,
                        2
                    ),

                "Most Occupied Zone":
                    most_common_zone,

                "Final Third Percentage":
                    round(
                        final_third_percentage,
                        1
                    ),

                "Rejected Tracking Jumps":
                    rejected_movements
            }


            summary_df = pd.DataFrame(

                performance_summary.items(),

                columns=[
                    "Metric",
                    "Value"
                ]
            )


            st.dataframe(
                summary_df,
                use_container_width=True
            )


            # =================================================
            # PHASE 23 — MISSION 13 COMPLETE
            # =================================================

            st.success(
                """
                🎉 Mission 13 Complete!
                """)
        
