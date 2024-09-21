<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>nhKCR prediction result</title>
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
$jobid=$_GET["value"];
?>

<div id="page1">
<?php 
	$filename=$jobid;	
	$name_html="result.html";
	
	if(file_exists("./public/$filename/$name_html")){			
		header("Location: ./public/$filename/$name_html");
	}
	else{
		$status="Submited";
		if(file_exists("./public/$filename/SVM_test.seq")){
			$status="Running";
		}
		else{
			$status="Running";
		}		
			
		echo "<h3>Your Request has been Submitted: </h3><br />";
		echo '<table width="100%" border="0" cellspacing="0" cellpadding="0">';
		echo '<tr><td width="70" rowspan="2"><img src="./images/clock.gif" width="70" height="70"></td>';
		echo '<td width="50">&nbsp;</td>';
		echo "<td align=\"left\" valign=\"top\"><b>Job ID: </b><span style=\"color:#FF0000\">$filename</span></td></tr>";		
		echo "<tr><td width=\"50\">&nbsp;</td><td align=\"left\" valign=\"top\"><b>Status: </b>$status</td></tr>";			
		echo '</table>';			
		echo "<br /><br />";
		echo "The Request has been submitted to the queueing system and will run soon.<br />";			
		echo "<br />";
		echo "The result will be displayed in this page when done.  Please wait... ";
		header("refresh:5;url=waitting.php?value=$filename");			
	}
?>
	
</div>
<!-- end #page -->
<div id="footer">
	<p>&copy; 2021. All Rights Reserved. Design by YZChen.<br />
</div>
<!-- end #footer -->
</body>
</html>

