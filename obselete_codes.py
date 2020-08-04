def draw_y_y(filename):
    all_lines,linenums=get_log_lines(filename)
    l=[]
    for i in range(1,len(all_lines)):
        #if linenums[i]<8000:
        #    continue
        if linenums[i]<28000:
            continue
        if all_lines[i][-1]==0:
            continue
        #if all_lines[i][5]>all_lines[i-1][5]:
        #    continue
        if all_lines[i][-3]<1000:
            continue
        #if all_lines[i][-1]>100:
        #    continue
        #log(linenums[i])
        l.append(all_lines[i])
    log("got %d datas"%(len(l)))

    """raw_t=[i[0] for i in l]
    delta_t=[i[1]-i[0] for i in l]
    raw_h=[i[2] for i in l]
    delta_h=[i[3]-i[2] for i in l]
    res=[i[4]/1000 for i in l]
    iaq=[i[5] for i in l]
    co2=[i[7] for i in l]
    bvoc=[i[8] for i in l]
    siaq=[i[6] for i in l]"""
    raw_t=numpy.array([i[0] for i in l])
    raw_h=numpy.array([i[2] for i in l])
    res=numpy.array([i[5]/1000 for i in l])
    iaq=numpy.array([i[6] for i in l])
    siaq=numpy.array([i[7] for i in l])
    co2=numpy.array([i[8] for i in l])
    bvoc=numpy.array([i[9] for i in l])

    log("iaq: %s"%(iaq))
    log("co2: %s"%(co2))
    log("res: %s"%(res))

    import matplotlib.pyplot as plt
    fig=plt.figure()
    #ax=fig.add_subplot(111,projection='3d')
    #ax.scatter(res,raw_h,co2, marker='.')
    
    ax1=fig.subplots(1)
    #ax1.plot(co2,siaq,'.',markersize=1,label="sIAQ to $CO_2$")
    #ax1.plot(co2,bvoc,'.',markersize=1,label="bVOC to $CO_2$")
    ax1.plot(res,co2,'.:',markersize=1,label="")
    #ax1.plot(raw_h,delta_h,'.',markersize=1,label=r"$delta humi to raw humi")
    #ax1.plot([i[5]/1000 for i in l_low],[i[8] for i in l_low],'.b',markersize=1,label=r"t<27")
    #ax1.plot([i[5]/1000 for i in l_high],[i[8] for i in l_high],'.r',markersize=1,label=r"t>27")
    #ax1.plot([i[5]/1000 for i in l_low],[i[8] for i in l_low],'.b',markersize=1,label=r"h<52%")
    #ax1.plot([i[5]/1000 for i in l_high],[i[8] for i in l_high],'.r',markersize=1,label=r"h>52%")
    #ax1.axis([0,8000,0,1050])
    #plt.axhline(y=exact_gs_energy,c="green",xmin=0,xmax=1,label='Exact=%.4f'%(exact_gs_energy))
    #ax1.set_ylabel('static IAQ')
    #ax1.set_xlabel('$CO_2$ concentraiation(ppm)')
    #ax1.set_ylabel('humidity correction')
    #ax1.set_xlabel('raw humidity(%)')
    plt.title("%s"%(filename))
    plt.savefig("iaqtemp.png")
    plt.show()

def model1(filename):
    """delta p = A + B/T - ln(R)"""
    all_lines,linenums=get_log_lines(filename)
    l=[]
    for i in range(1,len(all_lines)):
        #if linenums[i]<8000:
        #    continue
        if linenums[i]<28000:
            continue
        if all_lines[i][-1]==0:
            continue
        #if all_lines[i][5]>all_lines[i-1][5]:
        #    continue
        if all_lines[i][-3]<1000:
            continue
        if all_lines[i][5]<76800 and linenums[i]%4!=0:
            continue
        if 105000<all_lines[i][5]<130000 and linenums[i]%4!=0:
            continue
        #if all_lines[i][-1]>100:
        #    continue
        #log(linenums[i])
        l.append(all_lines[i])
    log("got %d datas"%(len(l)))

    res=numpy.array([i[5] for i in l])
    tres=numpy.array([[i[1]+273.15 for i in l],[i[5] for i in l]])
    co2=numpy.array([i[8] for i in l])

    #log(numpy.linalg.norm(dp(coes,co2,tres))/math.sqrt(len(co2)))
    #l_temp=list(numpy.abs(dp(coes,co2,tres)))
    #l_temp.sort(reverse=True)
    #log(l_temp[0:10])
    
    def dp_4_curve(xs,A,B,C):
        return C*(A+B/xs[0]-numpy.log(xs[1]))
    para,pcov=curve_fit(dp_4_curve,tres,co2,p0=(0,18000,5000))
    stde=numpy.sqrt(numpy.diag(pcov))
    log("para: %s"%(para))
    log("stde: %s"%(stde))
    #log("pcov: %s"%(pcov))
    log(numpy.linalg.norm(dp_4_curve(tres,para[0],para[1],para[2])-co2)/math.sqrt(len(co2)))
    l_temp=list(numpy.abs(dp_4_curve(tres,para[0],para[1],para[2])-co2))
    l_temp.sort(reverse=True)
    log(l_temp[0:10])

    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax1=fig.subplots(1)
    ax1.plot(res,co2,'.',markersize=2,label="Raw Data")
    ax1.plot(res,dp_4_curve(tres,para[0],para[1],para[2]),'.',markersize=2,label="Fit Curve")
    #stde2=[0,stde[1]/3,stde[2]]
    #stde2[1]=0
    #ax1.plot(res,dp_4_curve(tres,*(para-stde2)),'-',linewidth=1,label="Fit Curve Min")
    #ax1.plot(res,dp_4_curve(tres,*(para+stde2)),'-',linewidth=1,label="Fit Curve Max")
    ax1.legend()
    ax1.set_ylabel(r'$CO_2$ Concentraiation(ppm)')
    ax1.set_xlabel(r'Gas Resistance($\Omega$)')
    plt.text(95000,4000,"$CO_2(ppm)=C\\times(A+\\frac{B}{T(K)}-ln(R_{MOS}(\\Omega)))$ \n$A=-52.7\\pm2.4$ \n$B=(1.934\\pm0.007)\\times10^{4}$ \n$C=5032\\pm27$")
    plt.title("%s"%(filename))
    plt.savefig("co2_res_model1.png")
    plt.show()

def stat_bsec_a(filename):
    BSEC_B=3372
    BSEC_C=4634
    BSEC_PPM0=500.0
    K_SHIFT=273.15
    log(1)
    all_lines,linenums=get_log_lines(filename)
    log(2)
    bsec_a_shld=[]
    bsec_a_acct=[]
    bsec_a_mein=[]
    for l in all_lines:
        bsec_a_shld.append(BSEC_PPM0/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
        bsec_a_acct.append(l[8]/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
        bsec_a_mein.append(l[9]/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
    log(3)

    #beg=4820;end=5200
    #beg=68300;end=68800
    beg=88000;end=92000
    inc=[]
    dec=[]
    ax=0
    flag=True
    for i in range(beg+1,end+1):
        if bsec_a_shld[i]>bsec_a_shld[i-1]:
            if flag:
                ax+=1
            else:
                dec.append(ax)
                ax=1
                flag=True
        else:
            if not flag:
                ax+=1
            else:
                inc.append(ax)
                ax=1
                flag=False
    inc_sum=[0]*(max(inc)+1)
    dec_sum=[0]*(max(dec)+1)
    for i in inc:
        inc_sum[i]+=1
    for i in dec:
        dec_sum[i]+=1
    log(inc_sum)
    log(dec_sum)

def plot_bsec_a(filename):
    BSEC_B=3372
    BSEC_C=4634
    BSEC_PPM0=500.0
    K_SHIFT=273.15
    log(1)
    all_lines,linenums=get_log_lines(filename)
    log(2)
    bsec_a_shld=[];bsec_a_acct=[];bsec_a_mein=[]
    for l in all_lines[:]:
        bsec_a_shld.append(BSEC_PPM0/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
        bsec_a_acct.append(l[8]/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
        bsec_a_mein.append(l[9]/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
    log(3)

    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoMinorLocator,MultipleLocator

    fig=plt.figure()
    fig.set_size_inches(12,9)
    ax1=fig.subplots(1)
    #ax2=ax1.twinx()
    ts=list(range(len(bsec_a_shld)))
    mks=0.5
    #ax1.plot(ts,[i[-1] for i in all_lines],'g.',markersize=max(mks//2,1),label="R")
    #ax1.axhline(y=0,c="pink",xmin=0,xmax=1,label='0')
    """for i in range(100,1999):
        if (bsec_a_shld[i]>bsec_a_shld[i-1] and bsec_a_shld[i]>bsec_a_shld[i+1]) or \
           (bsec_a_shld[i]<bsec_a_shld[i-1] and bsec_a_shld[i]<bsec_a_shld[i+1]):
           ax1.axvline(x=i,c="pink",ymin=0,ymax=1)"""
    #ax1.plot(ts,gen_fake_a_lr(all_lines),'.',markersize=mks,label="gedanken")
    #ax1.plot(ts,gen_fake_a(bsec_a_shld),'.',markersize=mks,label="gedanken")
    
    ax1.plot(ts,bsec_a_shld,'.',markersize=mks,label="should")
    ax1.plot(ts,bsec_a_acct,'.',markersize=mks,label="actually")
    ax1.plot(ts,bsec_a_mein,'.',markersize=mks,label="two lr")
    ax1.plot(ts,gen_fake_a_fsm(bsec_a_shld),'.',markersize=mks,label="fsm")
    
    #ax1.set_xlim(200,400)
    #ax1.set_ylim(0.4,1.4)
    ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.grid(True,which='both',axis='x')
    ax1.grid(True,which='both',axis='y')

    """ax2.axhline(y=0,c="pink",xmin=0,xmax=1,label='0')
    ax2.axhline(y=1,c="pink",xmin=0,xmax=1,label='0')
    df=[];x_df=[]
    for i in range(1,len(bsec_a_shld)):
        if abs(bsec_a_shld[i]-bsec_a_shld[i-1])>1e-3:
            df.append((bsec_a_acct[i]-bsec_a_acct[i-1])/(bsec_a_shld[i]-bsec_a_shld[i-1]))
            if abs(df[-1])>1.1:
                df.pop()
            else:
                x_df.append(i)
    ax2.plot(x_df,df,'g^-',markersize=mks,label="diff ratio")"""
    #ax2.plot(ts[1:],[bsec_a_shld[i+1]-bsec_a_shld[i] for i in range(len(all_lines)-1)],'.',markersize=mks,label="diff should")
    #ax2.plot(ts[1:],[bsec_a_acct[i+1]-bsec_a_acct[i] for i in range(len(all_lines)-1)],'x-',markersize=mks,label="diff actually")
    #ax2.xaxis.set_minor_locator(AutoMinorLocator(5))
    #ax2.grid(True,which='major',axis='y')
    #ax2.set_xlim(21000,22000)
    #ax2.set_ylim(-0.05,0.06)

    #ax2.legend(loc=1)
    ax1.legend(loc=2)
    plt.title("%s"%(filename))
    plt.savefig("bsec_a.png",dpi=800)
    plt.show()

def gen_fake_a_fsm(bseca_shld,lr3=0.17,lr4=0.00005,lr1=0.1,lr2=0.01,latsz=0.02,s1th=1000):
    """finite state mechine"""
    # 0: 快速趋近模式，以lr1向上，lr2向下的速度快速逼近
    # 1: 不响应模式
    # 2: 弃疗模式，lr3*delta_shld+lr4*(shld-mein)
    bseca_mein=list(bseca_shld[0:100])
    bseca=sum(bseca_shld[50:100])/50
    state=0
    dec_ct=0
    lat_last=bseca
    shld_last=bseca_shld[99]
    for i in bseca_shld[100:]:
        if state==0:
            if i>bseca:
                bseca+=lr1*(i-bseca)
            else:
                bseca+=lr2*(i-bseca)
            if bseca>(lat_last+latsz):
                lat_last=lat_last+latsz
                dec_ct=max(dec_ct-2,0)
            elif bseca<(lat_last-latsz):
                lat_last=lat_last-latsz
                dec_ct+=1
                if dec_ct>=3:
                    state=1
                    s1_ct=s1th
        elif state==1:
            s1_ct-=1
            if bseca<(i-latsz):
                state=0
                dec_ct=0
                lat_last=bseca
            if s1_ct<=0:
                state=2
        elif state==2:
            #if abs(i-shld_last)<0.01:
            bseca+=lr3*(i-shld_last)+lr4*(i-bseca)
            if bseca<(i-latsz):
                state=0
                dec_ct=0
                lat_last=bseca
        else:
            log("you are flying",l=2)
        bseca_mein.append(bseca)
        shld_last=i
    return bseca_mein

def gen_fake_a(bseca_shld):
    dumps_dec=[float('nan'),1.0,0.86,0.64]
    dumps_dec2=[float('nan'),0.2,0.1,0.1]
    dumps_inc=[float('nan'),1.0,0.86,0.64]
    dumps_inc2=[float('nan'),0.2,0.1,0.1]
    a_fake=bseca_shld[0:100]
    a_temp=sum(bseca_shld[50:100])/50
    a_ext=a_temp
    ashld_max=bseca_shld[99]
    dir_flag=2 #0 dec, 1 inc
    for i in range(100,len(bseca_shld)):
        if bseca_shld[i]>=bseca_shld[i-1]:
            if dir_flag==1:
                suc_mono+=1
            else:
                a_ext=a_temp
                suc_mono=1
                dir_flag=1
        else:
            if dir_flag==0:
                suc_mono+=1
            else:
                a_ext=a_temp
                suc_mono=1
                dir_flag=0
        if dir_flag==1:
            if bseca_shld[i]>ashld_max-0.1:
                if suc_mono<len(dumps_inc):
                    a_temp+=dumps_inc[suc_mono]*(bseca_shld[i]-bseca_shld[i-1])
                else:
                    a_temp+=0.0*(a_ext-a_temp)
            else:
                if suc_mono<len(dumps_inc2):
                    a_temp+=dumps_inc2[suc_mono]*(bseca_shld[i]-bseca_shld[i-1])
                else:
                    a_temp+=0.0*(a_ext-a_temp)
        else:
            if bseca_shld[i]>ashld_max-0.1:
                if suc_mono<len(dumps_dec):
                    a_temp+=dumps_dec[suc_mono]*(bseca_shld[i]-bseca_shld[i-1])
                else:
                    a_temp+=0.15*(a_ext-a_temp)
            else:
                if suc_mono<len(dumps_dec2):
                    a_temp+=dumps_dec2[suc_mono]*(bseca_shld[i]-bseca_shld[i-1])
                else:
                    a_temp+=0.15*(a_ext-a_temp)
        a_fake.append(a_temp)
        if bseca_shld[i]>ashld_max:
            ashld_max=bseca_shld[i]
    return a_fake

def gen_fake_co2(lines,BSEC_B=3372.0,BSEC_C=4634.0,lr1=0.9,lr2=0,lr3=1,mode=0):
    BSEC_PPM0=500.0
    K_SHIFT=273.15
    bsec_a=100
    my_co2s=[]

    for i,l in enumerate(lines):
        cali_ct=i
        bsec_a_temp=BSEC_PPM0/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5])
        if cali_ct<50:
            bsec_a=bsec_a_temp;
        elif cali_ct<100:
            bsec_a=bsec_a+(bsec_a_temp-bsec_a)/(cali_ct-49)
        elif bsec_a_temp>bsec_a:
            bsec_a=bsec_a+lr1*(bsec_a_temp-bsec_a)
            #bsec_a=bsec_a+(9.58950368e-4)*(bsec_a_temp-bsec_a)
        else:
            bsec_a=bsec_a+lr2*(bsec_a_temp-bsec_a)
        my_co2=BSEC_C*(bsec_a + BSEC_B/(l[1]+K_SHIFT) - math.log(l[5]))
        if(i>0):
            my_co2=my_co2s[-1]+lr3*(my_co2-my_co2s[-1])
        my_co2s.append(my_co2)
    """if mode==0:
        for i,l in enumerate(lines):
            if l[8]<525:
                my_co2s[i]=l[8]
    elif mode==1:
        ax=0
        for i,l in enumerate(lines):
            if l[8]<525:
                ax+=1
        log("%d except"%(ax))"""
    return my_co2s

def plot_t_y(filename):
    all_lines,linenums=get_log_lines(filename)
    l=all_lines
    
    ts=list(range(len(l)))
    mks=5
    
    import matplotlib.pyplot as plt
    fig=plt.figure(figsize=(12,9))
    ax1=fig.subplots(1)
    ax1.axhline(y=500,c="pink",xmin=0,xmax=1,label='500')
    ax1.plot(ts,[i[8] for i in l],'.',markersize=mks,label="bsec's co2")
    ax1.plot(ts,[i[9] for i in l],'.',markersize=mks,label="my co2")
    #ax1.plot(ts,gen_fake_co2(l),'.',markersize=mks,label="gedanken co2")
    ax1.set_ylim(0,6000)
    ax2=ax1.twinx()
    ax2.plot(ts,[i[5] for i in l],'g.',markersize=max(mks//2,1),label="gas resistance")
    

    ax1.legend(loc=2)
    ax2.legend(loc=1)
    plt.title("%s"%(filename))
    plt.savefig("time_expand.png")
    plt.show()

def fit_co2(filename):
    all_lines,linenums=get_log_lines(filename)
    log(len(linenums))
    #all_lines=all_lines[0:4290]
    bsec_co2s=numpy.array([i[8] for i in all_lines])
    para,pcov=curve_fit(gen_fake_co2,all_lines,bsec_co2s,p0=(5000,5000,0.5,0.001,0.0001))
    stde=numpy.sqrt(numpy.diag(pcov))
    log("para: %s"%(para))
    log("stde: %s"%(stde))
    log(numpy.linalg.norm(numpy.array(gen_fake_co2(all_lines,*para))-bsec_co2s)/math.sqrt(len(bsec_co2s)))

    import matplotlib.pyplot as plt
    fig=plt.figure()
    fig.set_size_inches(12,9)
    ax1=fig.subplots(1)
    ax1.axhline(y=500,c="c",xmin=0,xmax=1,label='500',linewidth=1)
    ax1.axhline(y=525,c="y",xmin=0,xmax=1,label='525',linewidth=1)
    ts=list(range(len(all_lines)))
    mks=1
    ax1.plot(ts,[i[8] for i in all_lines],'.',markersize=mks,label="bsec's co2")
    ax1.plot(ts,gen_fake_co2(all_lines,*para,mode=1),'.',markersize=mks,label="gedanken co2")
    ax2=ax1.twinx()
    ax2.plot(ts,[i[1] for i in all_lines],'g.',markersize=max(mks//2,1),label="")
    ax1.legend(loc=2)
    plt.title("%s"%(filename))
    plt.savefig("fit2.png",dpi=600)
    plt.show()

def gen_fake_a_lr2(lines,BSEC_B=3372.0,BSEC_C=4634.0):
    BSEC_PPM0=500.0
    K_SHIFT=273.15
    bsec_as=[]
    bsec_a_temps=[]
    bsec_a_max=0
    for i,l in enumerate(lines):
        cali_ct=i
        bsec_a_temps.append(BSEC_PPM0/BSEC_C - BSEC_B/(l[1]+K_SHIFT) + math.log(l[5]))
        if cali_ct<50:
            bsec_as.append(bsec_a_temps[-1])
        elif cali_ct<100:
            bsec_as.append(bsec_as[-1]+(bsec_a_temps[-1]-bsec_as[-1])/(cali_ct-49))
        elif bsec_a_temps[-1]>bsec_as[-1]:
            bsec_as.append(bsec_as[-1]+0.9*(bsec_a_temps[-1]-bsec_as[-1]))
        elif bsec_a_temps[-1]>bsec_a_max-0.1:
            delta_a_temp=(bsec_a_temps[-1]-bsec_a_temps[-2])
            if delta_a_temp<0:
                bsec_as.append(bsec_as[-1]+0.8*delta_a_temp)
            else:
                bsec_as.append(bsec_as[-1]+0.3*delta_a_temp)
        else:
            bsec_as.append(bsec_as[-1]+0.3*(bsec_a_temps[-1]-bsec_a_temps[-2]))
        
        if bsec_a_temps[-1]>bsec_a_max:
            bsec_a_max=bsec_a_temps[-1]
    return bsec_as

def fit_bseca(filename):
    all_lines,linenums=get_log_lines(filename)
    log("get %d data"%(len(all_lines)),l=0)
    BSEC_B=3372.0
    BSEC_C=4634.0
    bseca_shld=[]
    bseca_acct=[]
    for l in all_lines:
        bseca_shld.append(500.0/BSEC_C - BSEC_B/(l[1]+273.15) + math.log(l[5]))
        bseca_acct.append(l[8]/BSEC_C - BSEC_B/(l[1]+273.15) + math.log(l[5]))
    bseca_acct=numpy.array(bseca_acct)

    """para=(0.0018,0.00012)
    para,pcov=curve_fit(gen_fake_a_twolr,bseca_shld,bseca_acct,p0=para)
    predict=numpy.array(gen_fake_a_twolr(bseca_shld,*para))"""

    para=(0.01,0.01)
    log(para)
    para,pcov=curve_fit(gen_fake_a_fsm,bseca_shld,bseca_acct,p0=para)
    predict=numpy.array(gen_fake_a_fsm(bseca_shld))

    log(para)
    stde=numpy.sqrt(numpy.diag(pcov))
    log("stde: %s"%(stde))
    std_dev=numpy.linalg.norm(predict-bseca_acct)/math.sqrt(len(bseca_acct))
    #std_dev=numpy.linalg.norm(numpy.array(bseca_shld)-bseca_acct)/math.sqrt(len(bseca_acct))
    log("std dev: %.2f%%"%(std_dev*100))

if __name__ == '__main__':
    #fit_bseca("iaqdata.05082")
    #fit_bseca("iaqdata.txt")
    
    #plot_bsec_a("iaqdata.05082")
    plot_bsec_a("iaqdata.txt")
    
    #plot_t_y("iaqdata.05082")
    #stat_bsec_a("iaqdata.05082")