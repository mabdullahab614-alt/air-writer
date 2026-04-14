import cv2
import mediapipe as mp
import numpy as np

# ─── Setup ───────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(max_num_hands=1,
                           min_detection_confidence=0.7,
                           min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# ─── Canvas ──────────────────────────────────────────
canvas     = np.zeros((720, 1280, 3), dtype=np.uint8)
prev_x, prev_y = 0, 0
draw_color = (0, 255, 0)   # default green
thickness  = 8
mode       = "DRAW"        # DRAW or ERASE

COLORS = {
    "GREEN":  (0, 255, 0),
    "BLUE":   (255, 100, 0),
    "RED":    (0, 0, 255),
    "YELLOW": (0, 255, 255),
    "WHITE":  (255, 255, 255),
}

def get_landmark_pos(lm, idx, w, h):
    pt = lm.landmark[idx]
    return int(pt.x * w), int(pt.y * h)

def fingers_up(lm, w, h):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    up = []
    for t, p in zip(tips, pips):
        ty = lm.landmark[t].y
        py = lm.landmark[p].y
        up.append(ty < py)
    # Thumb
    tx = lm.landmark[4].x
    mx = lm.landmark[3].x
    up.insert(0, tx < mx)
    return up

print("✅ Air Writer Started!")
print("☝️  Index finger = DRAW")
print("✌️  Two fingers  = MOVE (no draw)")
print("🖐️  All fingers  = ERASE")
print("Press 'c' to clear | 's' to save | 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w  = frame.shape[:2]
    rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res   = hands.process(rgb)

    # ── Color palette buttons (top bar) ──────────────
    colors_list = list(COLORS.items())
    btn_w = 120
    for i, (name, col) in enumerate(colors_list):
        x1 = i * btn_w
        cv2.rectangle(frame, (x1, 0), (x1 + btn_w, 60), col, -1)
        cv2.putText(frame, name, (x1 + 5, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

    # Erase button
    cv2.rectangle(frame, (len(colors_list)*btn_w, 0),
                  (len(colors_list)*btn_w + btn_w, 60), (50,50,50), -1)
    cv2.putText(frame, "ERASE", (len(colors_list)*btn_w + 10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

        ix, iy = get_landmark_pos(lm, 8, w, h)   # index tip
        fx = ix  # finger x

        up = fingers_up(lm, w, h)
        index_up  = up[1]
        middle_up = up[2]
        all_up    = all(up[1:])   # 4 fingers up = erase

        # ── Color / erase selection (hand in top bar) ──
        if iy < 60:
            for i, (name, col) in enumerate(colors_list):
                if i * btn_w < ix < (i+1) * btn_w:
                    draw_color = col
                    mode = "DRAW"
            if len(colors_list)*btn_w < ix < (len(colors_list)+1)*btn_w:
                mode = "ERASE"
            prev_x, prev_y = 0, 0
            continue

        # ── Drawing modes ──────────────────────────────
        if all_up:
            mode = "ERASE"
        elif index_up and not middle_up:
            mode = "DRAW"
        elif index_up and middle_up:
            mode = "MOVE"
            prev_x, prev_y = 0, 0

        if mode == "DRAW":
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = ix, iy
            cv2.line(canvas, (prev_x, prev_y), (ix, iy),
                     draw_color, thickness)
            prev_x, prev_y = ix, iy

        elif mode == "ERASE":
            cv2.circle(canvas, (ix, iy), 40, (0,0,0), -1)
            prev_x, prev_y = 0, 0

        # Draw cursor
        color_show = (0,0,200) if mode=="ERASE" else draw_color
        cv2.circle(frame, (ix, iy), 12, color_show, -1)

    else:
        prev_x, prev_y = 0, 0

    # ── Merge canvas onto frame ───────────────────────
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(canvas_gray, 5, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    merged = cv2.add(frame_bg, canvas_fg)

    # ── HUD ──────────────────────────────────────────
    cv2.putText(merged, f"Mode: {mode}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,0,200) if mode=="ERASE" else draw_color, 3)
    cv2.putText(merged, "C=Clear  S=Save  Q=Quit", (10, 710),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180,180,180), 2)

    cv2.imshow("✋ Air Writer — Abdullah Javid", merged)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
        print("🗑️  Canvas cleared!")
    elif key == ord('s'):
        fname = "drawing.png"
        cv2.imwrite(fname, canvas)
        print(f"💾 Saved as {fname}")

cap.release()
cv2.destroyAllWindows()