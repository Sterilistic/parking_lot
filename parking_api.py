import RPi.GPIO as GPIO
import time
import threading
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React app

# Distance threshold in cm to detect a car
DIST_THRESHOLD = 10

# GPIO Pin Mapping
SLOTS = [
    {"id": 1, "TRIG": 23, "ECHO": 24, "GREEN_LED": 27, "RED_LED": 17},
    {"id": 2, "TRIG": 5, "ECHO": 6, "GREEN_LED": 13, "RED_LED": 22},
    {"id": 3, "TRIG": 2, "ECHO": 3, "GREEN_LED": 9, "RED_LED": 10},
    {"id": 4, "TRIG": 11, "ECHO": 8, "GREEN_LED": 7, "RED_LED": 25},
    {"id": 5, "TRIG": 20, "ECHO": 21, "GREEN_LED": 16, "RED_LED": 12}
]

# Global state
parking_state = {slot["id"]: {"occupied": False, "distance": 0, "car_reg": None, "last_updated": datetime.now().isoformat()} for slot in SLOTS}

# Database setup
def init_db():
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_id INTEGER,
            car_registration TEXT,
            check_in_time TEXT,
            check_out_time TEXT,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('parking.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
init_db()

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
    time.sleep(0.05)
    
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    start_time = time.time()
    timeout = start_time + 0.04
    
    while GPIO.input(echo) == 0 and time.time() < timeout:
        start = time.time()
    
    if time.time() >= timeout:
        return 999
    
    timeout = time.time() + 0.04
    while GPIO.input(echo) == 1 and time.time() < timeout:
        end = time.time()
    
    if time.time() >= timeout:
        return 999
    
    duration = end - start
    distance = (duration * 34300) / 2
    return distance

def get_active_registration(slot_id):
    conn = get_db_connection()
    record = conn.execute(
        'SELECT car_registration FROM parking_records WHERE slot_id = ? AND status = "active"',
        (slot_id,)
    ).fetchone()
    conn.close()
    return record['car_registration'] if record else None

def monitor_sensors():
    while True:
        for slot in SLOTS:
            dist = measure_distance(slot["TRIG"], slot["ECHO"])
            occupied = dist <= DIST_THRESHOLD
            
            # Update LEDs
            GPIO.output(slot["GREEN_LED"], not occupied)
            GPIO.output(slot["RED_LED"], occupied)
            
            # Get car registration if occupied
            car_reg = get_active_registration(slot["id"]) if occupied else None
            
            # Update state
            parking_state[slot["id"]] = {
                "occupied": occupied,
                "distance": round(dist, 1),
                "car_reg": car_reg,
                "last_updated": datetime.now().isoformat()
            }
        
        time.sleep(1)

@app.route('/api/status')
def get_status():
    occupied_count = sum(1 for state in parking_state.values() if state["occupied"])
    free_count = len(SLOTS) - occupied_count
    
    return jsonify({
        "total_slots": len(SLOTS),
        "occupied": occupied_count,
        "free": free_count,
        "slots": parking_state,
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/slot/<int:slot_id>')
def get_slot(slot_id):
    if slot_id not in parking_state:
        return jsonify({"error": "Slot not found"}), 404
    return jsonify(parking_state[slot_id])

@app.route('/api/checkin', methods=['POST'])
def checkin():
    data = request.json
    slot_id = data.get('slot_id')
    car_registration = data.get('car_registration')
    
    if not slot_id or not car_registration:
        return jsonify({"error": "Slot ID and car registration required"}), 400
    
    if slot_id not in parking_state:
        return jsonify({"error": "Invalid slot ID"}), 400
    
    # Check if slot is actually free
    if parking_state[slot_id]["occupied"]:
        return jsonify({"error": "Slot is already occupied"}), 400
    
    # Check if car is already checked in somewhere
    conn = get_db_connection()
    existing = conn.execute(
        'SELECT slot_id FROM parking_records WHERE car_registration = ? AND status = "active"',
        (car_registration,)
    ).fetchone()
    
    if existing:
        conn.close()
        return jsonify({"error": f"Car already checked in at slot {existing['slot_id']}"}), 400
    
    # Create new parking record
    conn.execute(
        'INSERT INTO parking_records (slot_id, car_registration, check_in_time, status) VALUES (?, ?, ?, "active")',
        (slot_id, car_registration, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Check-in successful", "slot_id": slot_id, "car_registration": car_registration})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    slot_id = data.get('slot_id')
    
    if not slot_id:
        return jsonify({"error": "Slot ID required"}), 400
    
    if slot_id not in parking_state:
        return jsonify({"error": "Invalid slot ID"}), 400
    
    conn = get_db_connection()
    record = conn.execute(
        'SELECT * FROM parking_records WHERE slot_id = ? AND status = "active"',
        (slot_id,)
    ).fetchone()
    
    if not record:
        conn.close()
        return jsonify({"error": "No active parking record found for this slot"}), 400
    
    # Update record with checkout time
    conn.execute(
        'UPDATE parking_records SET check_out_time = ?, status = "completed" WHERE id = ?',
        (datetime.now().isoformat(), record['id'])
    )
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Check-out successful", "car_registration": record['car_registration']})

@app.route('/api/records')
def get_records():
    conn = get_db_connection()
    records = conn.execute(
        'SELECT * FROM parking_records ORDER BY check_in_time DESC LIMIT 50'
    ).fetchall()
    conn.close()
    
    return jsonify([dict(record) for record in records])

if __name__ == '__main__':
    # Start sensor monitoring in background thread
    sensor_thread = threading.Thread(target=monitor_sensors, daemon=True)
    sensor_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("Cleaning up...")
        GPIO.cleanup() 