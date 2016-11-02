/*
DS2433 EEPROM
EEPROM 512byte(8bit*512byte) teble16(32byte*16table)
LASERE_ROM 8byte (8-Bit Family Code + 48-Bit Serial Number + 8-Bit CRC Tester)
Scratchpad 32byte(8bit*32byte)
==============================================================================
Typical structure on the EEPROM
    //        offset : length
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
*/

#include <OneWire.h>
OneWire ds(12); // 1-Wire connected with pin 12

int i,p,r;
byte data[512];
byte addr[8];

void setup(void) {
delay(1000);
Serial.begin(9600);
} 

void loop(void) {
/*Search for the Device*/
if ( !ds.search(addr)) {
Serial.println("Can not find the device");
ds.reset_search();
delay(5000);
return; //loop
}
/*DS2433　Show whether IC is correct family or not*/
if ( addr[0] == 0x23) {
Serial.println("This device is a DS2433 family device (Dimension, Fortus, ...)");
}
else if ( addr[0] == 0xB3) {
Serial.println("This device is a uPrint family device (uPrint, uPrint SE, HP DesignJet 3D");
}
else{
Serial.println("Unknown device found!");
/*return;*/
}
/*Display DS2433 Serial Number address, HEX*/
Serial.print("device address = ");
for( i = 0; i < 8; i++) {
Serial.print(addr[i], HEX);
Serial.print(" ");
}
/*Display if CRC for DS2433 is valid*/
if ( OneWire::crc8( addr, 7) != addr[7]) {
Serial.println("CRC is not valid!");
return;
}
Serial.println("");
Serial.println("");
delay(500);
/*Prep OK*/

/*Read and Display EEPROM Values (Calls function below)*/
read_eeprom();

delay(20000);

}

/* READ_EEPROM */
void read_eeprom(){
ds.reset();
ds.write(0xcc); //skip command
ds.write(0xf0); //eeprom read command
ds.write(0x00); //adrees
ds.write(0x00); //adrees

/* READ_EEPROM */
Serial.println("EEPROM DATA (512byte) =(");
for (int i = 0; i <= 511; i++) {
data[i] = ds.read();
}

/*Display*/
for (int i = 0; i <= 511; i++) {
if(data[i]<0x10)Serial.print(0);
Serial.print(data[i], HEX);
Serial.print(" ");
if(i%16==15){
Serial.println("");
} 
}
Serial.println(")HEX");
Serial.println(" ");
}
