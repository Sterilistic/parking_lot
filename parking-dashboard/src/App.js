import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const RASPBERRY_PI_URL = 'http://192.168.0.24:5000'; // Replace with your Pi's IP

function ParkingSlot({ slotId, slot, onCheckout }) {
  if (!slot) return <div className="parking-slot empty"></div>;
  return (
    <div className={`parking-slot ${slot.occupied ? 'occupied' : 'free'}`}>
      <div className="slot-header">
        <span className="slot-number">Slot {slotId}</span>
        <div className="distance">{slot.distance}cm</div>
      </div>
      {slot.occupied && (
        <div className="slot-details">
          <div className="car-reg">{slot.car_reg || 'Unknown'}</div>
          <button className="checkout-btn" onClick={() => onCheckout(parseInt(slotId))}>
            Check Out
          </button>
        </div>
      )}
    </div>
  );
}

function App() {
  const [parkingData, setParkingData] = useState({
    total_slots: 0,
    occupied: 0,
    free: 0,
    slots: {}
  });
  const [checkinForm, setCheckinForm] = useState({
    slot_id: '',
    car_registration: ''
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchParkingData = async () => {
      try {
        const response = await axios.get(`${RASPBERRY_PI_URL}/api/status`);
        setParkingData(response.data);
      } catch (error) {
        console.error('Error fetching parking data:', error);
      }
    };

    fetchParkingData();
    const interval = setInterval(fetchParkingData, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleCheckin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${RASPBERRY_PI_URL}/api/checkin`, {
        ...checkinForm,
        slot_id: parseInt(checkinForm.slot_id, 10)
      });
      setMessage(`✅ ${response.data.message}`);
      setCheckinForm({ slot_id: '', car_registration: '' });
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage(`❌ ${error.response?.data?.error || 'Check-in failed'}`);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const handleCheckout = async (slotId) => {
    try {
      const response = await axios.post(`${RASPBERRY_PI_URL}/api/checkout`, { slot_id: slotId });
      setMessage(`✅ Check-out successful for ${response.data.car_registration}`);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage(`❌ ${error.response?.data?.error || 'Check-out failed'}`);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const getAvailableSlots = () => {
    return Object.entries(parkingData.slots)
      .filter(([_, slot]) => !slot.occupied)
      .map(([slotId, _]) => slotId);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Parking Lot Dashboard</h1>
        <p className="subtitle">
          Real-time monitoring and management of parking slots. <br />
          <span className="legend">
            <span className="legend-box free"></span> Free &nbsp;
            <span className="legend-box occupied"></span> Occupied &nbsp;
            <span className="legend-box loading"></span> Loading Zone
          </span>
        </p>

        {/* Stats */}
        <div className="stats">
          <div className="stat-box">
            <h3>Total Slots</h3>
            <p>{parkingData.total_slots}</p>
          </div>
          <div className="stat-box free">
            <h3>Available</h3>
            <p>{parkingData.free}</p>
          </div>
          <div className="stat-box occupied">
            <h3>Occupied</h3>
            <p>{parkingData.occupied}</p>
          </div>
        </div>

        <div className="main-content">
        <div className="side-panel">
            <div style={{textAlign: 'center', marginBottom: 16}}>
              <span role="img" aria-label="car" style={{fontSize: 32}}>🚗</span>
            </div>
            {message && <div className="message">{message}</div>}
            <div className="checkin-form">
              <h2>Manual Vehicle Check-in</h2>
              <form onSubmit={handleCheckin}>
                <div className="form-group">
                  <label>Select Available Slot:</label>
                  <select
                    value={checkinForm.slot_id}
                    onChange={(e) => setCheckinForm({...checkinForm, slot_id: e.target.value})}
                    required
                  >
                    <option value="">Select a slot</option>
                    {getAvailableSlots().map(slotId => (
                      <option key={slotId} value={slotId}>Slot {slotId}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Car Registration Number:</label>
                  <input
                    type="text"
                    value={checkinForm.car_registration}
                    onChange={(e) => setCheckinForm({...checkinForm, car_registration: e.target.value.toUpperCase()})}
                    placeholder="ABC-1234"
                    required
                  />
                </div>
                <button type="submit" disabled={!checkinForm.slot_id || !checkinForm.car_registration}>
                  Check In
                </button>
              </form>
            </div>
          </div>
          <div className="parking-map">
            <div className="lane left-lane">
              <ParkingSlot slotId={2} slot={parkingData.slots[2]} onCheckout={handleCheckout} />
              <ParkingSlot slotId={4} slot={parkingData.slots[4]} onCheckout={handleCheckout} />
              <div className="loading-zone">Loading Zone</div>
              <div className="loading-zone">Loading Zone</div>
            </div>
            <div className="road">
              <div className="road-markings"></div>
            </div>
            <div className="lane right-lane">
              <ParkingSlot slotId={1} slot={parkingData.slots[1]} onCheckout={handleCheckout} />
              <ParkingSlot slotId={3} slot={parkingData.slots[3]} onCheckout={handleCheckout} />
              <ParkingSlot slotId={5} slot={parkingData.slots[5]} onCheckout={handleCheckout} />
              <div className="loading-zone">Loading Zone</div>
            </div>
          </div>
          
        </div>
      </header>
    </div>
  );
}

export default App; 