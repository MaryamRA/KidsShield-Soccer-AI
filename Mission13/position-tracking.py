# ============================================
# Phase 3 — Track Artin's Position
# ============================================

# IMPORTANT:
# Create a completely fresh YOLO model.
# This creates a fresh ByteTrack tracker state.
model = YOLO("yolov8n.pt")

# Change this after inspecting the IDs from this SAME tracking run.
artin_id = 4

artin_positions = []

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise FileNotFoundError(
        f"Could not open video: {video_path}"
    )

frame_number = 0

# Keep track of every ID that appears
all_tracking_ids = set()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_number += 1

    # Track PEOPLE only
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0],
        verbose=False
    )

    result = results[0]

    # No tracking IDs in this frame
    if result.boxes.id is None:
        continue

    boxes = result.boxes.xyxy.cpu().tolist()
    ids = result.boxes.id.cpu().tolist()

    for box, player_id in zip(boxes, ids):

        player_id = int(player_id)

        # Remember every ID YOLO sees
        all_tracking_ids.add(player_id)

        # Look for Artin
        if player_id == artin_id:

            x1, y1, x2, y2 = box

            # Center of bounding box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            time_seconds = (
                frame_number - 1
            ) / fps

            artin_positions.append({
                "frame": frame_number,
                "time": time_seconds,
                "player_id": player_id,
                "pixel_x": center_x,
                "pixel_y": center_y
            })

# Close video
cap.release()

# Convert to DataFrame
artin_df = pd.DataFrame(artin_positions)

print("=" * 50)
print("TRACKING RESULTS")
print("=" * 50)

print("All tracking IDs found:")
print(sorted(all_tracking_ids))

print()

print("Selected Artin ID:")
print(artin_id)

print()

print("Tracked Artin positions:")
print(len(artin_df))

print("=" * 50)

# Check whether the selected ID was found
if artin_df.empty:

    print()
    print("❌ Artin was NOT found.")
    print()
    print(
        f"ID {artin_id} was not found during this "
        "tracking run."
    )
    print()
    print(
        "IMPORTANT: The tracking ID may have changed."
    )
    print(
        "Use the IDs printed above to identify "
        "Artin again."
    )

else:

    print()
    print("✅ Artin tracking successful!")
    print()

    display(artin_df.head(10))
