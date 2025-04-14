# Gesture-Controlled YouTube & Virtual Mouse using Hand Tracking

This project allows you to **control YouTube** (like scrolling reels, playing/pausing videos, navigation) and also use your **right hand as a virtual mouse** to control the full laptop screen using gestures — all through your webcam!

## ✨ Features

- 🎥 Control YouTube using hand gestures:
  - Index finger up → Next reel
  - Index + Middle finger → Previous reel
  - All fingers open → Resume video
  - All fingers closed → Pause video
  - Thumb stretched left → Back page
  - Pinky stretched right → Forward page
  - Index finger up + hand lifted → Scroll up
  - Thumb + Index open wide → Scroll down
  - Thumb + Index close together → Pause/select video

- 🖱️ Virtual Mouse:
  - Move hand → Move mouse cursor
  - Pinch index + thumb → Left click
  - Index + middle pinch → Right click

- 📍 Full-screen resolution support

---

## 🛠️ Requirements

- Python 3.7 or higher
- Webcam

### Install dependencies

```bash
pip install opencv-python mediapipe pyautogui pygetwindow numpy
