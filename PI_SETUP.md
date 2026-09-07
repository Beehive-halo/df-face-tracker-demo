# Raspberry Pi Setup


## 1. Get/update the project

Fresh install:

```bash
git clone https://github.com/Beehive-halo/df-face-tracker-demo.git
cd df-face-tracker-demo
git switch pi3a-optimized-rewrite
```

Already cloned:

```bash
cd df-face-tracker-demo
git fetch origin
git switch pi3a-optimized-rewrite
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

- camera image appears
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

## . Enable tracking

In `config.py` change:

```python
USE_SERVOS = True
```

Then run:

```bash
python main.py
```

If an axis moves the wrong way, swap that axis between `1` and `-1`:

```python
PAN_DIRECTION = -1
TILT_DIRECTION = 1
```

## 6. Next time

```bash
cd df-face-tracker-demo
source .venv/bin/activate
python main.py
```