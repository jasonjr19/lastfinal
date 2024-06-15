document.getElementById('uploadButton').addEventListener('click', function() {
    // Get user details
    const userName = document.getElementById('userName').value;
    const userAge = document.getElementById('userAge').value;
    const userPhone = document.getElementById('userPhone').value;
    
    // Get file inputs
    const passportFile = document.getElementById('passport').files[0];
    // Get other file inputs similarly
    
    // Check if any file is selected
    if (passportFile) {
        // Simulate file upload (in real scenario, you would send these files to a server)
        console.log("Uploading Passport:", passportFile.name);
        // Similar upload process for other files
        
        // Clear input fields after uploading
        document.getElementById('userName').value = '';
        document.getElementById('userAge').value = '';
        document.getElementById('userPhone').value = '';
        document.getElementById('passport').value = '';
        // Clear other input fields similarly
    } else {
        alert("Please select at least one document to upload.");
    }
});
