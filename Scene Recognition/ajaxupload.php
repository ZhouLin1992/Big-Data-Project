<?php

$valid_extensions = array('jpeg', 'jpg', 'png', 'gif', 'bmp'); // valid extensions
$path = 'uploads/'; // upload directory

if(isset($_FILES['image']))
{
	$img = $_FILES['image']['name'];
	$tmp = $_FILES['image']['tmp_name'];
		
	// get uploaded file's extension
	$ext = strtolower(pathinfo($img, PATHINFO_EXTENSION));
	
	// can upload same image using rand function
	$final_image = rand(1000,1000000).$img;
	
	// check's valid format
	if(in_array($ext, $valid_extensions)) 
	{					
		$path = $path.strtolower($final_image);	
			
		if(move_uploaded_file($tmp,$path)) 
		{
			//echo "<img src='$path' />";
		}
	} 
	else 
	{
		echo 'invalid';
	}
}

$content = shell_exec('/home/xinsongdu/anaconda2/bin/python /home/xinsongdu/Desktop/bigdata/project/data/predict2.py 2>&1');
//shell_exec('$command');
//echo $output;
//$logpath = '/var/www/html/jQuery_upload/log.txt';
//$content = @file_get_contents($logpath);
if($content){
	$str=substr($content,strpos($content,'*result*'));
	unlink($path);	
	echo $str;
}


?>
