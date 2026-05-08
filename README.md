---
title: Air Writer
emoji: ✋
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "6.14.0"
app_file: app.py
pinned: false
license: mit
---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=✋%20AIR%20WRITER&fontSize=60&fontColor=00f5ff&animation=twinkling&fontAlignY=38&desc=Draw%20in%20mid-air%20with%20your%20bare%20hand&descAlignY=58&descColor=bf00ff&descSize=20" width="100%"/>

<br/>

[![HF Spaces](https://img.shields.io/badge/🤗%20HuggingFace-LIVE%20DEMO-FF6F00?style=for-the-badge&labelColor=0d1117)](https://huggingface.co/spaces/Abdullah2894830/air-writer)
[![GitHub](https://img.shields.io/badge/GitHub-air--writer-181717?style=for-the-badge&logo=github&labelColor=0d1117)](https://github.com/mabdullahab614-alt/air-writer)
[![Stars](https://img.shields.io/github/stars/mabdullahab614-alt/air-writer?style=for-the-badge&color=FFD700&labelColor=0d1117)](https://github.com/mabdullahab614-alt/air-writer/stargazers)
[![License](https://img.shields.io/badge/License-MIT-bf00ff?style=for-the-badge&labelColor=0d1117)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117)](https://python.org)
[![Status](https://img.shields.io/badge/Status-LIVE%20%F0%9F%9F%A2-00ff88?style=for-the-badge&labelColor=0d1117)](https://huggingface.co/spaces/Abdullah2894830/air-writer)

<br/>

> **Your webcam is the canvas. Your finger is the brush. No hardware required.**

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"/>

</div>

---

## 🔥 What Is Air Writer?

**Air Writer** is a real-time computer vision application that turns your bare hand into a digital drawing tool. Using **MediaPipe's 21-point hand landmark detection**, it tracks your finger position at 30fps and lets you draw, move, and erase — all in mid-air, through any webcam, in your browser. No stylus. No touchscreen. No install.

```
Webcam → MediaPipe (21 landmarks) → Gesture Classification → Canvas Rendering → Your Browser
```

---

## ✨ Feature Showcase

<table>
<tr>
<td width="50%">

### ✍️ Air Writer (Web App)
| Gesture | Action |
|---------|--------|
| ☝️ Index finger up | **DRAW** — trace pixel-perfect lines |
| ✌️ Index + Middle up | **MOVE** — reposition without marking |
| 🖐️ All fingers up | **ERASE** — wipe a 40px radius instantly |
| 🗑️ Clear Canvas btn | **RESET** — blank slate in one click |

</td>
<td width="50%">

### 🖥️ Air PC Controller (Desktop)
| Gesture | Action |
|---------|--------|
| ☝️ Index finger | Move mouse cursor |
| 👌 Pinch index+thumb | Left click |
| 🤏 Pinch middle+thumb | Right click |
| ✌️ 2 fingers pinched | Double click |
| 🖐️ Open palm | Scroll up |
| ✊ Fist | Scroll down |

</td>
</tr>
</table>

### 🎨 Color Palette
![Green](https://img.shields.io/badge/●-Green-00ff00?style=flat-square)
![Blue](https://img.shields.io/badge/●-Blue-6464ff?style=flat-square)
![Red](https://img.shields.io/badge/●-Red-ff3333?style=flat-square)
![Yellow](https://img.shields.io/badge/●-Yellow-ffff00?style=flat-square)
![White](https://img.shields.io/badge/●-White-ffffff?style=flat-square)

---

## 🏗️ Tech Stack

<div align="center">

| Layer | Technology | Version | Role |
|-------|-----------|---------|------|
| 🧠 **AI / Vision** | MediaPipe | 0.10.35 | 21-point hand landmark detection @ 30fps |
| 👁️ **Image Processing** | OpenCV | 4.x | Camera flip, canvas blend, drawing primitives |
| 🌐 **Web Interface** | Gradio | 6.14.0 | Streaming webcam + live output rendering |
| 🔢 **Numerics** | NumPy | 1.26.4 | Coordinate mapping, bitwise mask operations |
| 🖼️ **Images** | Pillow | 12.x | Frame format conversion for Gradio pipeline |
| 🖱️ **OS Control** | PyAutoGUI | 0.9.54 | Mouse movement, clicks, scroll (controller mode) |
| 🐍 **Runtime** | Python | 3.12 | Core language |

</div>

---

## ⚡ How It Works

```python
# 1. Capture webcam frame (RGB via Gradio)
frame → flip(mirror) → MediaPipe HandLandmarker

# 2. Get 21 hand landmarks
landmarks[8]  = index fingertip  →  drawing cursor
landmarks[4]  = thumb tip        →  click detection (controller)

# 3. Classify gesture
fingers_up() → [thumb, index, middle, ring, pinky]
  all[1:]     → ERASE mode
  [1] + [2]   → MOVE  mode
  [1] only    → DRAW  mode

# 4. Render
cv2.line(canvas, prev, current, color, thickness=8)

# 5. Composite
merged = bitwise_and(frame, mask_inv) + bitwise_and(canvas, mask)

# 6. Stream to browser via Gradio
return cv2.cvtColor(merged, COLOR_BGR2RGB)
```

---

## 📊 Performance Specs

| Metric | Value |
|--------|-------|
| Hand detection | MediaPipe Tasks API (0.10.35) |
| Landmark points | 21 per hand |
| Detection confidence | 0.70 threshold |
| Draw thickness | 8 px |
| Erase radius | 40 px |
| Cursor smoothing | 7-frame weighted avg (controller) |
| Click cooldown | 20 frames @ 30fps ≈ 667ms |
| Canvas layers | 2 (camera feed + drawing canvas) |
| Blend method | Bitwise AND/ADD (zero-copy) |

---

## 🚀 Quick Start

### Option A — Browser (No Install)

Click below — it opens instantly in your browser:

[![Launch App](https://img.shields.io/badge/🚀%20Launch%20Air%20Writer-Live%20on%20HuggingFace-FF6F00?style=for-the-badge&labelColor=0d1117)](https://huggingface.co/spaces/Abdullah2894830/air-writer)

---

### Option B — Run Locally

```bash
# 1. Clone
git clone https://github.com/mabdullahab614-alt/air-writer.git
cd air-writer

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Air Writer (web UI)
python app.py
# → Open http://127.0.0.1:7860

# 5. OR launch PC Controller (desktop)
python controller.py
# → Press Q to quit
```

> **Note:** If you have TensorFlow installed system-wide, use the `venv` to avoid protobuf version conflicts.

---

## 📁 Project Structure

```
air-writer/
│
├── 📄 app.py              ← Gradio web app (Air Writer)
├── 📄 gradio_app.py       ← Alternate Gradio interface
├── 📄 controller.py       ← Desktop Air PC Controller
├── 📄 requirements.txt    ← Pinned dependencies
├── 📄 packages.txt        ← System libs for HF Spaces (OpenGL ES)
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named mediapipe` | Use the project venv, not system Python |
| Camera not showing | Allow browser camera permissions when prompted |
| Jerky drawing | Improve room lighting; keep hand centred |
| HF Space slow to start | First cold start downloads the 10MB model — wait 30s |
| Controller cursor jumps | Ensure only one hand is visible in frame |

---

## 🤝 Contributing

```bash
git checkout -b feature/your-idea
git commit -m "feat: your idea"
git push origin feature/your-idea
# → Open a Pull Request
```

**Ideas welcome:**
- Multi-hand support
- Shape snapping (circle, line, rectangle)
- SVG export
- Gesture-based color switching
- Mobile WebRTC support

---

## 📄 License

MIT — free to use, modify, and deploy.

---

<div align="center">

**Built by [Abdullah Javid](https://github.com/mabdullahab614-alt)**
BS Artificial Intelligence · UMT Lahore

[![Portfolio](https://img.shields.io/badge/Portfolio-Live-00f5ff?style=for-the-badge&labelColor=0d1117)](https://portfolio-website-jet-iota-21.vercel.app/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Abdullah2894830-FF6F00?style=for-the-badge&logo=huggingface&labelColor=0d1117)](https://huggingface.co/Abdullah2894830)
[![GitHub](https://img.shields.io/badge/GitHub-mabdullahab614--alt-181717?style=for-the-badge&logo=github&labelColor=0d1117)](https://github.com/mabdullahab614-alt)

<br/>

*"The best interface is no interface."*

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>
