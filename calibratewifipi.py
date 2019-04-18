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


def equations9(unknowns,x,y,z,r1,r2,r3):
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
    eq8=r2[2]**2 -(xc3-x2)**2-(yc3-y2)**2-(zc3-z2)**2
    eq9=r3[2]**2-(xc3-x3)**2-(yc3-y3)**2-(zc3-z3)**2
    return (eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9)

def equations3(unknowns,x,y,z,r1,r2,r3):
#calibrated values
    xc1,xc2,xc3=x
    yc1,yc2,yc3=y
    zc1,zc2,zc3=z
    x1,y1,z1=unknowns
    eq1=r1[0]**2-(xc1-x1)**2-(yc1-y1)**2-(zc1-z1)**2
    eq4=r1[1]**2-(xc2-x1)**2-(yc2-y1)**2-(zc2-z1)**2
    eq7=r1[2]**2-(xc3-x1)**2-(yc3-y1)**2-(zc3-z1)**2
    return (eq1,eq4,eq7)

def match(line,keyword):
	line=line.lstrip()
	length=len(keyword)
	if line[:length] == keyword:
		return line[length:]
	else:
		return None


#RSSI=-10*n*log(d)+A
#A=-35dBm Signal Strength At 1 meter
#n=2.7 Path Loss Exponent
#RSSI1m=-22
#Envfactor=int(input('environment factor '))

def Distance(quality,A,n):	#Rssi = requency A=35 n=2
	#RSSI=quality/2-100
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

def findallrouters():
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
            dict_wifi[i].append(cells[i][3])	#name
            dict_wifi[i].append(cells[i][2])	#quality
            if int(cells[i][2])<-50:                  #behind wall
                RSSI1m=-30; Envfactor=4
            else:
                RSSI1m=-22; Envfactor=3
            dict_wifi[i].append(str(Distance(int(cells[i][2]),RSSI1m,Envfactor)))
    return cells,dict_wifi


class readwifi(threading.Thread):
    def __init__(self,interval):
		#self.root = Tkinter.Tk()
        self.interval=interval
        #self.RSSI1m=RSSI1m
        #self.Envfactor=Envfactor
        super(readwifi, self).__init__()
    def run(self):
        #RSSI1m=self.RSSI1m
        #Envfactor=self.Envfactor
        measurementindex=0
        x=[0]*3
        y=[0]*3
        z=[0]*3
        while measurementindex<=2: #3 points
            x[measurementindex]=input('x ')
            y[measurementindex]=input('y ')
            z[measurementindex]=input('z ')
            cells,dict_wifi=findallrouters()
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
                # x.append(float(input('x ')))
                # y.append(float(input('y ')))
                # z.append(float(input('z ')))
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

        i=0
        xrouter=[0]*len(names); yrouter=xrouter; zrouter=xrouter;
        while i<len(names):
            if len(names)<3:
                print('not enough networks')
                break
            if len(names)-i<3:              #use 3rd last wifi to calculate location if #wifis not divideable through 3
                i=i-(3-(len(names)-i))
                #print(i,len(names))
            wifi1=names[i]
            wifi2=names[i+1]
            wifi3=names[i+2]
            r1=[0]*3 ; r2=[0]*3; r3=[0]*3;
            #print(quality1[i])
            for j in range(0,len(quality1[i])):
                qualitywifi1=quality1[i][j]
                qualitywifi2=quality1[i+1][j]
                qualitywifi3=quality1[i+2][j]
                if int(qualitywifi1)<-50:                  #behind wall
                    RSSI1m=-30; Envfactor=4
                else:
                    RSSI1m=-22; Envfactor=3
                r1[j]=Distance(qualitywifi1,RSSI1m,Envfactor)
                if int(qualitywifi2)<-50:                  #behind wall
                    RSSI1m=-30; Envfactor=4
                else:
                    RSSI1m=-22; Envfactor=3
                r2[j]=Distance(qualitywifi2,RSSI1m,Envfactor)
                if int(qualitywifi3)<-50:                  #behind wall
                    RSSI1m=-30; Envfactor=4
                else:
                    RSSI1m=-22; Envfactor=3
                r3[j]=Distance(qualitywifi3,RSSI1m,Envfactor)
            try:
                sol=(sc.root(equations,(10,10,10,10,10,10,10,10,10),args=(x,y,z,r1,r2,r3)))
                xrouter[i]=sol.x[0]
                xrouter[i+1]=sol.x[1]
                xrouter[i+2]=sol.x[2]
                yrouter[i]=sol.x[3]
                yrouter[i+1]=sol.x[4]
                yrouter[i+2]=sol.x[5]
                zrouter[i]=sol.x[6]
                zrouter[i+1]=sol.x[7]
                zrouter[i+2]=sol.x[8]
                print(names[i],xrouter[i],yrouter[i],zrouter[i],'\n')
                print(names[i+1],xrouter[i+1],yrouter[i+1],zrouter[i+1],'\n')
                print(names[i+2],xrouter[i+2],yrouter[i+2],zrouter[i+2],'\n')
            except:
                print('no solution found')
                print(names[i],r1[0],r1[1],r1[2],quality1[i][0],quality1[i][1],quality1[i][2],'\n')
                print(names[i+1],r2[0],r2[1],r2[2],quality1[i+1][0],quality1[i+1][1],quality1[i+1][2],'\n')
                print(names[i+2],r3[0],r3[1],r3[2],quality1[i+2][0],quality1[i+2][1],quality1[i+2][2],'\n')
            i=i+3












# 		print(np.shape(quality1),len(quality1))
# 		ax=plt.subplot(111)
# 		#print(quality1)
# 		for i in range(0,len(quality1)):
# 			#print(names[i])
# 		 	line,=ax.plot(range(0,len(quality1[0])),quality1[i],label=str(names[i]))
#
# 		box = ax.get_position()
# 		ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# # Put a legend below current axis
# 		#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# 		ax.legend(loc='center left', bbox_to_anchor=(1, 0.5) ,prop={'size':6})
# 		plt.show()
# 		#print(quality1,'/n',names)





th=readwifi(0.0005)
th.start()
