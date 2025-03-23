// script.js
function simulateData() {
    // Generate random values for simulation
    const heartRate = Math.floor(Math.random() * (130 - 60 + 1)) + 60;
    const spo2 = Math.floor(Math.random() * (100 - 90 + 1)) + 90;
    const steps = Math.floor(Math.random() * 10000);
  
    // Update elements with the simulated data
    document.getElementById('heart-rate').textContent = `${heartRate} bpm`;
    document.getElementById('spo2').textContent = `${spo2} %`;
    document.getElementById('steps').textContent = `${steps} steps`;
  
    // Update statuses (example thresholds)
    document.getElementById('heart-rate-status').textContent = heartRate > 120 ? 'Critical' : 'Normal';
    document.getElementById('spo2-status').textContent = spo2 < 92 ? 'Critical' : 'Normal';
  
    // Optionally, add an alert if a value is critical
    if (heartRate > 120 || spo2 < 92) {
      addAlert(`Alert at ${new Date().toLocaleTimeString()}: ${heartRate > 120 ? 'High Heart Rate' : ''} ${spo2 < 92 ? 'Low SpO₂' : ''}`);
    }
  }
  
  function addAlert(message) {
    const alertsList = document.getElementById('alerts-list');
    const li = document.createElement('li');
    li.className = 'list-group-item';
    li.textContent = message;
    // Insert new alert at the beginning of the list
    alertsList.insertBefore(li, alertsList.firstChild);
  }
  
  // Simulate data every 5 seconds
  setInterval(simulateData, 5000);
  simulateData(); // Initial call to populate data immediately
