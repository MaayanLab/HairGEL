<?php
list($_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW']) = 
  explode(':', base64_decode(substr($_SERVER['HTTP_AUTHORIZATION'], 6)));
if (!isset($_SERVER['PHP_AUTH_USER'])) {
	header("WWW-Authenticate: Basic realm=\"Private Area\"");
	header("HTTP/1.0 401 Unauthorized");
	print "Sorry - you need valid credentials to be granted access!\n";
	exit;
} else {
	$passwd = file_get_contents('password.conf', FILE_USE_INCLUDE_PATH);
	if (($_SERVER['PHP_AUTH_USER'] == 'rendllab') && ($_SERVER['PHP_AUTH_PW'] == $passwd)) {
		$doc = new DOMDocument();
		$doc->loadHTMLFile("P22.html");
		echo $doc->saveHTML();

	} else {
		header("WWW-Authenticate: Basic realm=\"Private Area\"");
		header("HTTP/1.0 401 Unauthorized");
		print "Sorry - you need valid credentials to be granted access!\n";
		exit;
	}
}
?>
