<?php 
include "qrlib.php";
$data = '123456';
// 发送合适的报头
//header("Content-Type: image/jpeg;text/html; charset=utf-8");
// 发送图片
$errorCorrectionLevel = 'L';
$matrixPointSize = 4;
QRcode::png($data, false, $errorCorrectionLevel, $matrixPointSize, 2);  
exit;