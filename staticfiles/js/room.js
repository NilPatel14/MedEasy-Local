document.getElementById("reservationForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const patientName = document.getElementById("patientName").value;
  const checkIn = document.getElementById("checkin").value;
  const roomNo = document.getElementById("roomNo").value;
  const roomType = document.getElementById("roomType").value;
  const bedNo = document.getElementById("bedNo").value;

  alert(`Reservation Details:\n\nPatient Name: ${patientName}\nCheck In: ${checkIn}\nRoom No: ${roomNo}\nRoom Type: ${roomType}\nBed No: ${bedNo}`);
});

// Room and Bed Data for Chart.js
const roomData = {
  labels: ['Occupied Rooms', 'Unoccupied Rooms'],
  datasets: [{
    label: 'Room Status',
    data: [12, 5], // Replace with actual data
    backgroundColor: ['#ff6347', '#f4a460'],
    borderColor: ['#d9534f', '#f0ad4e'],
    borderWidth: 1
  }]
};

const bedData = {
  labels: ['Occupied Beds', 'Unoccupied Beds'],
  datasets: [{
    label: 'Bed Status',
    data: [15, 8], // Replace with actual data
    backgroundColor: ['#ff6347', '#f4a460'],
    borderColor: ['#d9534f', '#f0ad4e'],
    borderWidth: 1
  }]
};

// Room Chart
const ctxRoom = document.getElementById('roomChart').getContext('2d');
new Chart(ctxRoom, {
  type: 'bar',
  data: roomData,
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      tooltip: { backgroundColor: '#333' }
    },
    scales: {
      x: { beginAtZero: true },
      y: { beginAtZero: true }
    }
  }
});

// Bed Chart
const ctxBed = document.getElementById('bedChart').getContext('2d');
new Chart(ctxBed, {
  type: 'bar',
  data: bedData,
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      tooltip: { backgroundColor: '#333' }
    },
    scales: {
      x: { beginAtZero: true },
      y: { beginAtZero: true }
    }
  }
});
