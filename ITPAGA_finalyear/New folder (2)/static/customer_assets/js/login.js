function validateForm() {
    var emailOrPhone = document.getElementById("email").value;
    var password = document.getElementById("psw").value;
  
    // Regular expression for email validation
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
    // Regular expression for phone number validation (10 digits)
    var phoneRegex = /^\d{10}$/;
  
    if (emailOrPhone == "" || password == "") {
      alert("Both email/phone and password are required");
      return false;
    }
  
    // Validate whether the input is an email or a phone number
    if (!(emailRegex.test(emailOrPhone) || phoneRegex.test(emailOrPhone))) {
      alert("Please enter a valid email or phone number");
      return false;
    }
  
    return true;
  }
  