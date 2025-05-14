# Smart IoT Parking Lot: End-to-End System from Raspberry Pi to Modern Dashboard

---

## Motivation

Parking inefficiency is a pervasive problem in urban environments, contributing to traffic congestion, increased emissions, and driver frustration. According to the INRIX 2017 Global Traffic Scorecard, drivers in the US spend an average of 17 hours per year searching for parking, costing $73 billion in time, fuel, and emissions [1]. In dense cities, up to 30% of traffic is caused by vehicles searching for parking [2]. This not only wastes resources but also exacerbates air pollution and reduces quality of life.

Traditional parking lots lack real-time visibility, making it difficult for both attendants and drivers to know which spaces are available. This inefficiency is a barrier to smart city initiatives and modern urban planning. As cities grow and mobility patterns change, there is a pressing need for scalable, data-driven parking solutions that can adapt to demand, reduce congestion, and improve user experience.

**Our motivation** is to build a smart, scalable, and user-friendly parking management system using IoT sensors, a Raspberry Pi, and a modern web dashboard. This system provides real-time slot status, check-in/check-out management, and a visual map, improving efficiency and user experience. Such a solution is valuable for commercial parking lots, smart cities, universities, and corporate campuses. With the rise of smart infrastructure, our system can be a key enabler for future mobility solutions, including dynamic pricing, reservation systems, and integration with navigation apps.

*References:*
1. INRIX Research, "Global Traffic Scorecard," 2017. [Link](http://inrix.com/scorecard/)
2. Shoup, D. (2005). The High Cost of Free Parking. Planners Press.
3. IBM Global Parking Survey, 2011.

---

## Technical Approach

Our system integrates hardware and software components to deliver a seamless smart parking experience. The design emphasizes modularity, scalability, and real-time responsiveness.

### System Architecture
- **Hardware Layer:**
  - **Raspberry Pi 4 Model B** as the central controller.
  - **Ultrasonic sensors (HC-SR04)** for each parking slot to detect vehicle presence.
  - **Red and green LEDs** for each slot to indicate availability.
  - **Physical model** with a central road, parking slots on both sides, and loading zones.
- **Software Layer:**
  - **Python (Flask) API** running on the Raspberry Pi, reading sensor data, controlling LEDs, and exposing REST endpoints.
  - **SQLite database** for persistent check-in/check-out records.
  - **React.js dashboard** for real-time visualization, manual check-in/out, and slot management.
  - **Responsive, modern UI** with a map matching the physical layout.
- **Communication:**
  - The dashboard fetches real-time data from the Pi over HTTP (local network).
  - CORS enabled for cross-device access.

### Data Flow
1. **Sensors** detect car presence and send signals to the Raspberry Pi via GPIO pins.
2. **Raspberry Pi** processes sensor data, updates slot status, and controls LEDs.
3. **Flask API** exposes endpoints for slot status, check-in, and check-out.
4. **React Dashboard** fetches data from the API and displays a real-time map and controls for attendants.
5. **Database** logs all check-in and check-out events for auditing and analytics.

### Design Decisions
- **Modularity:** Each slot is independently wired and managed, allowing for easy scaling.
- **Real-time Updates:** The dashboard polls the API every second for up-to-date status.
- **User Experience:** The dashboard map visually matches the physical model, reducing confusion for attendants.
- **Security:** CORS is enabled for local development; in production, authentication and HTTPS would be added.
- **Extensibility:** The system can be extended to support mobile apps, analytics dashboards, or integration with payment systems.

### Scalability & Future Extensions
- The architecture supports adding more slots by updating the SLOTS array and wiring additional sensors/LEDs.
- The backend can be containerized for deployment on larger infrastructure.
- Future work could include:
  - Mobile app for drivers
  - Dynamic pricing and reservation
  - Integration with city-wide traffic management
  - Predictive analytics for demand forecasting

### Circuit Diagram
*Insert circuit diagram or wiring photo here*

#### Wiring Overview (per slot)
- Breadboard + rail connects to Raspberry Pi Pin 2 (5V).
- Breadboard – rail connects to Raspberry Pi Pin 6 (GND).
- HC-SR04 VCC → + rail, GND → – rail, TRIG → assigned GPIO, ECHO → voltage divider → assigned GPIO.
- Red LED: Anode → 330Ω resistor → assigned GPIO, Cathode → – rail.
- Green LED: Anode → 330Ω resistor → assigned GPIO, Cathode → – rail.

#### GPIO Assignments

| Slot | TRIG | ECHO | GREEN_LED | RED_LED |
|------|------|------|-----------|---------|
|  1   |  23  |  24  |    27     |   17    |
|  2   |   5  |   6  |    13     |   22    |
|  3   |   2  |   3  |     9     |   10    |
|  4   |  11  |   8  |     7     |   25    |
|  5   |  20  |  21  |    16     |   12    |

*Insert close-up images of breadboard and GPIO connections here*

---

## Implementation Details

### Hardware
- **Raspberry Pi 4 Model B**
- **Half-size breadboard**
- **20mA red & green LEDs** (2.0–2.2V red, 3.0–3.2V green)
- **HC-SR04 ultrasonic sensors**
- **Jumper wires**
- **Resistors:** 330Ω for LEDs, 1kΩ + 2kΩ for voltage divider

#### Hardware Setup & Challenges
- Careful wiring was required to avoid cross-talk between sensors.
- Voltage dividers were used to protect the Pi from 5V ECHO signals.
- Breadboard layout was optimized for clarity and ease of debugging.
- LEDs were tested for correct polarity and brightness.
- The physical model was designed to match the dashboard for intuitive mapping.

### Software
- **Backend:**
  - Python 3, Flask, flask-cors, RPi.GPIO, sqlite3
  - Sensor monitoring in a background thread for real-time updates
  - REST API endpoints for status, check-in, check-out, and records
  - SQLite database for persistent storage and easy querying
  - Error handling for invalid input, timeouts, and sensor failures
- **Frontend:**
  - React.js (Create React App)
  - Axios for API requests
  - Responsive CSS for modern UI
  - Real-time polling for live updates
  - Modular components for slots, map, and forms

#### Database Schema
- **parking_records** table:
  - id (primary key)
  - slot_id (integer)
  - car_registration (text)
  - check_in_time (text)
  - check_out_time (text)
  - status (active/completed)

#### API Design
- `/api/status`: Returns all slot statuses
- `/api/checkin`: POST, records a car check-in for a slot
- `/api/checkout`: POST, records a car check-out
- `/api/records`: Returns recent check-in/out history

#### Frontend Component Structure
- **App.js**: Main dashboard logic and layout
- **ParkingSlot**: Visual representation of each slot
- **Check-in Form**: For manual entry by attendants
- **Stats & Legend**: For quick overview
- **Responsive Layout**: Side-by-side on desktop, stacked on mobile

#### Testing, Debugging, and Calibration
- Sensor readings were validated with known distances
- LEDs were tested for correct response to slot status
- API endpoints were tested with Postman and browser
- UI was tested on multiple devices and browsers

#### Deployment & Maintenance
- The backend runs as a service on the Raspberry Pi
- The frontend can be served locally or deployed to a web server
- System can be maintained by updating the SLOTS array and redeploying

### References & Citations
- [Flask Documentation](https://flask.palletsprojects.com/)
- [RPi.GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
- [React Documentation](https://react.dev/)
- [HC-SR04 Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [INRIX Global Traffic Scorecard](http://inrix.com/scorecard/)
- [The High Cost of Free Parking, Donald Shoup, 2005]
- [IBM Global Parking Survey, 2011]

---

## Results

- **Real-time Monitoring:**
  - Slot status updates instantly as cars enter/leave.
  - LEDs on the model reflect the dashboard state.
- **User Experience:**
  - Attendants can see available/occupied slots at a glance.
  - Manual check-in/out is simple and error-checked.
  - The dashboard map matches the physical layout, reducing confusion.
- **Reliability:**
  - System handles invalid input gracefully.
  - Database preserves all parking records for auditing.
- **Performance:**
  - API response time is typically <100ms on local network
  - Dashboard updates every second with no noticeable lag
- **Scalability:**
  - Easily extendable to more slots or features (e.g., user-facing mobile app, analytics).
- **Impact:**
  - Demonstrates the feasibility of low-cost, scalable smart parking
  - Can be commercialized or used as a research platform for smart city solutions

### Limitations & Future Work
- **Limitations:**
  - Sensor accuracy can be affected by environmental noise
  - System currently works on local network; remote access would require additional security
  - No user-facing mobile app yet
- **Future Work:**
  - Add predictive analytics for demand forecasting
  - Integrate with payment and reservation systems
  - Develop a mobile app for drivers
  - Add camera-based license plate recognition

### Lessons Learned
- **Challenges:**
  - Ensuring reliable sensor readings in a noisy environment
  - Handling type mismatches between frontend and backend (e.g., slot_id as string vs integer)
  - UI/UX design for clarity and usability
  - Debugging hardware and software integration
- **What Went Wrong:**
  - Occasional sensor misreads required additional debouncing logic
  - Network issues when Pi and dashboard were not on the same subnet
- **Takeaway:**
  - The project demonstrates a robust, extensible IoT solution for smart parking, with real-world applicability and room for further innovation.

*Insert before/after images, demo screenshots, and any data/graphs if available*

---

## Contribution

This project was completed by a team of three members:
- **Member 1:** Hardware wiring, sensor integration, Raspberry Pi setup, and physical model construction. Led the design and testing of the sensor circuits, and contributed to debugging hardware issues.
- **Member 2:** Backend API development, database integration, and system architecture. Implemented the Flask API, designed the database schema, and ensured robust error handling and data integrity.
- **Member 3:** Frontend dashboard design, React implementation, and UI/UX. Developed the dashboard layout, implemented real-time data fetching, and optimized the user experience for attendants.

All members contributed to testing, debugging, and documentation. The project would not have been possible without the collaborative effort of the entire team. Regular meetings, code reviews, and shared troubleshooting sessions ensured a smooth workflow and high-quality results.

*Insert team photo or collaboration screenshot here* 