function validateForm() {
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;
    var gender = document.getElementById("gender").value;
    var password = document.getElementById("psw").value;
    var confirmPassword = document.getElementById("confirmPsw").value;
  
    // Regular expression for email validation
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
    // Regular expression for phone number validation (10 digits)
    var phoneRegex = /^\d{10}$/;
  
    if (firstName == "" || lastName == "" || email == "" || phone == "" || gender == "" || password == "" || confirmPassword == "") {
      alert("All fields are required");
      return false;
    }
  
    if (!emailRegex.test(email)) {
      alert("Please enter a valid email address");
      return false;
    }
  
    if (!phoneRegex.test(phone)) {
      alert("Please enter a valid phone number (10 digits)");
      return false;
    }
  
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return false;
    }
  
    return true;
  }
  