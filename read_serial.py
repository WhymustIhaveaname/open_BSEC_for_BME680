#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time, sys, traceback, math, numpy, signal,json, random

LOGLEVEL = {0: "DEBUG", 1: "INFO", 2: "WARN", 3: "ERR", 4: "FATAL"}
LOGFILE = sys.argv[0].split(".")
LOGFILE[-1] = "log"
LOGFILE = ".".join(LOGFILE)

def log(msg, l=1, end="\n", logfile=None, fileonly=False):
    st = traceback.extract_stack()[-2]
    lstr = LOGLEVEL[l]
    now_str = "%s %03d" % (time.strftime("%y/%m/%d %H:%M:%S", time.localtime()), math.modf(time.time())[0] * 1000)
    if l < 3:
        tempstr = "%s [%s,%s:%d] %s%s" % (now_str, lstr, st.name, st.lineno, str(msg), end)
    else:
        tempstr = "%s [%s,%s:%d] %s:\n%s%s" % (
        now_str, lstr, st.name, st.lineno, str(msg), traceback.format_exc(limit=5), end)
    if not fileonly:
        print(tempstr, end="")
    if l >= 1 or fileonly:
        if logfile == None:
            logfile = LOGFILE
        with open(logfile, "a") as f:
            f.write(tempstr)

import serial

def read_serial():
    usb=serial.Serial('/dev/ttyUSB0',203400,timeout=1)
    if usb.isOpen() :
        log("open success",l=0)
    else:
        log("open failed",l=0)
    
    while True:
        try:
            line=usb.readline()
            if(len(line)>0):
                log(line,logfile="iaqdata.txt")
        except KeyboardInterrupt:
            usb.close()
            break
        except serial.serialutil.SerialException:
            usb.close()
            break
        except:
            usb.close()
            break

if __name__ == '__main__':
    read_serial()