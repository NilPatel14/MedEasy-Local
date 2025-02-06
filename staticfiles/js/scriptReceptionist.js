const ctx = document.getElementById('patientChart').getContext('2d');
    const patientChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['IPD', 'OPD'],
            datasets: [{
                label: 'Patient Distribution',
                data: [40, 60], // Adjust IPD and OPD data as needed
                backgroundColor: [' #FFC0CB', '#ADD8E6'], // 
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });
document.addEventListener("DOMContentLoaded", function () {
            const calendarIcon = document.getElementById("calendarIcon");
            const datePicker = document.getElementById("datePicker");

            // When the calendar icon is clicked, open the date picker
            calendarIcon.addEventListener("click", function () {
                datePicker.focus();
            });

            // When a date is selected, display the selected date (optional)
            datePicker.addEventListener("change", function () {
                alert("You selected: " + this.value);
            });
        });

