document.getElementById('prescription-form').addEventListener('submit', function(event) {
    let isValid = true;

    // Clear all errors
    document.querySelectorAll('.error').forEach(error => error.textContent = '');

    // Validate Patient Name
    const name = document.getElementById('patient-name').value.trim();
    if (name === '') {
        document.getElementById('name-error').textContent = 'Patient name is required.';
        isValid = false;
    }

    // Validate Patient Age
    const age = document.getElementById('patient-age').value.trim();
    if (age === '' || isNaN(age) || age <= 0) {
        document.getElementById('age-error').textContent = 'Valid patient age is required.';
        isValid = false;
    }

    // Validate Email
    const email = document.getElementById('patient-email').value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        document.getElementById('email-error').textContent = 'Valid email is required.';
        isValid = false;
    }

    // Validate Phone
    const phone = document.getElementById('patient-phone').value.trim();
    if (phone === '') {
        document.getElementById('phone-error').textContent = 'Phone number is required.';
        isValid = false;
    }

    // Validate Gender
    const gender = document.querySelector('input[name="gender"]:checked');
    if (!gender) {
        document.getElementById('gender-error').textContent = 'Gender selection is required.';
        isValid = false;
    }

    // Validate Diagnosis
    const diagnosis = document.getElementById('diagnosis').value.trim();
    if (diagnosis === '') {
        document.getElementById('diagnosis-error').textContent = 'Diagnosis is required.';
        isValid = false;
    }

    // Validate Prescription
    const prescription = document.getElementById('prescription').value.trim();
    if (prescription === '') {
        document.getElementById('prescription-error').textContent = 'Prescription is required.';
        isValid = false;
    }

    // Validate Certification
    const certification = document.getElementById('certification').checked;
    if (!certification) {
        document.getElementById('certification-error').textContent = 'You must certify the information.';
        isValid = false;
    }

    // Prevent form submission if validation fails
    if (!isValid) {
        event.preventDefault();
    }
});
