from tkinter import *
import subprocess
import time
import scipy.optimize as sc
import math
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from scipy.optimize import fsolve
import math

def equations3(unknowns,x,y,z,r):
#calibrated values
    xc1,xc2,xc3=x
    yc1,yc2,yc3=y
    zc1,zc2,zc3=z
    x1,y1,z1=unknowns
    eq1=r[0]**2-(xc1-x1)**2-(yc1-y1)**2-(zc1-z1)**2
    eq4=r[1]**2-(xc2-x1)**2-(yc2-y1)**2-(zc2-z1)**2
    eq7=r[2]**2-(xc3-x1)**2-(yc3-y1)**2-(zc3-z1)**2
    return (eq1,eq4,eq7)


def posequations(unknowns,router1,router2,router3,r1,r2,r3):
#calibrated values
    x1,y1,z1=router1
    x2,y2,z2=router2
    x3,y3,z3=router3
    x,y,z=unknowns
    eq1=r1**2-(x-x1)**2-(y-y1)**2-(z-z1)**2
    eq2=r2**2-(x-x2)**2-(y-y2)**2-(z-z2)**2
    eq3=r3**2-(x-x3)**2-(y-y3)**2-(z-z3)**2
    return (eq1,eq2,eq3)



def Distance(quality):	#Rssi = requency A=35 n=2
	#RSSI=quality/2-100
    # if int(quality)<-50:                  #behind wall
    #     RSSI1m=-30; Envfactor=4
    # elif int(quality)<-70:
    #     RSSI1m=-40; Envfactor=4
    # else:
    #     RSSI1m=-22; Envfactor=3
    RSSI1m=-50; Envfactor=4
    A=RSSI1m; n=Envfactor
    RSSI=quality
    aux=RSSI-A
    aux=(-1)*aux
    aux=float(aux)/(10*n)
    x=math.pow(10,aux)
    return x

def displaydata(dict_wifi,interval,name1,name2,name3):
			root=Tk()
			root.wm_title("Wi-fi AP Information")
			text=Text(root)
			text.insert(INSERT,"S.No."+'   '+"SSID"+'          '+"Channel"+'   '+"quality"+'   '+"Distance(mts)")
			text.insert(INSERT,'\n')
			text.insert(INSERT,"----------------------------------------------------------------------------")
			text.insert(INSERT,'\n')
			n=1
			for i in dict_wifi.keys():
				if dict_wifi[i]!=[]:
					if name1=='all':
						text.insert(INSERT,str(n)+' ')
						for j in dict_wifi[i]:
							text.insert(INSERT,str(j)+'      ')
						text.insert(INSERT,'\n')
						text.insert(INSERT,"----------------------------------------------------------------------")
						text.insert(INSERT,'\n')
						n=n+1
					elif dict_wifi[i][0].startswith(name1) or dict_wifi[i][0].startswith(name2) or dict_wifi[i][0].startswith(name3):
						text.insert(INSERT,str(n)+'      ')
						for j in dict_wifi[i]:
							text.insert(INSERT,str(j)+'      ')
						text.insert(INSERT,'\n')
						text.insert(INSERT,"----------------------------------------------------------------------")
						text.insert(INSERT,'\n')
						n=n+1
					#print ('\n')
			#print('a')
			#text.insert(END,"Finished")
			text.pack()
			root.after(int(interval*1000), lambda: root.destroy())
			root.mainloop()

def findallrouterslinux():
    #Process=subprocess.Popen(["iwlist","wlp2s0",sccan"],stdout=subprocess.PIPE,universal_newlines=True)  #iwlist for linux
    Process=subprocess.Popen(["sudo","iwlist","wlan0","scan"],stdout=subprocess.PIPE,universal_newlines=True)
    out,err=Process.communicate()	#start communicating = outputting
    #print(out,err)
    new_l=out.split('\n')	#split str out through enters
    n=0
    cells=[[0]*5]
    for line in new_l:
        line=line.lstrip()	#removes whitespace left
        line=line.rstrip()	#removes whitespace right
        if line.startswith("Cell"): #address
            line1=line.split()
            cells[n][0]=line1[4]
        if line.startswith("ESSID"):
            line2=line.split(":")
            cells[n][1]=line2[1]	#name
        if line.startswith("Quality"):
            line5=line.split()
    		#line6=line.split(' ')
    		#line5=line.split("=")
            line6=line5[2].split("=")
    	#	print line6[1]
            cells[n][2]=(line6[1])  #quality
        if line.startswith("Frequency"):
            line4=line.split(":")
            k=line4[1].split(' ')
    #		print k[0]
            cells[n][3]=(k[0])      #frequency
        if line.startswith("Channel"):
            line3=line.split(":")
            #print (line3[1])
            cells[n][4]=(line3[1])  #channel
            cells.append([0]*5)
            n=n+1
    try:
        cells.remove([0]*5)
    except:
        ''
    dict_wifi={}
    #print(len(cells))
    for i in range(0,len(cells)):
        dict_wifi[i]=[]
    for i in range(0,len(cells)):
            dict_wifi[i].append(str(cells[i][0])+':'+str(cells[i][1]))	#address
            dict_wifi[i].append(cells[i][3])	#frequency
            dict_wifi[i].append(cells[i][2])	#quality
            #dict_wifi[i].append(str(Distance(int(cells[i][2]))))
    return cells,dict_wifi
def findallrouterswindows():
    #Process=subprocess.Popen(["iwlist","wlp2s0",sccan"],stdout=subprocess.PIPE,universal_newlines=True)  #iwlist for linux
    Process=subprocess.Popen(["netsh","wlan","show","networks",'mode=bssid'],stdout=subprocess.PIPE,universal_newlines=True)
    out,err=Process.communicate()	#start communicating = outputting
    #print(out,err)
    new_l=out.split('\n')	#split str out through enters
    n=0
    cells=[[0]*4]
    for line in new_l:
        line=line.lstrip()	#removes whitespace left
        line=line.rstrip()	#removes whitespace right
        if line.startswith("SSID"):
            line2=line.split(":")
            networkname=line2[1][1:len(line2[1])]
            #print (networkname)
            cells[n][0]=networkname
        if line.startswith("BSSID"):
            line2=line.split(":")
            #print (line2[0],'7 place',line2[0][7])
            if line2[0][7]==line2[0][10]:
                name=line2[0][0:5]+line2[0][6]
            else:
                name=line2[0][0:5]+line2[0][6:8]
            #	print (line2[0][6:8],'6-8')

            cells[n][0]=(networkname+'_'+name)	#gives out name of connection
        if line.startswith("Signal"):
            line5=line.split(":")
            signal=line5[1].strip('%')
            RSSI=signal/2-100
            cells[n][2]=(RSSI)
        if line.startswith("Channel"):
            line3=line.split(":")
            #print (line3[1])
            cells[n][1]=(line3[1])
            cells.append([0]*3)
            n=n+1
    try:
        cells.remove([0]*3)
    except:
        ''
    dict_wifi={}
    #print(len(cells))
    for i in range(0,len(cells)):
        dict_wifi[i]=[]
    for i in range(0,len(cells)):
            dict_wifi[i].append(cells[i][0])	#namre
            dict_wifi[i].append(cells[i][1])	#channel
            dict_wifi[i].append(cells[i][2])	#signal
            dict_wifi[i].append(str(Distance(int(cells[i][2]),RSSI1m,Envfactor)))
    return cells,dict_wifi

def calibrate():
    ## calibrate
    measurementindex=0
    x=[0]*3
    y=[0]*3
    z=[0]*3
    while measurementindex<=2: #3 points
        x[measurementindex]=float(input('x '))
        y[measurementindex]=float(input('y '))
        z[measurementindex]=float(input('z '))
        cells,dict_wifi=findallrouterslinux()
        #sort data
        if measurementindex==0:

            n=0
            quality=[[0]*len(cells)]
            names=[0]*len(cells)

            for l in dict_wifi.keys():
                names[n]=dict_wifi[l][0]
                quality[measurementindex][n]=dict_wifi[l][2]	#list contains nr of measurements & sublist contains nr of wifis
                n=n+1
        else:
            n=0
            quality.append([0]*len(quality[measurementindex-1]))
            for i in dict_wifi.keys():
                try:
                    nameindex=names.index(dict_wifi[i][0])	#finds index of wifiname in array names
                    quality[measurementindex][nameindex]=dict_wifi[i][2]
                    #print(quality)
                except:
                    names.append(dict_wifi[i][0])		#appends new name if it doesn't find it
                    quality[measurementindex].append(dict_wifi[i][2])
                    for m in range(0,measurementindex):
                        quality[m].append(0)
                    quality[measurementindex].append(dict_wifi[i][2])
                    #nameindex=names(dict_wifi[i][0])
                #print(quality,'   ',names)
            n=n+1

        measurementindex=measurementindex+1

        #displaydata(dict_wifi,self.interval,'robolabwifi','controlslab','rc_car')
        #displaydata(dict_wifi,self.interval*10,'','','')
        #wifi names robolabwifi controlslab rc_car

    #take matrix transpose
    #print(quality,names)
    qlength=0
    for i in range(0,len(quality)):
        if qlength<len(quality[i]):
            qlength=len(quality[i])
            #print(qlength)
    #print(np.shape(names))
    quality1=np.zeros((len(names),len(quality)))
    for i in range(0,len(quality)):
        for j in range(0,len(quality[i])):
            try:
                quality1[j][i]=quality[i][j]
            except:
                ''
    #calculate wifi positions

    i=0; l=0
    xrouter=[0]; yrouter=[0]; zrouter=[0];sRouter=[]
    while i<len(names):
        wifi1=names[i]
        r=[0]*3
        #print(x,y,z)
        for j in range(0,len(quality1[i])):
            qualitywifi1=quality1[i][j]
            r[j]=Distance(qualitywifi1)
        try:
            sol=(sc.root(equations3,(1,1,1),args=(x,y,z,r)))
            if sol.success==True:
                xrouter.append(sol.x[0])
                yrouter.append(sol.x[1])
                zrouter.append(sol.x[2])
                sRouter.append(names[i])
                print(names[i],sol.x[0],sol.x[1],sol.x[2])
                l=l+1
                #print(sol)
            #else:
                #print('no solution found')
                #print(names[i],r[0],r[1],r[2],quality1[i][0],quality1[i][1],quality1[i][2],'\n')
        except:
            print('error occured')
        i=i+1
    print('number of networks=',l)
    # print(quality1,'\n',names)
    return xrouter,yrouter,zrouter,sRouter

#def calculatecoordinates(xrouter,yrouter,zrouter,sRouter):

class readwifi(threading.Thread):
    def __init__(self,interval,xrouter,yrouter,zrouter,sRouter):
		#self.root = Tkinter.Tk()
        self.interval=interval
        self.xrouter=xrouter
        self.yrouter=yrouter
        self.zrouter=zrouter
        self.sRouter=sRouter
        super(readwifi, self).__init__()
    def run(self):
        interval=self.interval
        xrouter=self.xrouter
        yrouter=self.yrouter
        zrouter=self.zrouter
        sRouter=self.sRouter
        #pos=[]
        runningindex=0
        while True:
            tic=time.time()
            cells,dict_wifi=findallrouterslinux()
            #print(dict_wifi,sRouter)
            signal=[0]*len(sRouter);
            for m in dict_wifi.keys():
                try:
                # for n in range(0,len(sRouter)):
                #     if sRouter[n]==dict_wifi[m][0]:
                #         nameindex=n
                #         signal[n]=dict_wifi[m][2]
                #         print(signal[n])


                    nameindex=sRouter.index(dict_wifi[m][0])	#finds index of wifiname in array sRouter
                    signal[nameindex]=int(dict_wifi[m][2])
                    # print(nameindex,signal)
                    #print(quality)
                except:
                    ''
                #nameindex=names(dict_wifi[i][0])
                    #print(m)
            #print('Signal',signal)
            pos=[]; namesol=[];
            for i in range(0,len(signal)):
                if (len(signal)-i)<3:
                    i=i-(3-(len(signal)-i))
                #print('i',i,'lensignal',len(signal))
                router1=[xrouter[i],yrouter[i],zrouter[i]]
                router2=[xrouter[i+1],yrouter[i+1],zrouter[i+1]]
                router3=[xrouter[i+2],yrouter[i+2],zrouter[i+2]]
                r1=Distance(signal[i]);
                r2=Distance(signal[i+1]);
                r3=Distance(signal[i+2]);
                #try:
                sol=(sc.root(posequations,(1,1,1),args=(router1,router2,router3,r1,r2,r3)))
                # if runningindex==0:
                #
                #print(sol)
                if sol.success==True:
                    #print(sol)
                    pos.append(sol.x)
                    namesol.append(sRouter[i])
                    namesol.append(sRouter[i+1])
                    namesol.append(sRouter[i+2])
                #else:
                    #print(sRouter[i],r1,r2,r3)
                # except:
                #     print('no solution')
                i=i+3
            toc=time.time()
            print(pos)
            #print(namesol)
            print('time=',toc-tic)
            runningindex=runningindex+1
            #time.sleep(interval)






xrouter,yrouter,zrouter,sRouter=calibrate()
#xrouter,yrouter,zrouter,sRouter=dataset()

# names= ['58:6D:8F:88:29:EF:0', 'FA:8F:CA:6A:02:85:"dsl"', '24:F5:A2:41:FF:B1:"Office TV.v"', '14:91:82:72:58:7F:"rc_car"', '38:17:C3:AF:C5:30:"VRL"', '38:17:C3:AF:C5:31:"eduroam"', '38:17:C3:AF:C5:32:"UCSB Setup"', '38:17:C3:AF:C5:33:"UCSB Wireless Web"', 'C0:C1:C0:DC:4B:05:"UCSB Secure"', '24:F5:A2:41:FF:B2:"robolabwifi"', '38:17:C3:AF:AA:12:"rc_car_5GHz"', '38:17:C3:AF:AA:13:"UCSB Wireless Web"', '38:17:C3:AF:AA:10:"UCSB Secure"', 'E0:91:F5:C8:10:3F:"eduroam"', 'C0:C1:C0:DC:4B:04:""', '38:17:C3:AB:70:62:"robolabwifi"', '38:17:C3:AB:70:63:"UCSB Wireless Web"', '38:17:C3:AF:C3:B0:"UCSB Secure"', 'B8:09:8A:DA:C2:E7:"eduroam"', '88:63:DF:A8:48:11:"Soorya\\xE2\\x80\\x99s iMac"', '38:17:C3:EC:CA:40:"Mohammed\'s iMac"', '38:17:C3:EC:CA:41:"eduroam"', '38:17:C3:EC:CA:42:"UCSB Setup"', '38:17:C3:EC:CA:43:"UCSB Wireless Web"', '38:17:C3:AB:70:60:"UCSB Secure"', '38:17:C3:AB:70:61:"eduroam"', '38:17:C3:AF:C5:23:"UCSB Setup"', '88:63:DF:9F:CC:15:"UCSB Secure"', '28:F0:76:08:F6:84:"sina\'s iMac"', '38:17:C3:AF:C4:50:"Weiting\\xE2\\x80\\x99s iMac"', '38:17:C3:AF:C4:51:"eduroam"', '38:17:C3:AF:C4:52:"UCSB Setup"', '38:17:C3:AF:C4:53:"UCSB Wireless Web"', '38:17:C3:AF:C5:20:"UCSB Secure"', '38:17:C3:AF:C5:21:"eduroam"', '38:17:C3:AF:C5:22:"UCSB Setup"', '10:6F:3F:E8:83:3A:"UCSB Wireless Web"', '30:23:03:29:0E:47:"MOMENTLab"', '0:"controlslab"', '8A:15:04:BD:E1:7F:"controlslab"', '8A:15:04:BD:E1:74:"\\x00\\x00\\x00\\x00"', '8A:15:04:BD:E1:75:"\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"', '38:17:C3:AF:C3:A0:"\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"', '38:17:C3:AF:C3:A1:"eduroam"', '38:17:C3:AF:C3:A2:"UCSB Setup"', '38:17:C3:AF:AA:03:"UCSB Wireless Web"', '38:17:C3:AF:AA:00:"UCSB Secure"', '38:17:C3:AF:C3:B1:"eduroam"', '38:17:C3:AF:C3:B2:"UCSB Setup"', '38:17:C3:AF:C3:B3:"UCSB Wireless Web"', '38:17:C3:AF:C4:90:"UCSB Secure"', '38:17:C3:AF:C4:91:"eduroam"', '38:17:C3:AF:C4:92:"UCSB Setup"', '38:17:C3:AF:C4:93:"UCSB Wireless Web"', '38:17:C3:AB:70:70:"UCSB Secure"', '38:17:C3:AB:70:71:"eduroam"', '38:17:C3:AB:70:72:"UCSB Setup"', '38:17:C3:AB:70:73:"UCSB Wireless Web"', '38:17:C3:AF:AA:11:"UCSB Secure"', '0:"UCSB Setup"', '38:17:C3:AB:70:60:"eduroam"', '28:F0:76:08:F6:84:"UCSB Secure"', 'C8:E0:EB:27:4F:B3:"UCSB Setup"', '10:6F:3F:E8:83:3B:"Anant\\xE2\\x80\\x99s iMac"', 'B0:B8:67:CE:33:D1:"MOMENTLab_5GHz"', '38:17:C3:EC:CA:50:"UCSB Setup"', '38:17:C3:EC:CA:51:"eduroam"', '38:17:C3:EC:CA:52:"UCSB Setup"', '38:17:C3:EC:CA:53:"UCSB Wireless Web"', '0:"UCSB Secure"']
#
# quality=np.array([[  0,   0,   0,], [-65, -72, -58,], [-56, -58, -61,], [-28, -31, -28,], [-52, -54, -54,], [-58, -57, -60,], [-57, -57, -60,], [-57, -57, -60,], [-58, -57, -60,], [-49, -50, -48,], [-34, -32, -35,], [-77, -77, -77,], [-78, -77, -77,], [-77, -77, -77,], [-51, -42, -47,], [-35, -35, -31,], [-77, -77, -85,], [-77, -77, -84,], [-78, -78,   0,], [-68, -68,   0,], [-75, -75,   0,], [-78, -78,   0,], [-78, -78,   0,], [-78, -78,   0,], [-78, -78,   0,], [-77, -77, -85,], [-77, -77, -85,], [-69, -64,   0,], [-76, -76,   0,], [-88, -85, -85,], [-88, -88, -88,], [-86, -87, -87,], [-88, -86, -86,], [-85, -86, -86,], [-69, -64, -64,], [-69, -62, -62,], [-69, -63, -63,], [-85, -83, -83,], [-69,   0,   0,], [  0, -76, -76,], [  0, -76, -88,], [  0, -88, -87,], [  0, -88, -86,], [  0, -87, -81,], [  0, -87, -82,], [  0, -86, -81,], [  0, -86, -75,], [  0, -81, -75,], [  0, -81, -80,], [  0, -82, -81,], [  0, -82, -81,], [  0, -81, -80,], [  0, -81, -81,], [  0, -75, -81,], [  0, -75, -81,], [  0, -75, -82,], [  0, -75, -82,], [  0, -79, -82,], [  0, -79, -82,], [  0, -78,   0,], [  0, -78,   0,], [  0, -78,   0,], [  0, -78,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -83,   0,]]);
#
#
# i=0; n=0;l=0
# x=[0,0,0.9]; y=[0,0.9,0.9]; z=[0,0,0]
# xrouter=[]; yrouter=[]; zrouter=[];sRouter=[]
# while i<len(names):
#     if quality[i][0]!=0 and quality[i][1]!=0 and quality[i][2]!=0:
#         wifi1=names[i]
#         r=[0]*3
#         #print(x,y,z)
#         for j in range(0,len(quality[i])):
#             qualitywifi1=quality[i][j]
#             r[j]=Distance(qualitywifi1)
#
#         try:
#             sol=(sc.root(equations3,(1,1,1),args=(x,y,z,r)))
#             if sol.success==True:
#                 xrouter.append(sol.x[0])
#                 yrouter.append(sol.x[1])
#                 zrouter.append(sol.x[2])
#                 sRouter.append(names[i])
#                 n=n+1
#                 #print(sol)
#         except:
#             ''
#     i=i+1
# print(xrouter,yrouter,zrouter,sRouter)

th=readwifi(0.0005,xrouter,yrouter,zrouter,sRouter)
th.start()
