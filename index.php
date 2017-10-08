<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>This is the first website</title>
	</head>
	<body>
		<?php
		$python_file = shell_exec("python pyfolder/file_2.py");
		echo $python_file;
		 ?>
	</body>
</html>
