import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# ─── Safety ──────────────────────────────────────────
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# ─── Screen size ─────────────────────────────────────
SCREEN_W, SCREEN_H = pyautogui.size()

# ─── Camera ──────────────────────────────────────────
CAM_W, CAM_H = 640, 480

# ─── MediaPipe ───────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

cap = cv2.VideoCapture(0)
cap.set(3, CAM_W)
cap.set(4, CAM_H)

# ─── Smoothing ───────────────────────────────────────
smooth = 7
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

# ─── Click state ─────────────────────────────────────
click_cooldown   = 0
rclick_cooldown  = 0
scroll_cooldown  = 0
COOLDOWN_FRAMES  = 20

def get_pos(lm, idx):
    return lm.landmark[idx].x, lm.landmark[idx].y

def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def fingers_up(lm):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    up = []
    for t, p in zip(tips, pips):
        up.append(lm.landmark[t].y < lm.landmark[p].y)
    # Thumb
    up.insert(0, lm.landmark[4].x < lm.landmark[3].x)
    return up

print("✅ Air PC Controller Started!")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("☝️  Index finger    = Move cursor")
print("👌 Pinch index+thumb = Left click")
print("✌️  2 fingers pinch  = Right click")
print("🖐️  All 5 up         = Scroll up")
print("👊 Fist (all down)   = Scroll down")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("Press Q to quit")

# ─── Reduce movement area to center of frame ─────────
MARGIN = 100  # pixels from edge — smaller = bigger movement

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res   = hands.process(rgb)

    # Decrement cooldowns
    click_cooldown  = max(0, click_cooldown  - 1)
    rclick_cooldown = max(0, rclick_cooldown - 1)
    scroll_cooldown = max(0, scroll_cooldown - 1)

    gesture_text = "No Hand"
    color        = (100, 100, 100)

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

        up = fingers_up(lm)

        # Key landmark positions
        idx_tip   = get_pos(lm, 8)   # index tip
        mid_tip   = get_pos(lm, 12)  # middle tip
        thumb_tip = get_pos(lm, 4)   # thumb tip
        wrist     = get_pos(lm, 0)

        # ── CURSOR MOVEMENT (index finger) ────────────
        # Map from [MARGIN, CAM_W-MARGIN] → [0, SCREEN_W]
        raw_x = np.interp(idx_tip[0], [MARGIN/CAM_W, 1-MARGIN/CAM_W], [0, SCREEN_W])
        raw_y = np.interp(idx_tip[1], [MARGIN/CAM_H, 1-MARGIN/CAM_H], [0, SCREEN_H])

        # Smooth cursor
        curr_x = prev_x + (raw_x - prev_x) / smooth
        curr_y = prev_y + (raw_y - prev_y) / smooth
        prev_x, prev_y = curr_x, curr_y

        pyautogui.moveTo(int(curr_x), int(curr_y))

        # ── GESTURE DETECTION ─────────────────────────

        # 1️⃣ LEFT CLICK — pinch thumb + index
        pinch_dist = distance(thumb_tip, idx_tip)
        if pinch_dist < 0.05 and click_cooldown == 0:
            pyautogui.click()
            click_cooldown = COOLDOWN_FRAMES
            gesture_text = "LEFT CLICK! 👆"
            color = (0, 255, 0)

        # 2️⃣ RIGHT CLICK — pinch thumb + middle
        elif distance(thumb_tip, mid_tip) < 0.05 and rclick_cooldown == 0:
            pyautogui.rightClick()
            rclick_cooldown = COOLDOWN_FRAMES
            gesture_text = "RIGHT CLICK! 👆"
            color = (0, 165, 255)

        # 3️⃣ SCROLL UP — all 5 fingers up
        elif all(up) and scroll_cooldown == 0:
            pyautogui.scroll(3)
            scroll_cooldown = COOLDOWN_FRAMES
            gesture_text = "SCROLL UP 🔼"
            color = (255, 255, 0)

        # 4️⃣ SCROLL DOWN — fist (all fingers down)
        elif not any(up[1:]) and scroll_cooldown == 0:
            pyautogui.scroll(-3)
            scroll_cooldown = COOLDOWN_FRAMES
            gesture_text = "SCROLL DOWN 🔽"
            color = (0, 0, 255)

        # 5️⃣ DOUBLE CLICK — index + middle up, pinch
        elif up[1] and up[2] and distance(idx_tip, mid_tip) < 0.04 and click_cooldown == 0:
            pyautogui.doubleClick()
            click_cooldown = COOLDOWN_FRAMES * 2
            gesture_text = "DOUBLE CLICK! ✌️"
            color = (255, 0, 255)

        # Default — just moving
        else:
            gesture_text = "MOVING 🖱️"
            color = (0, 255, 255)

        # Draw index fingertip
        ix = int(idx_tip[0] * CAM_W)
        iy = int(idx_tip[1] * CAM_H)
        cv2.circle(frame, (ix, iy), 12, color, -1)

    # ── HUD ──────────────────────────────────────────
    # Background bar
    cv2.rectangle(frame, (0, 0), (CAM_W, 50), (20, 20, 20), -1)

    cv2.putText(frame, f"Gesture: {gesture_text}",
                (10, 35), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, color, 2)

    # Instructions
    instructions = [
        "☝ Move  |  Pinch=Click  |  All up=ScrollUp",
        "Fist=ScrollDown  |  Q=Quit"
    ]
    for i, txt in enumerate(instructions):
        cv2.putText(frame, txt, (10, CAM_H - 30 + i*20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                    (180, 180, 180), 1)

    cv2.imshow("✋ Air PC Controller — Abdullah Javid", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Controller stopped!")