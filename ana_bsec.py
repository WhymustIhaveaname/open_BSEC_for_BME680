#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time,sys,traceback,math,numpy
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

import re

def get_log_lines(filename):
    p=re.compile("b'([\\-0-9,\\.\\s]+?)\\\\r\\\\n'")
    all_lines=[]
    f=open(filename)
    for line in f:
        temp=None
        temp=p.search(line)
        if not temp:
            continue
        all_lines.append([eval(i) for i in temp.group(1).split(",")])
        if(len(all_lines[-1])<5):
            all_lines.pop()
            continue
    f.close()
    return all_lines

def gen_fake_a_twolr(bseca_shld,lr1=0.0018,lr2=0.00012):
    bseca_mein=bseca_shld[0:100]
    bseca=sum(bseca_shld[50:100])/50
    for i in bseca_shld[100:]:
        if i>bseca:
            bseca+=lr1*(i-bseca)
        else:
            bseca+=lr2*(i-bseca)
        bseca_mein.append(bseca)
    return bseca_mein

def plot_bsec_a(filename):
    BSEC_B=3372
    BSEC_C=4634
    BSEC_PPM0=500.0
    K_SHIFT=273.15
    log('reading logs...')
    all_lines=get_log_lines(filename)
    log('generating bsec_a shld and acct')
    bsec_a_shld=[];bsec_a_acct=[];bsec_a_mein=[]
    for l in all_lines[:]:
        bsec_a_shld.append(BSEC_PPM0/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
        bsec_a_acct.append(l[8]/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
        #bsec_a_mein.append(l[9]/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
    log('drawing')

    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoMinorLocator,MultipleLocator

    fig=plt.figure()
    fig.set_size_inches(12,9)
    ax1=fig.subplots(1)
    ts=list(range(len(bsec_a_shld)))
    mks=0.5
    
    ax1.plot(ts,bsec_a_shld,'.',markersize=mks,label="should")
    ax1.plot(ts,bsec_a_acct,'.',markersize=mks,label="actually")
    ax1.plot(ts,gen_fake_a_twolr(bsec_a_shld),'.',markersize=mks,label="mein_twolr")
    
    #ax1.set_xlim(200,400)
    #ax1.set_ylim(0.4,1.4)
    ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.grid(True,which='both',axis='x')
    ax1.grid(True,which='both',axis='y')
    ax1.legend(loc=2)
    plt.title("%s"%(filename))
    plt.savefig("bsec_a.png",dpi=800)
    plt.show()

if __name__ == '__main__':
    log(len(get_log_lines('iaqdata.0522')))
    #plot_bsec_a('iaqdata.05082')