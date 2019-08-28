<?php
//Info for connection to server
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "test";

//Create connection
$conn = new mysqli($servername,$username,$password,$dbname);

//Check 
if($conn -> connect_error) { 
    print("connection failed: ". $conn->connect_error);
}

$sql = "SELECT * FROM repositories";
$result = $conn->query($sql);

if($result->num_rows > 0){
    echo "<div id = 'Repos'><ul>";
    while($row = $result->fetch_assoc()){
        echo "<li><h3><a href= '". $row["RepoURL"]."'>".$row["RepoName"]. " </a></h3>". $row["RepoDesc"] . "</li>";
    }
    echo "</ul></div>";
}


?>