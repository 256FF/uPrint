#!/usr/bin/python
# tool.py forked from @meawoppl
# edited COM-Port for Windows
# changed re-read to 2x
# changed spleep time to 2s

import argparse, subprocess, sys, os
import serial, time, binascii, os

parser = argparse.ArgumentParser(description='These are some simple scripts to interface a oneWire eeprom to a computer using a arduino Mirror..')

parser.add_argument("-s", "--save", help="Save the eeprom to disk. (Default action)", action="store_true")
parser.add_argument("-l", "--load", help="Restore the eeprom to the oldest available image.", action="store_true")
parser.add_argument("-t", "--test", help="Test eeprom (and arduino/connections etc).", action="store_true")
parser.add_argument("-c", "--clear", help="Clear the flash write all zeros.")

def readROM():
    sp.write("r")
    return sp.read(8) #original 9

def readFlash():
    sp.flushInput()
    sp.write("f")
    # return sp.read(512)     # 512 for Dimension (DS2433); 128 for uPrint(SE)(+) / HP Clone
    return sp.read(128)   # 128 for uPrint(SE)(+) / HP Clone

def pollForChip():
    sp.write("x")
    return sp.read(1) == "p"

def waitForChip():
    while True:
        print "Polling for chip. . ."
        if pollForChip(): break
        time.sleep(2.0) #original was 0.5
    print "\t found!"

    # Flush the serial port!
    sp.flushInput()


def echo():
    print "ping. . .",
    sp.write("e")
    if sp.read() != "e":
        print "No echo :("
    else:
        print "pong! (success)"
def getPathForRom(rom):
    return os.path.join("flash-dumps", binascii.hexlify(rom))

def dump2433():
    waitForChip()

    # Read the ROM.  echo its hex
    rom = readROM()
    print(binascii.hexlify(rom) + " (" + str(len(rom)) + ")")

    # Read it 2x and make sure they all match
    # for reread in range(2): assert rom == readROM(), "Mismatched ROM read.  Aborting"

    # Read the flash
    flash = readFlash()
    print("Flash Read: %i bytes" % len(flash))

    # Read it 2x and make sure they all match
    #for reread in range(2): assert flash == readFlash(), "Mismatched flash read.  Aborting"

    # Make a path to store the dumped data
    fPath = getPathForRom(rom)
    if not os.path.isdir(fPath): os.makedirs(fPath)

    # Mark them by the time, so we can reload the oldest one later
    fullNamePath = os.path.join(fPath, str(time.time()) + ".bin")
    open(fullNamePath, "wb").write(flash)

    # Echo our success
    print "Wrote", fullNamePath

def write2433(flash):
    waitForChip()

    # Retrieve the rom
    currentRom = readROM()

    # Make sure it matches
    assert currentRom == readROM(), "ROM's do not match!"

    #stupid check the flash size to 512
    # assert len(flash) == 512, "ROM size is not 512  ({0}".format(len(flash))    # 512 for Dimension (DS2433); 128 for uPrint(SE)(+) / HP Clone
    assert len(flash) == 128, "ROM size is not 128  ({0}".format(len(flash))  # 128 for uPrint(SE)(+) / HP Clone

    # Transmit the write command + the new flash
    sp.write("w")
    sp.write(flash)

    result = sp.read(3)

    print "Write Result:", repr(result)

    if result == "t":
        print("Success")
    else:
        print("Failure!")

def writeOldestToChip():
    waitForChip()
    currentRom = readROM()

    print("Detected Chip with ROM: " + binascii.hexlify(currentRom))

    romDIR = getPathForRom(currentRom)
    flashes = [f for f in os.listdir(romDIR) if not f.startswith(".")]
    flashes.sort()
    flashPath = os.path.join(romDIR, flashes[0])

    print("Attempting to flash with image from " + flashPath)
    oldestFlashData = open(flashPath).read()
    write2433(oldestFlashData)

    print("Verifying write")
    reread = readFlash()
    if reread != oldestFlashData:
        print "Write failure!  Aborting."
        print "First wrong offset:"

        print type(oldestFlashData), len(oldestFlashData)
        print type(reread), len(reread)
        for n, (d1, d2) in enumerate(zip(oldestFlashData, reread)):
            if d1 != d1:
                print "Broken at", n, binascii.hexlify(d1), binascii.hexlify(d2)
    else:
        print "Write successful."

def clearFlash():
    #waitForChip()
    currentRom = readROM()
    print("Detected Chip with ROM: " + binascii.hexlify(currentRom))
    # write2433("\0" * 512)       # 512 for Dimension (DS2433); 128 for uPrint(SE)(+) / HP Clone
    write2433("\0" * 128)       # 128 for uPrint(SE)(+) / HP Clone

# MY Arduion was not found, so I changed line to port COM13
# Start the serial port up.  NB this is *nix specific, so needs changing for windows users.
# if "linux" in sys.platform:
#    possibleSerialPorts = [d for d in os.listdir("/dev") if "ttyACM" in d]
# elif sys.platform is "darwin":
#    possibleSerialPorts = [d for d in os.listdir("/dev") if "tty.usbmodemfa131" in d]
# else:
#    possibleSerialPorts = ["COM13", "COM12"]
# spAddy = os.path.join("/dev", possibleSerialPorts[0])
# print( "Using serial port: " + spAddy)

# MY Arduion was not found, so I changed line to port COM13
sp = serial.Serial('COM13', baudrate=9600, timeout=3)
sp.flushInput()

args = parser.parse_args()

if args.test:
    waitForChip()
    print("Doing Echo Test")
    echo()
    print("Reading ROM ID:",)
    print(binascii.hexlify(readROM()))
    sys.exit(0)

if args.load:
    print("Backing up eeprom")
    dump2433()

    # Flush the input stream b/c these are independant interations
    sp.flushInput()
    print("Flashing oldest stored")
    writeOldestToChip()
else:
    print("Dumping eeprom")
    dump2433()