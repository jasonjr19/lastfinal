<?php 
  require 'config.php';
  if(isset($_POST["submit"])) {

  $email = $_POST["email"];
  $pass = $_POST["pass"]; 

  // Prepared statement to prevent SQL injection
  $stmt = $conn->prepare("SELECT * FROM `admin` WHERE email = ? ;");
  $stmt->bind_param("s", $email);
  $stmt->execute();
  $result = $stmt->get_result();

  if(mysqli_num_rows($result) > 0) {
    echo "Entered Password: " . $pass . "<br>";
    echo "Hashed Password from DB: " . $row["pass"] . "<br>";
        
      $row = mysqli_fetch_assoc($result);
      // if($_SESSION['login'] === true ){
      //   header("location: ../index.php");
      // }
      // else{
      if($pass === $row["pass"]) { // Assuming pass is hashed in the database
          $_SESSION["login"] = true;
          $_SESSION["admin_id"] = $row["admin_id"];
          echo $row['admin_id'];
          header("location: ../index.php");
          // exit(); // Make sure to exit after redirection
      } else {
          echo "<script> alert('Incorrect password'); </script>";
      }
  } else {
      echo "<script> alert('Email not registered'); </script>";
  }
}

?>


<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Travel Buddy Admin</title>
    <!-- plugins:css -->
    <link rel="stylesheet" href="../template/assets/vendors/mdi/css/materialdesignicons.min.css">
    <link rel="stylesheet" href="../template/assets/vendors/css/vendor.bundle.base.css">
    <link rel="stylesheet" href="../template/assets/css/style.css">
    <!-- End layout styles -->
    <link rel="shortcut icon" href="../template/assets/images/favicon.png" />
  </head>
  <body>
    <div class="container-scroller">
      <div class="container-fluid page-body-wrapper full-page-wrapper">
        <div class="row w-100 m-0">
          <div class="content-wrapper full-page-wrapper d-flex align-items-center auth login-bg">
            <div class="card col-lg-4 mx-auto">
              <div class="card-body px-5 py-5">
                <h3 class="card-title text-left mb-3">Login</h3>
                <form action="./login.php" method="POST">
                  <div class="form-group">
                    <label>Email</label>
                    <input type="text" class="form-control p_input" name="email" id="email">
                  </div>
                  <div class="form-group">
                    <label>Password</label> 
                    <input type="password" class="form-control p_input" name="pass" id="pass">
                  </div>
                  <!-- <div class="form-group d-flex align-items-center justify-content-between">
                    <a href="#" class="forgot-pass">Forgot password</a>
                  </div> -->
                  <div class="text-center">
                    <button type="submit" name="submit" id="submit" class="btn btn-primary btn-block enter-btn">Log in</button>
                  </div>
                  <p class="sign-up">Don't have an Account?<a href="./register.html"> Sign Up</a></p>
                </form>
              </div>
            </div>
          </div>
          <!-- content-wrapper ends -->
        </div>
        <!-- row ends -->
      </div>
      <!-- page-body-wrapper ends -->
    </div>
    <!-- container-scroller -->
    <!-- plugins:js -->
    <script src="../template/assets/vendors/js/vendor.bundle.base.js"></script>
    <!-- endinject -->
    <!-- Plugin js for this page -->
    <!-- End plugin js for this page -->
    <!-- inject:js -->
    <script src="../template/assets/js/off-canvas.js"></script>
    <script src="../template/assets/js/hoverable-collapse.js"></script>
    <script src="../template/assets/js/misc.js"></script>
    <script src="../template/assets/js/settings.js"></script>
    <script src="../template/assets/js/todolist.js"></script>
    <!-- endinject -->
  </body>
</html>