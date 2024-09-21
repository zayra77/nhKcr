<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>nhKCR Server</title>
<link rel="stylesheet" type="text/css" href="style.css" media="screen" />
</head>
<body>
<div id="header">
	<div id="logo">
		<h1><a href="#">&nbsp;</a></h1>		
		<p><br /><a href="#">A predictor of crotonylation sites on non-histone proteins</a></p>
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
	$page="prediction";
	if(isset($_GET['page'])){
		$page=$_GET['page'];
		if($page=='introduction'){
			include("./include/introduction.php");
		}
		if($page=='prediction'){
			include("./include/prediction.php");
		}
		if($page=='submit'){
			include("./include/submit.php");
		}
		if($page=='help'){
			include("./include/help.php");
		}
		if($page=='download'){
			include("./include/download.php");
		}
		if($page=='contact'){
			include("./include/contact.php");
		}		
	}
	else{
		include("./include/prediction.php");
	}	
?>

	<!-- end #content -->
	<div id="sidebar">
		<div id="sidebar-bgtop"></div>
		<div id="sidebar-content">
			<ul>				
                <li id="search">
					<h2><img src="./images/redball.png" width="12" height="12">&nbsp;&nbsp;Search Result</h2>
					<form action="query.php" method="post" enctype="multipart/form-data" name="form3" id="form3">
						<fieldset>
                        <ul><li><strong>Your job ID?</strong></li></ul>
                        Insert your job ID in the box to query your prediction result (e.g.20210203085650_z8XZxaoy).<br/><br />
						<strong>ID:</strong> <input type="text" name="T1" size="20" class="entryField">
						<br /><br />
                        <input name="submit1" type="submit" value="Query">&nbsp;&nbsp;
                        <input name="reset1" type="reset" value="Reset">
						</fieldset>
                        The result will be stored in our website for a month!
					</form>
                    
				</li>
				<li>
					<h2><img src="./images/redball.png" width="12" height="12">&nbsp;&nbsp;Who are using?</h2>
					<script type="text/javascript" src="//rf.revolvermaps.com/0/0/4.js?i=5s9ouw32ry1&amp;m=0&amp;h=128&amp;c=ff0000&amp;r=20" async="async"></script>
				</li>
			</ul>
		</div>
		<div id="sidebar-bgbtm"></div>
	</div>
	<!-- end #sidebar -->
</div>
<!-- end #page -->
<div id="footer">
	<p>&copy; 2018. All Rights Reserved. Design by YZChen.
</div>
<!-- end #footer -->
</body>
</html>


