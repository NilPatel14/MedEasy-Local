
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


        document.getElementById('sendOtpButton').addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the form from submitting
        
            let email = document.getElementsByName('email')[0].value; // Get email value from the form
        
            // Make an AJAX request to Django to send the OTP
            fetch('/send-otp/', { // Use the correct URL for your Django view
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // If you're using JSON
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // CSRF token
                },
                body: JSON.stringify({ email: email }) // Send the email in JSON body
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('OTP sent successfully!');
                    alert(data.message); // Optional: Show success message to the user
                } else {
                    console.log('Error:', data.message);
                    alert(data.message); // Optional: Show error message
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
        
        document.getElementById("sendOtpButton").addEventListener("click", function() {
            // Show overlay
            const overlay = document.getElementById("overlay");
            overlay.classList.add("active");
        
            // Simulate async operation (e.g., sending OTP via AJAX)
            setTimeout(() => {
              overlay.classList.remove("active"); // Hide overlay after the operation
            }, 3000); // Replace with actual AJAX success callback
          });

