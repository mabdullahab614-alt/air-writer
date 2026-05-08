import gradio as gr
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

# ─── MediaPipe Setup ─────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ─── Canvas ──────────────────────────────────────────
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
prev_x, prev_y = 0, 0

COLORS = {
    "🟢 Green":  (0, 255, 0),
    "🔵 Blue":   (255, 100, 0),
    "🔴 Red":    (0, 0, 255),
    "🟡 Yellow": (0, 255, 255),
    "⬜ White":  (255, 255, 255),
}

current_color = (0, 255, 0)
current_mode  = "DRAW"

def fingers_up(lm):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    up = []
    for t, p in zip(tips, pips):
        up.append(lm.landmark[t].y < lm.landmark[p].y)
    up.insert(0, lm.landmark[4].x < lm.landmark[3].x)
    return up

def process_frame(frame, color_choice, clear_canvas):
    global canvas, prev_x, prev_y, current_color, current_mode

    if frame is None:
        return None, "No camera feed"

    # Convert PIL to numpy
    frame = np.array(frame)
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    h, w  = frame.shape[:2]

    # Resize canvas if needed
    if canvas.shape[:2] != (h, w):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Clear canvas if requested
    if clear_canvas:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        prev_x, prev_y = 0, 0

    # Set color
    current_color = COLORS.get(color_choice, (0, 255, 0))

    # Process hand
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    gesture_text = "✋ Show your hand!"
    color_display = current_color

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

        ix = int(lm.landmark[8].x * w)
        iy = int(lm.landmark[8].y * h)

        up = fingers_up(lm)
        index_up  = up[1]
        middle_up = up[2]
        all_up    = all(up[1:])

        if all_up:
            current_mode = "ERASE"
            gesture_text = "🖐️ ERASING"
            prev_x, prev_y = 0, 0
        elif index_up and middle_up:
            current_mode = "MOVE"
            gesture_text = "✌️ MOVING"
            prev_x, prev_y = 0, 0
        elif index_up:
            current_mode = "DRAW"
            gesture_text = "☝️ DRAWING"

        if current_mode == "DRAW":
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = ix, iy
            cv2.line(canvas, (prev_x, prev_y), (ix, iy),
                     current_color, 8)
            prev_x, prev_y = ix, iy
        elif current_mode == "ERASE":
            cv2.circle(canvas, (ix, iy), 40, (0,0,0), -1)
            prev_x, prev_y = 0, 0

        # Draw cursor
        cur_color = (0,0,200) if current_mode=="ERASE" else current_color
        cv2.circle(frame, (ix, iy), 12, cur_color, -1)

    else:
        prev_x, prev_y = 0, 0
        gesture_text = "✋ Show your hand!"

    # Merge canvas onto frame
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask     = cv2.threshold(canvas_gray, 5, 255, cv2.THRESH_BINARY)
    mask_inv    = cv2.bitwise_not(mask)
    frame_bg    = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg   = cv2.bitwise_and(canvas, canvas, mask=mask)
    merged      = cv2.add(frame_bg, canvas_fg)

    # HUD
    cv2.rectangle(merged, (0, 0), (w, 45), (20,20,20), -1)
    cv2.putText(merged, f"Mode: {current_mode}  |  {gesture_text}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0,0,200) if current_mode=="ERASE" else current_color, 2)

    # Convert back to RGB for Gradio
    merged = cv2.cvtColor(merged, cv2.COLOR_BGR2RGB)
    return merged, gesture_text

# ─── Gradio Interface ────────────────────────────────
CSS = """
body { background: #0a0a0f !important; }
.gradio-container {
    background: linear-gradient(135deg, #0a0a0f, #0d1117) !important;
    font-family: 'Segoe UI', sans-serif !important;
}
.main-title {
    text-align: center;
    font-size: 2.5em;
    font-weight: 900;
    background: linear-gradient(90deg, #00f5ff, #bf00ff, #ff006e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 20px 0 5px;
    letter-spacing: 3px;
}
"""

with gr.Blocks(title="✋ Air Writer — Abdullah Javid", css=CSS) as app:

    gr.HTML("""
    <div class="main-title">✋ AIR WRITER</div>
    <div style="text-align:center; color:#00ff88; font-size:0.9em;
                letter-spacing:2px; margin-bottom:20px;">
        ▸ DRAW IN AIR WITH YOUR FINGER · POWERED BY MEDIAPIPE ◂
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Controls")

            color_choice = gr.Radio(
                choices=list(COLORS.keys()),
                value="🟢 Green",
                label="🎨 Drawing Color"
            )

            clear_btn = gr.Checkbox(
                label="🗑️ Clear Canvas",
                value=False
            )

            gr.Markdown("""
---
### ✋ Gesture Guide
| Gesture | Action |
|---------|--------|
| ☝️ 1 finger | Draw |
| ✌️ 2 fingers | Move |
| 🖐️ All fingers | Erase |

---
### 💡 Tips
- Good lighting helps!
- Keep hand visible
- Move slowly for better drawing
- Use clear background

---
**Built by Abdullah Javid**
**BS AI @ UMT Lahore**
            """)

        with gr.Column(scale=2):
            gr.Markdown("### 📷 Live Camera Feed")
            cam_input  = gr.Image(
                sources=["webcam"],
                streaming=True,
                label="Your Camera"
            )
            output_img = gr.Image(
                label="✋ Air Writer Output",
                streaming=True
            )
            gesture_out = gr.Textbox(
                label="🖐️ Detected Gesture",
                interactive=False
            )

    cam_input.stream(
        fn=process_frame,
        inputs=[cam_input, color_choice, clear_btn],
        outputs=[output_img, gesture_out]
    )

    gr.HTML("""
    <div style="text-align:center; padding:16px; color:rgba(0,245,255,0.3);
                font-size:0.75em; letter-spacing:2px; margin-top:10px;
                border-top:1px solid rgba(0,245,255,0.1);">
        ✋ AIR WRITER · BUILT BY ABDULLAH JAVID · BS AI @ UMT LAHORE · PAKAI MEDICAL
    </div>
    """)

app.launch()