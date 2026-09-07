# DF Face Tracker Demo

A lightweight face-tracking camera demo designed specifically for a Raspberry Pi 3 A+ using Picamera2, OpenCV Haar detection, and a Pimoroni Pan-Tilt HAT.

## Design goals

- Low CPU use on Raspberry Pi 3 A+
- Low memory overhead
- Simple code that is easy to tune
- Safe optional servo control
- Stable tracking without constant servo chatter

The tracker runs the camera at 320x240 and 15 FPS by default. Haar face detection only runs every few frames, while the most recent target is reused briefly between scans. This avoids doing the most expensive OpenCV operation on every frame.

## Hardware

- Raspberry Pi 3 A+
- Raspberry Pi camera supported by Picamera2
- Pimoroni Pan-Tilt HAT / compatible pan-tilt hardware
- Adequate Raspberry Pi power supply

Servos can cause voltage drops. Fix any Raspberry Pi undervoltage warnings before enabling servo tracking.

## Install

Update Raspberry Pi OS first:

```bash
sudo apt update
sudo apt upgrade
```

Install Picamera2 and OpenCV from Raspberry Pi OS packages:

```bash
sudo apt install python3-picamera2 python3-opencv
```

Install the Pan-Tilt Python library if you are using the servos:

```bash
python3 -m pip install pantilthat
```

If your Raspberry Pi OS Python environment blocks system-wide pip installs, use the package/install method recommended for your Pan-Tilt HAT version instead.

## First test: camera only

Leave this in `config.py`:

```python
USE_SERVOS = False
```

Run:

```bash
python3 main.py
```

The default configuration is headless for lower CPU use. Set:

```python
SHOW_PREVIEW = True
```

if you want an OpenCV debug window with the detected face box.

## Power diagnostics

Run:

```bash
python3 diagnostics.py
```

or directly:

```bash
vcgencmd get_throttled
```

`throttled=0x0` means no current or recorded throttling flags were detected.

## Servo test

Before enabling automatic tracking, test the mount:

```bash
python3 servo_test.py
```

The project uses the Pimoroni angle convention:

- centre: `0`
- negative direction: down/left depending on mount orientation
- positive direction: up/right depending on mount orientation
- native range: roughly `-90` to `90`

The default software limits are intentionally smaller to reduce the chance of the bracket binding mechanically.

## Enable tracking

When camera detection and power are stable, change:

```python
USE_SERVOS = True
```

If an axis moves in the wrong direction, change its direction value in `config.py`:

```python
PAN_DIRECTION = -1
TILT_DIRECTION = 1
```

Swap either `1` and `-1` as required by your physical mount.

## Performance tuning

Important values in `config.py`:

- `FRAME_WIDTH` / `FRAME_HEIGHT`: processing resolution
- `CAMERA_FPS`: camera frame-rate cap
- `DETECTION_INTERVAL`: how often Haar detection runs
- `TARGET_HOLD_FRAMES`: how long the last detected target is kept
- `SHOW_PREVIEW`: disable for best performance
- `KP_PAN` / `KP_TILT`: tracking response speed
- `SMOOTHING`: target position filtering
- `SERVO_MIN_CHANGE`: minimum command change before another servo write

For the Raspberry Pi 3 A+, the defaults are intentionally conservative.

## Project structure

```text
main.py          main tracking loop
camera.py        Picamera2 capture
vision.py        Haar face detection
controller.py    smoothing and pan/tilt control
servos.py        Pan-Tilt HAT output
config.py        tuning and hardware settings
servo_test.py    manual servo movement test
diagnostics.py   Raspberry Pi power/throttling check
```

## Notes

The Haar cascade XML is included in the repository so the demo can run without downloading a model at startup.
