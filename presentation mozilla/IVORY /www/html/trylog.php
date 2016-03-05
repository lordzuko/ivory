<?php
$user= $_POST[username];
$pass= $_POST[password];

if($user=='admin' and  $pass=='kremlin'){
	 
	Include('Dashboard.html');
}
else {
	echo "Try Again";
	Include('login.php');
}

?>
