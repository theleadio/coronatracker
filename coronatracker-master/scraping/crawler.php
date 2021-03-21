<?php

/*

Author : Shafiq Mustapa
Email : sicksand@gmail.com / shafiq@sustento.my
File : crawler.php
About : This script read the rss and pump it into a xml file
Date : 4th Feb 2020

*/

$url = 'https://www.google.com/alerts/feeds/04291961558717184598/11230507918514212460';

$response = file_get_contents($url);

$fp = fopen('json/news.xml', 'w');

fwrite($fp, $response);
fclose($fp);