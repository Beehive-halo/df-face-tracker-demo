# Raspberry Pi Setup

## 1. Get/update the project

Fresh install:

```bash
git clone https://github.com/Beehive-halo/df-face-tracker-demo.git
cd df-face-tracker-demo
git switch df-rewrite
```

Already cloned:

```bash
cd df-face-tracker-demo
git fetch origin
git switch df-rewrite
git pull
```

## 2. Install everything

```bash
sudo apt update
sudo apt install -y git python3-picamera2 python3-opencv python3-venv

python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 3. Test camera + browser stream

In `config.py`, make sure:

```python
USE_SERVOS = False
ENABLE_STREAM = True
SHOW_PREVIEW = False
CAMERA_HFLIP = True
CAMERA_VFLIP = True
```

Run:

```bash
python main.py
```

On your Mac, open the URL printed by the Pi. Usually:

```text
http://raspberrypi.local:8000/
```

If that does not work, on the Pi run:

```bash
hostname -I
```

Then open:

```text
http://PI-IP-ADDRESS:8000/
```

Check that:

- the camera image is upright
- your face gets a box
- `TRACKING` appears when your face is found
- FPS is updating

Stop with `Ctrl+C`.

## 4. Test servos

Run:

```bash
python servo_test.py
```

Make sure:

- both axes move
- movement is safe
- it returns to centre

## 5. Enable tracking

In `config.py` change:

```python
USE_SERVOS = True
```

Then run:

```bash
python main.py
```

The upside-down camera defaults are:

```python
PAN_DIRECTION = 1
TILT_DIRECTION = -1
```

If one axis moves away from your face, stop the program and swap only that axis between `1` and `-1`.

## 6. Check Pi health

```bash
python diagnostics.py
```

This reports CPU temperature, available memory, and power/throttling warnings. The best throttling result is `throttled=0x0`.

## 7. Next time

```bash
cd df-face-tracker-demo
source .venv/bin/activate
python main.py
```
