<?php 
session_start();

// Database credentials
$servername = "localhost";
$username = "root";
$password = "";
$database = "travel_buddy";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// echo "Connected successfully";