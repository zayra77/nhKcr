<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>nhKCR result</title>
<link rel="stylesheet" type="text/css" href="style.css" media="screen" />
</head>
<body>
<div id="header">
	<div id="logo">
		<h1><a href="#">&nbsp;</a></h1>
		<p>A predictor of protein crotonylation sites<a href="#"></a></p>
	</div>
	<!-- end #logo -->
	<div id="menu">
		<ul>
			<li class="first"><a href="./index.php?page=introduction">Introduction</a></li>
			<li><a href="./index.php?page=prediction">Prediction</a></li>
			<li><a href="./index.php?page=help">Help</a></li>
            <li><a href="./index.php?page=download">Download</a></li>			
			<li><a href="./index.php?page=contact">Contact Us</a></li>
		</ul>
	</div>
	<!-- end #menu -->
</div>
<!-- end #header -->
<?php
// obtain the message on the page
$header="nhKCR Prediction";
$subject="nhKCR";
$message="Hi, guys:\n    Your sequence has been submited successfully!\nPlease wait! ... ";
?>
<div id="page1">
<?php
$baseDir = 'public/';
$showtime=date("YmdHis").'_'.make_char();
$currentTime=date('y-m-d H:i:s');
$workDir = $baseDir.$showtime;
$message = "";
$python3 = "/opt/anaconda3/bin/python ";

if (!file_exists($workDir)){
	// create work directory
	mkdir ($workDir,0777,true);

	// obtain sequences
	$sequences=$_POST["sequences"];
	$fileName = "sequence.txt";

	if($sequences != ""){
		$myFile = fopen($workDir.'/sequence.txt', 'w') or die("Unable to open file!");
		fwrite($myFile, $sequences);
		fclose($myFile);
	}


	if (!file_exists("$workDir/$fileName")){
		$message .= "Please paste protein sequences in fasta format! <br/>";
	}
	else{
		$fastaNumber = 0;
		$file_arr = file("$workDir/$fileName");

		for($i=0;$i<count($file_arr);$i++){
			if(substr($file_arr[$i], 0, 1)=='>'){
				$fastaNumber++;
			}
		}
		if($fastaNumber>100){
			$message.= "nhKCR web server was designed to accept at most 100 sequence at once.<br />";
		}
	}

	if($message != ""){
		echo "<h1><span style='color:#FF0000'>Error ...</span></h1>&nbsp;<br />";
		echo $message;
	}
	else{
		$cmd = $python3." nhKCR.py $showtime >/dev/null 2>&1 &";
		system($cmd);
		header("Location: waitting.php?value=$showtime");
	}
}
else {
	$message = "Could not create the working directory!";
}
?>
</div>
<!-- end #page -->
<div id="footer">
	<p>&copy; 2020 All Rights Reserved. Design by YZChen.<br />
</div>
<!-- end #footer -->
</body>
</html>
<?php
function make_char( $length = 8 ){
	$chars = array('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
	'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's',
	't', 'u', 'v', 'w', 'x', 'y','z', 'A', 'B', 'C', 'D',
	'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M', 'N', 'O',
	'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z',
	'0', '1', '2', '3', '4', '5', '6', '7', '8', '9');
	// 在 $chars 中随机取 $length 个数组元素键名
	$char_txt = '';
	for($i = 0; $i < $length; $i++){
	   // 将 $length 个数组元素连接成字符串
	   $char_txt .= $chars[array_rand($chars)];
	}
	return $char_txt;
}
?>