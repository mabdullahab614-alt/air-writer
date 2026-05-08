<div align="center">

<!-- LOGO PLACEHOLDER -->
<!-- <img src="assets/logo.png" alt="Air Writer Logo" width="140" /> -->

# ✋ AIR WRITER

### *Your hand is the only interface you'll ever need.*

> Draw, write, and control your entire PC — in mid-air — powered by real-time AI hand tracking.

<br/>

[![Stars](https://img.shields.io/github/stars/mabdullahab614-alt/air-writer?style=for-the-badge&color=FFD700&labelColor=0d1117)](https://github.com/mabdullahab614-alt/air-writer/stargazers)
[![Forks](https://img.shields.io/github/forks/mabdullahab614-alt/air-writer?style=for-the-badge&color=00f5ff&labelColor=0d1117)](https://github.com/mabdullahab614-alt/air-writer/network/members)
[![Issues](https://img.shields.io/github/issues/mabdullahab614-alt/air-writer?style=for-the-badge&color=ff006e&labelColor=0d1117)](https://github.com/mabdullahab614-alt/air-writer/issues)
[![License](https://img.shields.io/github/license/mabdullahab614-alt/air-writer?style=for-the-badge&color=bf00ff&labelColor=0d1117)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117)](https://python.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-0097A7?style=for-the-badge&logo=google&logoColor=white&labelColor=0d1117)](https://mediapipe.dev)

<br/>

<!-- DEMO GIF PLACEHOLDER -->
<!-- <img src="assets/demo.gif" alt="Air Writer Demo" width="700" /> -->

</div>

---

## 🔥 The Hook

**Air Writer** eliminates the boundary between thought and digital creation. Using nothing but a standard webcam and your bare hand, the AI tracks 21 precise landmark points on your fingers in real time — letting you draw, erase, and navigate your entire PC without touching a single device. This is not a prototype — it's a fully working, production-ready human-computer interaction system built by a BS AI student at UMT Lahore, and it runs in your browser right now.

---

## 🎯 Two Powerful Modes

<div align="center">

| Mode | Launch File | Interface |
|------|-------------|-----------|
| ✋ **Air Writer** | `app.py` | Gradio Web App (Browser) |
| 🖥️ **Air PC Controller** | `controller.py` | Native Desktop Window |

</div>

---

## ✨ Feature Showcase

### ✋ Air Writer — Draw in the Air

<table>
  <tr>
    <td>☝️ <b>Index Finger Up</b></td>
    <td>Enters <b>DRAW</b> mode — your fingertip becomes the pen</td>
  </tr>
  <tr>
    <td>✌️ <b>Two Fingers Up</b></td>
    <td>Enters <b>MOVE</b> mode — lifts the pen, reposition freely</td>
  </tr>
  <tr>
    <td>🖐️ <b>All Fingers Up</b></td>
    <td>Enters <b>ERASE</b> mode — wipes a 40px radius circle in real time</td>
  </tr>
  <tr>
    <td>🎨 <b>5-Color Palette</b></td>
    <td>Green · Blue · Red · Yellow · White — switchable from the sidebar</td>
  </tr>
  <tr>
    <td>🗑️ <b>Clear Canvas</b></td>
    <td>One-click canvas wipe via the Gradio UI</td>
  </tr>
  <tr>
    <td>📷 <b>Live Overlay</b></td>
    <td>Drawing is composited directly onto the live camera feed</td>
  </tr>
  <tr>
    <td>🌐 <b>Browser-Based UI</b></td>
    <td>Runs fully in-browser via Gradio — no native GUI needed</td>
  </tr>
</table>

---

### 🖥️ Air PC Controller — Control Your PC with Gestures

<table>
  <tr>
    <td>☝️ <b>Index Finger</b></td>
    <td>Moves the mouse cursor (smoothed with 7-frame interpolation)</td>
  </tr>
  <tr>
    <td>👌 <b>Pinch — Thumb + Index</b></td>
    <td>Left Click (20-frame cooldown to prevent double-firing)</td>
  </tr>
  <tr>
    <td>🤏 <b>Pinch — Thumb + Middle</b></td>
    <td>Right Click</td>
  </tr>
  <tr>
    <td>✌️ <b>2 Fingers Pinched Together</b></td>
    <td>Double Click</td>
  </tr>
  <tr>
    <td>🖐️ <b>All 5 Fingers Up</b></td>
    <td>Scroll Up (3 units)</td>
  </tr>
  <tr>
    <td>✊ <b>Fist — All Fingers Down</b></td>
    <td>Scroll Down (3 units)</td>
  </tr>
</table>

---

## 🏗️ Tech Architecture

<div align="center">

| Layer | Technology | Role |
|-------|-----------|------|
| 🧠 **AI / CV** | [MediaPipe 0.10.21](https://mediapipe.dev) | 21-point hand landmark detection at 30fps |
| 👁️ **Vision** | [OpenCV 4.x](https://opencv.org) | Camera feed, canvas blending, drawing primitives |
| 🌐 **Web UI** | [Gradio 6.x](https://gradio.app) | Streaming webcam + real-time output display |
| 🖱️ **OS Control** | [PyAutoGUI 0.9.54](https://pyautogui.readthedocs.io) | Cross-platform mouse, click, scroll |
| 🔢 **Math** | [NumPy < 2.0](https://numpy.org) | Landmark interpolation, coordinate mapping |
| 🖼️ **Images** | [Pillow 12.x](https://pillow.readthedocs.io) | Frame conversion for Gradio pipeline |
| 🐍 **Runtime** | Python 3.12 | Core language |

</div>

---

## 🧠 How It Works

```
Webcam Frame
     │
     ▼
MediaPipe Hands  ──►  21 Landmarks (x, y, z per joint)
     │
     ▼
fingers_up()  ──►  [thumb, index, middle, ring, pinky] boolean array
     │
     ├── index only      ──►  DRAW  → cv2.line() on canvas
     ├── index + middle  ──►  MOVE  → lift pen, reposition
     └── all up          ──►  ERASE → cv2.circle() black mask
     │
     ▼
Bitwise Merge (canvas + camera frame)
     │
     ▼
HUD Overlay → Gradio Output Stream
```

---

## ⚡ Performance

> **Tested on:** Windows 10, Python 3.12, standard 720p webcam

| Metric | Value |
|--------|-------|
| Hand detection latency | ~30ms per frame |
| Landmark confidence threshold | 0.70 |
| Tracking confidence threshold | 0.70 |
| Cursor smoothing factor | 7-frame weighted average |
| Click cooldown | 20 frames (~667ms at 30fps) |
| Erase brush radius | 40 pixels |
| Canvas draw thickness | 8 pixels |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- A working webcam
- Windows / macOS / Linux

---

### 1 — Clone the Repository

```bash
git clone https://github.com/mabdullahab614-alt/air-writer.git
cd air-writer
```

---

### 2 — Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

---

### 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you have TensorFlow installed system-wide, use the virtual environment above to avoid protobuf version conflicts.

---

### 4 — Run Air Writer (Web App)

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:7860**

---

### 5 — Run Air PC Controller (Desktop)

```bash
python controller.py
```

A native OpenCV window opens. Press **Q** to quit.

---

## 🎮 Usage Guide

### Air Writer (Browser)

1. Allow camera access when prompted by the browser
2. Your live feed appears on the right panel
3. **Raise your index finger** to start drawing
4. **Switch colors** using the radio buttons on the left
5. **Raise all fingers** to switch to Erase mode
6. **Tick "Clear Canvas"** to wipe and start fresh

### Air PC Controller (Desktop)

1. Hold your hand flat in front of the camera
2. Move your **index finger** to control the cursor
3. **Pinch thumb + index** to left-click
4. **Pinch thumb + middle** to right-click
5. **Open palm** to scroll up, **make a fist** to scroll down
6. Press **Q** to exit

---

## 📁 Project Structure

```
air-writer/
│
├── app.py              # Gradio web app — Air Writer
├── gradio_app.py       # Alternate Gradio interface
├── controller.py       # Desktop Air PC Controller
├── requirements.txt    # Pinned dependencies
├── .gitignore          # Excludes venv, cache
└── README.md           # This file
```

---

## 🤝 Contributing

Contributions are what make the open-source community extraordinary. Any improvements are **greatly appreciated**.

```bash
# 1. Fork the project
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes
git commit -m "Add AmazingFeature"

# 4. Push to your branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request
```

**Ideas welcome:**
- Multi-hand support
- Shape recognition (circle, line, rectangle detection)
- Export drawing as SVG
- Gesture-based color switching (no UI needed)
- Mobile browser support via WebRTC

---

## 🐛 Known Issues & Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: mediapipe` | Run inside the `venv` — do not use system Python if TensorFlow is installed |
| Camera not detected | Check webcam permissions in your OS settings |
| Gradio page loads but no camera | Allow camera access in browser when prompted |
| Cursor jumps erratically | Improve lighting; keep hand within frame center |
| Drawing lags | Lower your webcam resolution in `cap.set()` |

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 👨‍💻 Author

<div align="center">

**Abdullah Javid**
BS Artificial Intelligence · University of Management and Technology (UMT), Lahore

[![GitHub](https://img.shields.io/badge/GitHub-mabdullahab614--alt-181717?style=for-the-badge&logo=github&labelColor=0d1117)](https://github.com/mabdullahab614-alt)

*"The best interface is no interface."*

</div>

---

<div align="center">

⭐ **If this project saved you time or inspired you, drop a star — it means the world.** ⭐

</div>
