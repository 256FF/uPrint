tool.py
=======

Python programm for dumping EEPROM.-


Test_DS2433.ino
===============

Reading EEPROM and converting content to HEX.

 // Typical structure on the EEPROM
    //        offset : len
    //        0x00   : 0x08 - Canister serial number (double) (part of the key, written *on* the canister as S/N)
    //        0x08   : 0x08 - Material type (double)
    //        0x10   : 0x14 - Manufacturing lot (string)
    //        0x24   : 0x02 - Version? (must be 1)
    //        0x28   : 0x08 - Manufacturing date (date yymmddhhmmss)
    //        0x30   : 0x08 - Use date (date yymmddhhmmss)
    //        0x38   : 0x08 - Initial material quantity (double)
    //        0x40   : 0x02 - Plain content CRC (uint16)
    //        0x46   : 0x02 - Crypted content CRC (uint16)
    //        0x48   : 0x08 - Key (unencrypted, 8 bytes)
    //        0x50   : 0x02 - Key CRC (unencrypted, uint16)
    //        0x58   : 0x08 - Current material quantity (double)
    //        0x60   : 0x02 - Current material quantity crypted CRC (unencrypted, uint16)
    //        0x62   : 0x02 - Current material quantity CRC (unencrypted, uint16)
