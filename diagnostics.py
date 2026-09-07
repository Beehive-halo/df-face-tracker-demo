import subprocess


def get_throttled():
    try:
        result = subprocess.run(
            ["vcgencmd", "get_throttled"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    text = result.stdout.strip()
    try:
        value = int(text.split("=", 1)[1], 16)
    except (IndexError, ValueError):
        return None

    return value


def main():
    value = get_throttled()

    if value is None:
        print("Could not read Raspberry Pi throttling state.")
        return

    print(f"throttled=0x{value:x}")

    flags = [
        (0x1, "Undervoltage is happening now"),
        (0x2, "CPU frequency is capped now"),
        (0x4, "System is throttled now"),
        (0x8, "Soft temperature limit is active now"),
        (0x10000, "Undervoltage has happened since boot"),
        (0x20000, "CPU frequency capping has happened since boot"),
        (0x40000, "Throttling has happened since boot"),
        (0x80000, "Soft temperature limit has happened since boot"),
    ]

    active = [message for bit, message in flags if value & bit]

    if not active:
        print("No power or throttling warnings detected.")
        return

    for message in active:
        print(f"- {message}")


if __name__ == "__main__":
    main()
