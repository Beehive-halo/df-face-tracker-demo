# DF Face Tracker — Quick Setup

## Get the project

```bash
git clone https://github.com/Beehive-halo/df-face-tracker-demo.git
cd df-face-tracker-demo
git switch df-rewrite
```

Already cloned?

```bash
cd df-face-tracker-demo
git fetch origin
git switch df-rewrite
git pull
```

---

## macOS test

### Install

```bash
python3 -m venv .venv-mac
source .venv-mac/bin/activate
python -m pip install -r requirements-macos.txt
```

### Run

```bash
python macos_test.py --open-browser
```

It should open your webcam and the browser stream at:

```text
http://127.0.0.1:8000/
```

Press `Q` or `Escape` to stop.

If the camera will not open, allow Terminal or your IDE under **System Settings → Privacy & Security → Camera**.

Try another camera with:

```bash
python macos_test.py --camera 1 --open-browser
```

---

## Raspberry Pi 3 A+

### Install

```bash
sudo apt update
sudo apt install -y git python3-picamera2 python3-opencv python3-venv

python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Check power, temperature, and memory

```bash
python diagnostics.py
```

Best throttling result:

```text
throttled=0x0
```

### Test camera + Mac stream

Keep this in `config.py`:

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

On your Mac, open the URL printed by the Pi, usually:

```text
http://raspberrypi.local:8000/
```

If that does not work, run `hostname -I` and open `http://PI-IP-ADDRESS:8000/`.

### Test servos

```bash
python servo_test.py
```

If everything moves safely, change:

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

If an axis moves away from your face, stop the program and reverse only that axis.

---

## Next time

### Mac

```bash
cd df-face-tracker-demo
source .venv-mac/bin/activate
python macos_test.py --open-browser
```

### Pi

```bash
cd df-face-tracker-demo
source .venv/bin/activate
python main.py
```

Do not expose port `8000` directly to the public internet.
