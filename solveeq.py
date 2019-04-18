import scipy.optimize as sc
import math
import time
from numpy import sqrt
from sympy import *
from sympy.abc import x,y,z

# def equations(p):
#     r1,r2,r3 = p
#     eq1=
#     return (x+y**2-4, math.exp(x) + x*y - 3)

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

tic=time.process_time()
x=[0,1,1]; y=[0,0,1]; z=[0,0,0]; r1=[2,sqrt(5),sqrt(2)]; r2=[2,sqrt(5),sqrt(10)]; r3=[sqrt(5),2,sqrt(5)];
#x1,x2,x3,y1,y2,y3,z1,z2,z3 =  sc.fsolve(equations,(0,0,0,0,0,0,0,0,0),args=(x,y,z,r1,r2,r3))#,xtol=1e-8,maxfev=100)
sol=(sc.root(equations,(10,10,10,10,10,10,10,10,10),args=(x,y,z,r1,r2,r3)))

toc=time.process_time()
print(sol.x,sol.success)
#print((x1,x2,x3,y1,y2,y3,z1,z2,z3),toc-tic)
