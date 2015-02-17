<?php 
$db_hostname = 'localhost';
$db_database = 'hairgel';
$cwd = getcwd();
if ($cwd === "C:\\xampp\htdocs\hairgel") { // localhost
	$db_username = 'root';
	$db_password = '';
} else { // server
	$db_username = 'wangz10';
	$db_password = 'systemsbiology';
}

$db_server = mysql_connect($db_hostname, $db_username, $db_password);
if (!$db_server) die("Unable to connect to MySQL: " . mysql_error());
mysql_select_db($db_database)
or die("Unable to select database: " . mysql_error());

function sanitizeString($str){
	$str = strip_tags($str);
	$str = htmlentities($str);
	$str = stripslashes($str);
	return mysql_real_escape_string($str);
}

if (isset($_GET['gene'])) {
	$gene = sanitizeString($_GET['gene']);
	$query = "SELECT * FROM fpkms WHERE gene='$gene'";
	$out_array = array();

	$result = mysql_query($query);
	$row = mysql_fetch_assoc($result);
	
	$out_array['data'] = array();
	$samples = array('C6', 'C7', 'C8', 'C4', 'C1', 'C5', 'C3', 'C2');

	foreach ($samples as $sample) {
		$avg = $row["$sample".'_avg'];
		$sd = $row["$sample".'_sd'];
		array_push($out_array['data'], array('name' => $sample, 'avg' => $avg, 'sd' => $sd));
	}

	$query = "SELECT signature FROM signature WHERE gene='$gene'";
	$result = mysql_query($query);
	if ($result) {
		$signature = mysql_fetch_array($result)['signature'];
	} else {
		$signature = False;
	}	
	$out_array['signature'] = $signature;
	$out_array['gene'] = $row['gene'];

	echo json_encode($out_array);
}

mysql_close($db_server);
?>