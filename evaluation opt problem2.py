# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 17:10:18 2020

@author: 12259
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:25:16 2020

@author: 12259
"""

import numpy as np
from io import StringIO
from gurobipy import *

#model name
model = gurobipy.Model("Evaluation")
#import credit file
with open("a.txt") as f:
    data = f.read()
A=np.genfromtxt(StringIO(data), delimiter = '	')

for i in range(199):
    for j in range(25):
        if A[i,j]==4:
            A[i,j]=1

##build model

#problem formulation
x={}
y={}
z={}
y1={}
y2={}
z1={}
z2={}
xmax={}
xmin={}
I=range(25)
J=range(199)
M=30

xmax=model.addVar(vtype ='C')

xmin=model.addVar(vtype ='C')
for i in I:
    x[i]=model.addVar(vtype ='C')
for j in J:
    y[j]=model.addVar(vtype ='B')
    z[j]=model.addVar(vtype ='B')
    y1[j]=model.addVar(lb=- GRB.INFINITY,vtype ='C')
    z1[j]=model.addVar(lb=- GRB.INFINITY,vtype ='C')
    y2[j]=model.addVar(lb=- GRB.INFINITY,vtype ='C')
    z2[j]=model.addVar(lb=- GRB.INFINITY,vtype ='C')

for i in I:
    model.addConstr(x[i]>=xmin)
    model.addConstr(x[i]<=xmax)

model.addConstr(quicksum(x[i] for i in I)==100)

for j in J:
    model.addConstr(y2[j]==quicksum(A[j,i]*x[i] for i in I)-79)
    model.addConstr(y1[j]==max_(y2[j],0))
    model.addConstr(M*y[j]>=y1[j])
    model.addConstr(y[j]<=y1[j])
    model.addConstr(z2[j]==quicksum(A[j,i]*x[i] for i in I)-89)
    model.addConstr(z1[j]==max_(z2[j],0))
    model.addConstr(M*z[j]>=z1[j])
    model.addConstr(z[j]<=z1[j])

model.addConstr(quicksum(z[j] for j in J)<=0.5*quicksum(y[j] for j in J))
model.addConstr(quicksum(y[j] for j in J)-199*0.4>=-5)
model.addConstr(quicksum(y[j] for j in J)-199*0.4<=0)

model.setObjective(xmax-xmin, sense = GRB.MINIMIZE)


model.optimize()

for i in I:
    print(x[i].X)