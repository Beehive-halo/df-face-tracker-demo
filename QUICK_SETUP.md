# DF Face Tracker — Quick Setup

This is the short setup/reference guide for the Raspberry Pi 3 A+ build and the macOS test version.

## 1. Raspberry Pi 3 A+ setup

### Hardware
- Raspberry Pi 3 A+
- Raspberry Pi camera supported by Picamera2
- Pimoroni Pan-Tilt HAT / compatible pan-tilt hardware
- Stable Raspberry Pi power supply
- Mac and Pi on the same local network if you want the browser stream

### Get the project

```bash
git clone https://github.com/Beehive-halo/df-face-tracker-demo.git
cd df-face-tracker-demo
git switch pi3a-optimized-rewrite
```

If you already cloned it:

```bash
cd df-face-tracker-demo
git fetch origin
git switch pi3a-optimized-rewrite
git pull
```

### Install Raspberry Pi packages

```bash
sudo apt update
sudo apt install -y git python3-picamera2 python3-opencv python3-venv
```

Create a virtual environment that can still see the Raspberry Pi OS Picamera2/OpenCV packages:

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Activate it again after a reboot/new terminal with:

```bash
cd df-face-tracker-demo
source .venv/bin/activate
```

### Check power first

```bash
python diagnostics.py
```

You can also run:

```bash
vcgencmd get_throttled
```

Best result:

```text
throttled=0x0
```

Fix undervoltage/throttling before enabling servos.

### First camera test

In `config.py`, keep:

```python
USE_SERVOS = False
ENABLE_STREAM = True
SHOW_PREVIEW = False
```

Run:

```bash
python main.py
```

The terminal prints a browser URL such as:

```text
http://raspberrypi.local:8000/
```

Open that on your Mac.

If `.local` does not work:

```bash
hostname -I
```

Then use the Pi address, for example:

```text
http://192.168.1.42:8000/
```

The stream shows:
- face box
- face centre
- TRACKING / SEARCHING
- FPS
- pan/tilt command
- viewer count

Default Pi settings are intentionally light:
- camera/processing: 320×240
- camera: 15 FPS
- Haar detection: every 3 frames
- browser stream: about 5 FPS
- stream JPEG quality: 65
- no JPEG encoding when nobody is viewing

### Servo test

Do this before automatic tracking:

```bash
python servo_test.py
```

The project uses:
- centre = `0`
- pan/tilt native convention = roughly `-90..90`
- conservative software limits to avoid mechanical binding

If the mount moves safely and centres properly, edit `config.py`:

```python
USE_SERVOS = True
```

If an axis is reversed:

```python
PAN_DIRECTION = -1
TILT_DIRECTION = 1
```

Change the wrong axis between `1` and `-1`.

### Useful Pi tuning

If streaming makes the Pi struggle:

```python
STREAM_FPS = 3
STREAM_JPEG_QUALITY = 55
```

If face detection is too slow:

```python
DETECTION_INTERVAL = 4
```

If tracking is too twitchy:
- lower `KP_PAN`
- lower `KP_TILT`
- lower `MAX_STEP`
- lower `SMOOTHING`

If tracking reacts too slowly, increase those values gradually.

Do not expose port `8000` to the public internet. The current stream has no password or encryption.

---

## 2. macOS test version

The Mac version tests the webcam, Haar face detection, overlays, and MJPEG browser streaming.

It does **not** use:
- Picamera2
- Raspberry Pi hardware
- Pan-Tilt HAT
- servos
- Raspberry Pi diagnostics

### Install

Open Terminal:

```bash
git clone https://github.com/Beehive-halo/df-face-tracker-demo.git
cd df-face-tracker-demo
git switch pi3a-optimized-rewrite
```

If you already have the repo:

```bash
cd df-face-tracker-demo
git fetch origin
git switch pi3a-optimized-rewrite
git pull
```

Create a Mac-only environment:

```bash
python3 -m venv .venv-mac
source .venv-mac/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-macos.txt
```

### Run it

```bash
python macos_test.py --open-browser
```

The script should:
1. open the Mac webcam
2. open an OpenCV preview window
3. detect faces using the same Haar settings as the Pi version
4. start the browser stream
5. open:

```text
http://127.0.0.1:8000/
```

Press `Q` or `Escape` in the OpenCV window to stop.

### macOS camera permission

The first run may ask for camera permission.

If the camera does not open:

**System Settings → Privacy & Security → Camera**

Enable camera access for the app you used to launch Python, such as Terminal, iTerm, or your IDE.

Then close and rerun the script.

### Different camera

If camera `0` is not the camera you want:

```bash
python macos_test.py --camera 1 --open-browser
```

Try `2`, etc. if necessary.

### Useful Mac test options

No browser stream:

```bash
python macos_test.py --no-stream
```

No local OpenCV window:

```bash
python macos_test.py --no-window
```

Different stream port:

```bash
python macos_test.py --port 8080 --open-browser
```

Then open:

```text
http://127.0.0.1:8080/
```

### What a successful Mac test proves

If the Mac version detects your face and the browser stream works, that confirms:
- the Haar cascade loads
- the detection code works
- the tracking overlay works
- MJPEG encoding works
- `stream.py` works
- the browser viewer works

It does **not** confirm:
- Picamera2 works on the Pi
- Pi camera wiring/configuration
- Pan-Tilt HAT installation
- servo directions
- Pi power stability

Those still need to be tested on the Raspberry Pi.

---

## 3. Normal test order

### Mac
```bash
source .venv-mac/bin/activate
python macos_test.py --open-browser
```

### Raspberry Pi
```bash
source .venv/bin/activate
python diagnostics.py
python main.py
python servo_test.py
```

Only after all three Pi tests work:

```python
USE_SERVOS = True
```

Then run:

```bash
python main.py
```
