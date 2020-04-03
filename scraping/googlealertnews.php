<?php
/*

Author : Shafiq Mustapa
Email : sicksand@gmail.com / shafiq@sustento.my
File : googlealertnews.php
About : This script will read the downloaded xml file and put it in the db coronatracker
Google Alert RSS Feed : https://www.google.com/alerts/feeds/04291961558717184598/11230507918514212460
Date : 4th Feb 2020
*/

$servername = "localhost";
$username = "root";
$password = "password!^";
$table = "newsapi_local";

try {
    $conn = new PDO("mysql:host=$servername;dbname=coronatracker;charset=utf8;connect_timeout=15", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    //echo "Connected successfully";
    }
catch(PDOException $e)
    {
    //echo "Connection failed: " . $e->getMessage();
    }

// loop news
// Read the file from cron php file "crawler.php". the script will produce a xml file in json directory.
$path = "json/news.xml";

$xmlfile = file_get_contents($path);
//$xmldata = simplexml_load_file("json/news.xml") or die("Failed to load");

$new = simplexml_load_string($xmlfile);

$timestamp = date('Y-m-d H:i:s');

foreach ($new->entry as $news) {

	$title = $news->title;
	$description = $news->content;
	$author = $news->author->name;
	$url = substr($news->link['href'], 42);
	$url = strstr($url, '&', true);
	$content = $news->content;
	$urlToImage = 'https://image.thum.io/get/'.$url;
	$publishedAt = date("Y-m-d H:i:s", strtotime($news->published)) . "\n";
	$addedOn = date("Y-m-d H:i:s", strtotime($new->updated)). "\n";
	$siteName = parse_url($url);

	$title = addslashes((string)$title);
	$description = (string)$description;
	$author = (string)$author;
	$url = (string)$url;
	$content = (string)$content;
	$urlToImage = (string)$urlToImage;
	$publishedAt = (string)$publishedAt;
	$addedOn = (string)$addedOn;
	$siteName = (string)$siteName['host'];
	$language = "en";

	//echo "Title: ". $title."<br>Desc: ".$description."<br>author: ".$author."<br>Url: ".$url."<br>Content: ".$content ."<br>Image: ".$urlToImage ."<br>At: ".$publishedAt."<br><br>"; 
	// insert into mysql
	try {
		$query = "INSERT INTO newsapi_local (`title`,`description`,`author`,`url`,`content`,`urlToImage`,`publishedAt`,`addedOn`,`siteName`,`language`) VALUES ('$title','$description','$author','$url','$content','$urlToImage','$publishedAt','$addedOn','$siteName','$language')";
		// ON DUPLICATE KEY UPDATE (`addedOn`) VALUES ('$timestamp')	
		$conn->exec($query);

	} catch (PDOException $e) { 
	    die("ERROR: Could not able to execute $query. "
	            .$e->getMessage()); 
	} 
	
}

?>