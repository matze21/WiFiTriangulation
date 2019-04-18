from tkinter import *
import subprocess
import time
from scipy.optimize import fsolve
import math
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties


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
RSSI1m=-50
Envfactor=3

def Distance(quality,A,n):	#Rssi = requency A=35 n=2
	RSSI=quality/2-100
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
			print('a')
			#text.insert(END,"Finished")
			text.pack()
			root.after(int(interval*100000), lambda: root.destroy())
			root.mainloop()

class readwifi(threading.Thread):
	def __init__(self,interval,RSSI1m,Envfactor):
		#self.root = Tkinter.Tk()
		self.interval=interval
		self.RSSI1m=RSSI1m
		self.Envfactor=Envfactor
		super(readwifi, self).__init__()


	def run(self):


		RSSI1m=self.RSSI1m
		Envfactor=self.Envfactor
		names=[]
		quality=[]
		measurementindex=0
		t_end=time.time()+10
		while time.time()<t_end:
		#while True:
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
					dict_wifi[i].append(str(cells[i][0])+':'+str(cells[i][1]))	#namre
					dict_wifi[i].append(cells[i][4])	#channel
					dict_wifi[i].append(cells[i][2])	#signal
					dict_wifi[i].append(str(Distance(int(cells[i][2]),RSSI1m,Envfactor)))



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
			print(measurementindex)
			#time.sleep(5)

			measurementindex=measurementindex+1

			#displaydata(dict_wifi,self.interval,'robolabwifi','controlslab','rc_car')
			#displaydata(dict_wifi,self.interval*10,'','','')
			#wifi names robolabwifi controlslab rc_car

		#take matrix transpose
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
		print((quality1),names)
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
		#print(quality1,'/n',names)
#




th=readwifi(0.005,RSSI1m,Envfactor)
th.start()
