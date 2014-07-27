<?php

include "php_serial.class.php";

// Let's start the class

$serial = new phpSerial;

// First we must specify the device. This works on both linux and windows (if
// your linux serial device is /dev/ttyS0 for COM1, etc)

$serial->deviceSet("/dev/ttyS0");
$serial->confBaudRate(19200);

// Then we need to open it
$serial->deviceOpen();

// To write into
$serial->sendMessage("AT+cmgf=1;+cnmi=2,1,0,1,0\r");
// Wait and read from the port
$read = $serial -> readPort();

// construct the msg and send it
$serial->sendMessage("at+cmgs=\"+256782847346\"\r\n");
$serial->sendMessage("this is a text message from *****\r\n");
$serial->sendMessage(chr(26));
// Wait and read from the port
sleep(5);
$read=$read . $serial->readPort();

//wait for modem to send message
sleep(7);
$read=$read . $serial->readPort();

$serial->deviceClose();

// We can change the baud rate
// etc...

echo $read;
?>