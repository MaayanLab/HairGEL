<?php 
$db_database = 'hairgel';
$cwd = getcwd();
if ($cwd === "C:\\xampp\htdocs\hairgel" || $cwd === "/Users/zichen/Documents/bitbucket/hairgel" || $cwd === "/Library/WebServer/Documents/hairgel") { // localhost
	$db_hostname = 'localhost';
	$db_username = 'root';
	$db_password = '';
} else { // server
	$db_hostname = 'rendllabinfo.mydomaincommysql.com';
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

if (isset($_GET['table'])) {
	$table = $_GET['table'];
} else { // default for $table
	$table = 'fpkms';
}

if (isset($_GET['gene'])) {
	$gene = sanitizeString($_GET['gene']);
}

switch ($table) {
	case 'fpkms2':
		$samples = array('X1','X2','X3','X4','X5','X6','X7','X8','X13','X14','X16','X17','X19','X20');
		$signature_table = 'signature2';
		$query = "SELECT * FROM $table WHERE gene='$gene'";
		break;
	case 'fpkms_all':

		$samples = array('C6', 'C7', 'C8', 'C4', 'C1', 'C5', 'C3', 'C2',
			'X1','X2','X3','X4','X5','X6','X7','X8','X13','X14','X16','X17','X19','X20',
			'DS', 'DP', 'DF');
		$signature_table = 'signature2';
		$query = "SELECT * FROM fpkms JOIN fpkms2 ON fpkms.gene=fpkms2.gene JOIN fpkms3 ON fpkms2.gene=fpkms3.gene WHERE fpkms.gene='$gene'";		
		break;
	default:
		$samples = array('C6', 'C7', 'C8', 'C4', 'C1', 'C5', 'C3', 'C2');
		$signature_table = 'signature';
		$query = "SELECT * FROM $table WHERE gene='$gene'";
		break;
}


$out_array = array();

$result = mysql_query($query);
$row = mysql_fetch_assoc($result);

$out_array['data'] = array();

foreach ($samples as $sample) {
	$avg = $row["$sample".'_avg'];
	$sd = $row["$sample".'_sd'];
	array_push($out_array['data'], array('name' => $sample, 'avg' => $avg, 'sd' => $sd));
}

$query2 = "SELECT signature FROM $signature_table WHERE gene='$gene'";
$result2 = mysql_query($query2);
$signature = mysql_fetch_assoc($result2);
$out_array['signature'] = $signature['signature'];
$out_array['gene'] = $row['gene'];

echo json_encode($out_array);

mysql_close($db_server);
?>