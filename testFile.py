import RPi.GPIO as GPIO
import time

# Distance threshold in cm to detect a car
DIST_THRESHOLD = 10

# GPIO Pin Mapping
SLOTS = [
    {
        "TRIG": 23, "ECHO": 24,
        "GREEN_LED": 27, "RED_LED": 17
    },
    {
        "TRIG": 5, "ECHO": 6,
        "GREEN_LED": 13, "RED_LED": 22
    },
    {
        "TRIG": 2, "ECHO": 3,
        "GREEN_LED": 9, "RED_LED": 10
    },
    {
        "TRIG": 11, "ECHO": 8,
        "GREEN_LED": 7, "RED_LED": 25
    },
    {
        "TRIG": 20, "ECHO": 21,
        "GREEN_LED": 16, "RED_LED": 12
    }
]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup pins
for slot in SLOTS:
    GPIO.setup(slot["TRIG"], GPIO.OUT)
    GPIO.setup(slot["ECHO"], GPIO.IN)
    GPIO.setup(slot["GREEN_LED"], GPIO.OUT)
    GPIO.setup(slot["RED_LED"], GPIO.OUT)

def measure_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.05)  # Short delay to settle

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    timeout = start_time + 0.04  # 40 ms timeout

    # Wait for echo to go HIGH
    while GPIO.input(echo) == 0 and time.time() < timeout:
        start = time.time()

    if time.time() >= timeout:
        return 999  # Timeout (no object detected)

    # Wait for echo to go LOW
    timeout = time.time() + 0.04
    while GPIO.input(echo) == 1 and time.time() < timeout:
        end = time.time()

    if time.time() >= timeout:
        return 999  # Timeout again

    duration = end - start
    distance = (duration * 34300) / 2
    return distance

try:
    while True:
        for i, slot in enumerate(SLOTS, start=1):
            dist = measure_distance(slot["TRIG"], slot["ECHO"])
            print(f"Slot {i}: {dist:.1f} cm")

            if dist > DIST_THRESHOLD:
                # Slot free ? green on, red off
                GPIO.output(slot["GREEN_LED"], True)
                GPIO.output(slot["RED_LED"], False)
            else:
                # Slot occupied ? red on, green off
                GPIO.output(slot["GREEN_LED"], False)
                GPIO.output(slot["RED_LED"], True)

        time.sleep(1)

except KeyboardInterrupt:
    print("Cleaning up...")
    GPIO.cleanup()



