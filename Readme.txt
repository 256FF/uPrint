# Arduino tool for reading uPrint EEPROMs
Dumping Stratasys uPrint (SE) (PLUS) EEPROMs and other DS2433 Chips from Stratasys Printers

Install the Arduino OneWire library from here:
http://www.pjrc.com/teensy/td_libs_OneWire.html

Load the Arduino sketch, and upload it to your microcontroller.  

Wire up your arduino like so:

DataPin (D12)    Ard +5V     Ard GND
------------     -------   ---------- 
   |               |            |
   |     2.2k      |            |
   |----/\/\/\ -----            |
   |                            |
   |                            |
   |                            |
------------              ------------
OneWire Data              OneWire GND