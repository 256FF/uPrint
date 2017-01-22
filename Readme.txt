Arduino tool for reading uPrint/ HP DesignJet 3D EEPROMs
=======================================

Dumping Stratasys uPrint (SE) (PLUS) EEPROMs and DS2433 Chips from Stratasys Printers

1. Install the Arduino OneWire library from here:
   http://www.pjrc.com/teensy/td_libs_OneWire.html

2. Load the Arduino sketch and upload it.  

3. Wire up your arduino:

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

4. Use tool.py to dump the EEPROM - see folder pics

5. Use https://github.com/bvanheu/stratasys for decrypting the content - see folder pics
