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

# def Distance(quality,A,n):	#Rssi = requency A=35 n=2
# 	#RSSI=quality/2-100
#     RSSI=quality
#     aux=RSSI-A
#     aux=(-1)*aux
#     aux=float(aux)/(10*n)
#     x=math.pow(10,aux)
#     return x
def Distance(quality):	#Rssi = requency A=35 n=2
	#RSSI=quality/2-100
#    if int(quality)<-50:                  #behind wall
    #   RSSI1m=-30; Envfactor=4
    # elif int(quality)<-70:
    RSSI1m=-50; Envfactor=4
    # else:
    #     RSSI1m=-22; Envfactor=3
    A=RSSI1m; n=Envfactor
    RSSI=quality
    aux=RSSI-A
    aux=(-1)*aux
    aux=float(aux)/(10*n)
    x=math.pow(10,aux)
    return x


names= ['58:6D:8F:88:29:EF:0', 'FA:8F:CA:6A:02:85:"dsl"', '24:F5:A2:41:FF:B1:"Office TV.v"', '14:91:82:72:58:7F:"rc_car"', '38:17:C3:AF:C5:30:"VRL"', '38:17:C3:AF:C5:31:"eduroam"', '38:17:C3:AF:C5:32:"UCSB Setup"', '38:17:C3:AF:C5:33:"UCSB Wireless Web"', 'C0:C1:C0:DC:4B:05:"UCSB Secure"', '24:F5:A2:41:FF:B2:"robolabwifi"', '38:17:C3:AF:AA:12:"rc_car_5GHz"', '38:17:C3:AF:AA:13:"UCSB Wireless Web"', '38:17:C3:AF:AA:10:"UCSB Secure"', 'E0:91:F5:C8:10:3F:"eduroam"', 'C0:C1:C0:DC:4B:04:""', '38:17:C3:AB:70:62:"robolabwifi"', '38:17:C3:AB:70:63:"UCSB Wireless Web"', '38:17:C3:AF:C3:B0:"UCSB Secure"', 'B8:09:8A:DA:C2:E7:"eduroam"', '88:63:DF:A8:48:11:"Soorya\\xE2\\x80\\x99s iMac"', '38:17:C3:EC:CA:40:"Mohammed\'s iMac"', '38:17:C3:EC:CA:41:"eduroam"', '38:17:C3:EC:CA:42:"UCSB Setup"', '38:17:C3:EC:CA:43:"UCSB Wireless Web"', '38:17:C3:AB:70:60:"UCSB Secure"', '38:17:C3:AB:70:61:"eduroam"', '38:17:C3:AF:C5:23:"UCSB Setup"', '88:63:DF:9F:CC:15:"UCSB Secure"', '28:F0:76:08:F6:84:"sina\'s iMac"', '38:17:C3:AF:C4:50:"Weiting\\xE2\\x80\\x99s iMac"', '38:17:C3:AF:C4:51:"eduroam"', '38:17:C3:AF:C4:52:"UCSB Setup"', '38:17:C3:AF:C4:53:"UCSB Wireless Web"', '38:17:C3:AF:C5:20:"UCSB Secure"', '38:17:C3:AF:C5:21:"eduroam"', '38:17:C3:AF:C5:22:"UCSB Setup"', '10:6F:3F:E8:83:3A:"UCSB Wireless Web"', '30:23:03:29:0E:47:"MOMENTLab"', '0:"controlslab"', '8A:15:04:BD:E1:7F:"controlslab"', '8A:15:04:BD:E1:74:"\\x00\\x00\\x00\\x00"', '8A:15:04:BD:E1:75:"\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"', '38:17:C3:AF:C3:A0:"\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"', '38:17:C3:AF:C3:A1:"eduroam"', '38:17:C3:AF:C3:A2:"UCSB Setup"', '38:17:C3:AF:AA:03:"UCSB Wireless Web"', '38:17:C3:AF:AA:00:"UCSB Secure"', '38:17:C3:AF:C3:B1:"eduroam"', '38:17:C3:AF:C3:B2:"UCSB Setup"', '38:17:C3:AF:C3:B3:"UCSB Wireless Web"', '38:17:C3:AF:C4:90:"UCSB Secure"', '38:17:C3:AF:C4:91:"eduroam"', '38:17:C3:AF:C4:92:"UCSB Setup"', '38:17:C3:AF:C4:93:"UCSB Wireless Web"', '38:17:C3:AB:70:70:"UCSB Secure"', '38:17:C3:AB:70:71:"eduroam"', '38:17:C3:AB:70:72:"UCSB Setup"', '38:17:C3:AB:70:73:"UCSB Wireless Web"', '38:17:C3:AF:AA:11:"UCSB Secure"', '0:"UCSB Setup"', '38:17:C3:AB:70:60:"eduroam"', '28:F0:76:08:F6:84:"UCSB Secure"', 'C8:E0:EB:27:4F:B3:"UCSB Setup"', '10:6F:3F:E8:83:3B:"Anant\\xE2\\x80\\x99s iMac"', 'B0:B8:67:CE:33:D1:"MOMENTLab_5GHz"', '38:17:C3:EC:CA:50:"UCSB Setup"', '38:17:C3:EC:CA:51:"eduroam"', '38:17:C3:EC:CA:52:"UCSB Setup"', '38:17:C3:EC:CA:53:"UCSB Wireless Web"', '0:"UCSB Secure"']

quality=np.array([[  0,   0,   0,], [-65, -72, -58,], [-56, -58, -61,], [-28, -31, -28,], [-52, -54, -54,], [-58, -57, -60,], [-57, -57, -60,], [-57, -57, -60,], [-58, -57, -60,], [-49, -50, -48,], [-34, -32, -35,], [-77, -77, -77,], [-78, -77, -77,], [-77, -77, -77,], [-51, -42, -47,], [-35, -35, -31,], [-77, -77, -85,], [-77, -77, -84,], [-78, -78,   0,], [-68, -68,   0,], [-75, -75,   0,], [-78, -78,   0,], [-78, -78,   0,], [-78, -78,   0,], [-78, -78,   0,], [-77, -77, -85,], [-77, -77, -85,], [-69, -64,   0,], [-76, -76,   0,], [-88, -85, -85,], [-88, -88, -88,], [-86, -87, -87,], [-88, -86, -86,], [-85, -86, -86,], [-69, -64, -64,], [-69, -62, -62,], [-69, -63, -63,], [-85, -83, -83,], [-69,   0,   0,], [  0, -76, -76,], [  0, -76, -88,], [  0, -88, -87,], [  0, -88, -86,], [  0, -87, -81,], [  0, -87, -82,], [  0, -86, -81,], [  0, -86, -75,], [  0, -81, -75,], [  0, -81, -80,], [  0, -82, -81,], [  0, -82, -81,], [  0, -81, -80,], [  0, -81, -81,], [  0, -75, -81,], [  0, -75, -81,], [  0, -75, -82,], [  0, -75, -82,], [  0, -79, -82,], [  0, -79, -82,], [  0, -78,   0,], [  0, -78,   0,], [  0, -78,   0,], [  0, -78,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -82,   0,], [  0, -83,   0,]]);

def equations(unknowns,x,y,z,r1,r2,r3):
#calibrated values
    xc1,xc2,xc3=x
    yc1,yc2,yc3=y
    zc1,zc2,zc3=z
    x1,x2,x3,y1,y2,y3,z1,z2,z3=unknowns
    eq1=r1[0]**2-(xc1-x1)**2-(yc1-y1)**2-(zc1-z1)**2
    eq2=r2[0]**2-(xc1-x2)**2-(yc1-y2)**2-(zc1-z2)**2
    eq3=r3[0]**2-(xc1-x3)**2-(yc1-y3)**2-(zc1-z3)**2
    eq4=r1[1]**2-(xc2-x1)**2-(yc2-y1)**2-(zc2-z1)**2
    eq5=r2[1]**2-(xc2-x2)**2-(yc2-y2)**2-(zc2-z2)**2
    eq6=r3[1]**2-(xc2-x3)**2-(yc2-y3)**2-(zc2-z3)**2
    eq7=r1[2]**2-(xc3-x1)**2-(yc3-y1)**2-(zc3-z1)**2
    eq8=r2[2]**2-(xc3-x2)**2-(yc3-y2)**2-(zc3-z2)**2
    eq9=r3[2]**2-(xc3-x3)**2-(yc3-y3)**2-(zc3-z3)**2
    return (eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9)

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


i=0; n=0;l=0
x=[0,0,0.9]; y=[0,0.9,0.9]; z=[0,0,0]
xrouter=[0,0,0]*30; yrouter=[0]; zrouter=[0];sRouter=[]
#print(xrouter[0][0])
tic=time.time()
while i<len(names):
    if quality[i][0]!=0 and quality[i][1]!=0 and quality[i][2]!=0:
        wifi1=names[i]
        r=[0]*3
        #print(x,y,z)
        for j in range(0,len(quality[i])):
            qualitywifi1=quality[i][j]
            r[j]=Distance(qualitywifi1)

        #try:
        sol=(sc.root(equations3,(1,1,1),args=(x,y,z,r)))
        if sol.success==True:
            xrouter.append(sol.x)
            yrouter.append(sol.x[1])
            zrouter.append(sol.x[2])
            sRouter.append(names[i])
            n=n+1
                #print(sol)
        # except:
        #     ''
    i=i+1
#print(xrouter,yrouter,zrouter,sRouter)
toc=time.time()
print('number of solutions',n, xrouter,tic, toc)
