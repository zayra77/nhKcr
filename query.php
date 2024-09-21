<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>nhKcr</title>
<link rel="stylesheet" type="text/css" href="style.css" media="screen" />
</head>
<body>
<div id="header">
	<div id="logo">
	<h1><a href="#">&nbsp;</a></h1>		
		<p>A predictor of crotonylation sites on nonhistone proteins<a href="#"></a></p>
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
<div id="page">
<?php
$filename=$_POST["T1"];
$filename=preg_replace('/\s/','',$filename);
$status="Submited";
$name_html="result.html";
if($filename==""){
	echo "<h1><span style=\"color:#FF0000\">Error ...</span></h1>&nbsp;<br />";
	echo "<br />Please input an <b>ID</b> inorder to query.";
	echo "<p>Click <strong><a href='./index.php'>here</a></strong> to returen.</p>";
}
else{
	if(file_exists("./public/$filename")){
		if(file_exists("./public/$filename/$name_html")){			
			header("Location: ./public/$filename/$name_html");
		}
		else{
			header("Location: ./waitting.php?value=$filename");
		}
	}
	else{
		echo "<h1><span style=\"color:#FF0000\">Sorry ...</span></h1>&nbsp;<br />";
		echo "<br />The job your query is not exist!";
		echo "<p>Click <strong><a href='./index.php'>here</a></strong> to return.</p>";
	}
}
?>
	
</div>
<!-- end #page -->
<div id="footer">
	<p>&copy; 2018. All Rights Reserved. Design by YZChen.<br />
</div>
<!-- end #footer -->
</body>
</html>


