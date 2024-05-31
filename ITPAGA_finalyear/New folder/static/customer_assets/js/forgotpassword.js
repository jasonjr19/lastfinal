function validateForgotPasswordForm() {
    var email = document.getElementById("email").value;
  
    // Regular expression for email validation
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
    if (email == "") {
      alert("Please enter your email address");
      return false;
    }
  
    if (!emailRegex.test(email)) {
      alert("Please enter a valid email address");
      return false;
    }
  
    return true;
  }
  