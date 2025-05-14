# Smart IoT Parking Lot

## Project Overview
A full-stack IoT solution for real-time parking lot management using Raspberry Pi, ultrasonic sensors, LEDs, and a modern React dashboard. The system detects car presence in each slot, updates a web dashboard, and allows attendants to check in/out vehicles.
![Screenshot 2025-05-14 at 02 32 34](https://github.com/user-attachments/assets/c67cf8fa-081d-4d5c-8a8e-11fe119976a0)

---

## Hardware Requirements
- Raspberry Pi 4 Model B
- Half-size breadboard
- 5x HC-SR04 ultrasonic sensors
- 5x Red LEDs, 5x Green LEDs (20mA)
- Resistors: 330Ω (LEDs), 1kΩ + 2kΩ (voltage divider for ECHO)
- Jumper wires
- USB power supply for Pi

### Wiring Summary
- Each slot: 1 HC-SR04 sensor, 1 red LED, 1 green LED
- Use voltage divider on ECHO pin to protect Pi from 5V
- See report for detailed GPIO assignments and wiring diagram

---

## Software Requirements
- Python 3 (Raspberry Pi OS recommended)
- pip (Python package manager)
- Flask, flask-cors, RPi.GPIO, sqlite3
- Node.js & npm (for React dashboard)
- Git (optional, for cloning repo)

---

## Raspberry Pi Backend Setup
1. **Clone the repository** (or copy files to Pi):
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. **Install Python dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install flask flask-cors RPi.GPIO
   ```
3. **Connect hardware as per wiring diagram.**
4. **Run the backend API:**
   ```bash
   python3 parking_api.py
   ```
   The API will run on `http://<pi-ip>:5000`.

---

## React Dashboard (Frontend) Setup
1. **Navigate to the dashboard folder:**
   ```bash
   cd parking-dashboard
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Update the Pi IP address** in `src/App.js`:
   ```js
   const RASPBERRY_PI_URL = 'http://<pi-ip>:5000';
   ```
4. **Start the dashboard:**
   ```bash
   npm start
   ```
   The dashboard will open at `http://localhost:3000`.

---

## How to Run the System End-to-End
1. Power on the Raspberry Pi and ensure all sensors/LEDs are connected.
2. Start the backend API (`python3 parking_api.py`).
3. On your computer, start the React dashboard (`npm start` in `parking-dashboard`).
4. Access the dashboard in your browser. You should see real-time slot status and be able to check in/out vehicles.

---

## Troubleshooting
- **No data on dashboard:**
  - Check Pi IP address in `App.js`.
  - Ensure Pi and your computer are on the same network.
  - Check backend terminal for errors.
- **Sensor not detecting:**
  - Check wiring, especially voltage divider on ECHO.
  - Test sensor with a simple Python script.
- **LEDs not lighting:**
  - Check GPIO pin assignments and resistor values.
- **Port conflicts:**
  - Make sure nothing else is using port 5000 (backend) or 3000 (frontend).

---


## Contribution
See the report for team member contributions. PRs and suggestions welcome! 
