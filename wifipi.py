#jioFi  [5,10]
#anvesh [-5,10]
#2F [20,25]

cells=[]
dict_wifi={}
for i in range(0,20):
	dict_wifi[i]=[]



import subprocess
#Process=subprocess.Popen(["iwlist","wlp2s0","scan"],stdout=subprocess.PIPE,universal_newlines=True)
Process=subprocess.Popen(["iwlist","wlan0","scan"],stdout=subprocess.PIPE,universal_newlines=True)
out,err=Process.communicate()
print(out)
new_l=out.split('\n')
#print (new_l)

for line in new_l:
	line=line.lstrip()
	line=line.rstrip()
	if line.startswith("Cell"):
		line1=line.split()
	#	print line1[4]
		cells.append(line1[4]) #address

	if line.startswith("Channel"):
		line3=line.split(":")
	#	print line3[1]
		cells.append(line3[1]) #channel
	if line.startswith("Frequency"):
		line4=line.split(":")
		k=line4[1].split(' ')
#		print k[0]
		cells.append(k[0])
	if line.startswith("Quality"):
		line5=line.split()
		#line6=line.split(' ')
		#line5=line.split("=")
		line6=line5[2].split("=")
	#	print line6[1]
		cells.append(line6[1]) #quality
	if line.startswith("ESSID"):
		line2=line.split(":")
	#	print line2[1]
		cells.append(line2[1]) #name
print (cells)
cells.reverse()
#print cells
