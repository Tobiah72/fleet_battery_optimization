#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 16:57:29 2019

@author: tobysteckel

Improvements to make

- Make a .csv (excel input, more user friendly)
- Stochastic representiation
- Start creating more realistic value scenarios 
- Actual differentiation between performance of new and used
- Put in discount rate 

"""
import pulp
import csv

# Create Cost Coefficients 
#si, vs, sc, fr, pm, nb_t
#storage install, value of storage, service cost (B2U), fleet failure rate,
#performance multiplier, new battery cost f(t)
#si = 377  # low cost Storage installment including battery 
si = 604  # middle cost Storage installment including battery 
#si = 831  # high cost Storage installment including battery 
#vs = 10 # low value return from storage in year 
vs = 140 # middle value return from storage in year  
#vs = 269 # high value return from storage in year 
#sc = 20  # low value for B2U service cost 
sc = 30  # middle value for B2U service cost 
#sc = 40  # higher value for B2U service cost 
fr = .07     # percentage annual failure of fleets, percentage B2U capacity avaiable 
#pm = .7      # low percentage of performance/capacity multiplier for B2U
#pm = .75     # middle percentage of performance/capacity multiplier for B2U
pm = .8 # high percentage of performance/capacity multiplier for B2U
nb_1 = 230.62   # Battery price at given t
nb_2 = 219.63 # Battery price at given t
nb_3 = 211.85 # Battery price at given t
nb_4 = 205.69 # Battery price at given t
nb_5 = 200.87 # Battery price at given t
nb_6 = 197.05  # Battery price at given t
nb_7 = 193.88 # Battery price at given t
nb_8 = 191.16 # Battery price at given t
nb_9 = 188.78 # Battery price at given t
nb_10 = 186.68 # Battery price at given t


# Create decision variables , including slack variables 


#x1 = pulp.LpVariable.dicts("x1", df.index, lowBound=0)
#x_tj new battery for vehicle use 
x_11 = pulp.LpVariable("x_11", lowBound=0)
x_12 = pulp.LpVariable("x_12", lowBound=0)
x_13 = pulp.LpVariable("x_13", lowBound=0)
x_14 = pulp.LpVariable("x_14", lowBound=0)
x_15 = pulp.LpVariable("x_15", lowBound=0)
x_16 = pulp.LpVariable("x_16", lowBound=0)
x_17 = pulp.LpVariable("x_17", lowBound=0)
x_18 = pulp.LpVariable("x_18", lowBound=0)
x_19 = pulp.LpVariable("x_19", lowBound=0)
x_110 = pulp.LpVariable("x_1ten", lowBound=0)

#y_t installment of storage capacity with new battery 
y_1 = pulp.LpVariable("y_1", lowBound=0)
y_2 = pulp.LpVariable("y_2", lowBound=0)
y_3 = pulp.LpVariable("y_3", lowBound=0)
y_4 = pulp.LpVariable("y_4", lowBound=0)
y_5 = pulp.LpVariable("y_5", lowBound=0)
y_6 = pulp.LpVariable("y_6", lowBound=0)
y_7 = pulp.LpVariable("y_7", lowBound=0)
y_8 = pulp.LpVariable("y_8", lowBound=0)
y_9 = pulp.LpVariable("y_9", lowBound=0)
y_10 = pulp.LpVariable("y_ten", lowBound=0)

#z_t installment of storage capacity with old battery  
#z_1 = pulp.LpVariable("z_1", lowBound=0), only nine option not available until t=2 
z_2 = pulp.LpVariable("z_2", lowBound=0)
z_3 = pulp.LpVariable("z_3", lowBound=0)
z_4 = pulp.LpVariable("z_4", lowBound=0)
z_5 = pulp.LpVariable("z_5", lowBound=0)
z_6 = pulp.LpVariable("z_6", lowBound=0)
z_7 = pulp.LpVariable("z_7", lowBound=0)
z_8 = pulp.LpVariable("z_8", lowBound=0)
z_9 = pulp.LpVariable("z_9", lowBound=0)
z_10 = pulp.LpVariable("z_ten", lowBound=0)


# Slack Variables for constraints
#No duty constraints for now , just for ease of running 
s1 = pulp.LpVariable("s_1", lowBound=0) # Duty constraint slack variables 
s2 = pulp.LpVariable("s_2", lowBound=0)
s3 = pulp.LpVariable("s_3", lowBound=0)
s4 = pulp.LpVariable("s_4", lowBound=0)
s5 = pulp.LpVariable("s_5", lowBound=0)
s6 = pulp.LpVariable("s_6", lowBound=0)
s7 = pulp.LpVariable("s_7", lowBound=0)
s8 = pulp.LpVariable("s_8", lowBound=0)
s9 = pulp.LpVariable("s_9", lowBound=0)
s10 = pulp.LpVariable("s_ten", lowBound=0)
s11 = pulp.LpVariable("Overbuild s", lowBound=0)     #Overbuild constraint slack variables
s12 = pulp.LpVariable("yr2 B2U s", lowBound=0)      # B2U procurement constraint, only nine option not available until t=2 
s13 = pulp.LpVariable("yr3 B2U s", lowBound=0)
s14 = pulp.LpVariable("yr4 B2U s", lowBound=0)
s15 = pulp.LpVariable("yr5 B2U s", lowBound=0)
s16 = pulp.LpVariable("yr6 B2U s", lowBound=0)
s17 = pulp.LpVariable("yr7 B2U s", lowBound=0)
s18 = pulp.LpVariable("yr8 B2U s", lowBound=0)
s19 = pulp.LpVariable("yr9 B2U s", lowBound=0)
s20 = pulp.LpVariable("yrten B2U s", lowBound=0)
#Annual Spending Capacity constraint slack 
s21 = pulp.LpVariable("yr1 spending s", lowBound=0)     #Overbuild constraint slack variables
s22 = pulp.LpVariable("yr2 spending s", lowBound=0)      # B2U procurement constraint, only nine option not available until t=2 
s23 = pulp.LpVariable("yr3 spending s", lowBound=0)
s24 = pulp.LpVariable("yr4 spending s", lowBound=0)
s25 = pulp.LpVariable("yr5 spending s", lowBound=0)
s26 = pulp.LpVariable("yr6 spending s", lowBound=0)
s27 = pulp.LpVariable("yr7 spending s", lowBound=0)
s28 = pulp.LpVariable("yr8 spending s", lowBound=0)
s29 = pulp.LpVariable("yr9 spending s", lowBound=0)
s30 = pulp.LpVariable("yrten spending s", lowBound=0)

problem = pulp.LpProblem("Total cost", pulp.LpMinimize)

# Objective function
# yr1 contributions to overall cost
# yr1r returns, or negative contribution to overall cost 
yr1 = nb_1 * (x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + (y_1 * si)
yr2 = (fr *(nb_2 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_2 * (si - nb_1 + nb_2)) + z_2 * (si + sc - nb_1)  
yr2r = (vs * y_1) # t-1
yr3 = (fr *(nb_3 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_3 * (si - nb_1 + nb_3)) + z_3 * (si + sc - nb_1)  
yr3r = (vs * (y_1 + y_2)) + (pm*vs)*(z_2)
yr4 = (fr *(nb_4 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_4 * (si - nb_1 + nb_4)) + z_4 * (si + sc - nb_1)  
yr4r = (vs * (y_1 + y_2 + y_3)) + (pm*vs)*(z_2 + z_3)
yr5 = (fr *(nb_5 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_5 * (si - nb_1 + nb_5)) + z_5 * (si + sc - nb_1)  
yr5r = (vs * (y_1 + y_2 + y_3 + y_4)) + (pm*vs)*(z_2 + z_3 + z_4)
yr6 = (fr *(nb_6 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_6 * (si - nb_1 + nb_6)) + z_6 * (si + sc - nb_1)  
yr6r = (vs * (y_1 + y_2 + y_3 + y_4 + y_5)) + (pm*vs)*(z_2 + z_3 + z_4 + z_5)
yr7 = (fr *(nb_7 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_7 * (si - nb_1 + nb_7)) + z_7 * (si + sc - nb_1)  
yr7r = (vs * (y_1 + y_2 + y_3 + y_4 + y_5 + y_6)) + (pm*vs)*(z_2 + z_3 + z_4 + z_5 + z_6)
yr8 = (fr *(nb_8 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_8 * (si - nb_1 + nb_8)) + z_8 * (si + sc - nb_1)  
yr8r = (vs * (y_1 + y_2 + y_3 + y_4 + y_5 + y_6 + y_7)) + (pm*vs)*(z_2 + z_3 + z_4 + z_5 + z_6+ z_7)
yr9 = (fr *(nb_9 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_9 * (si - nb_1 + nb_9)) + z_9 * (si + sc - nb_1)  
yr9r = (vs * (y_1 + y_2 + y_3 + y_4 + y_5 + y_6 + y_7+ y_8)) + (pm*vs)*(z_2 + z_3 + z_4 + z_5 + z_6+ z_7+ z_8)
yr10 = (fr *(nb_10 *(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110))) + (y_10 * (si - nb_1 + nb_10)) + z_10 * (si + sc - nb_1)  
yr10r = (vs *(y_1 + y_2 + y_3 + y_4 + y_5 + y_6 + y_7+ y_8 + y_9)) + (pm*vs)*(z_2 + z_3 + z_4 + z_5 + z_6+ z_7+ z_8 + z_9)


problem += yr1 + yr2 - yr2r + yr3 - yr3r + yr4 - yr4r + yr5 - yr5r + yr6 - yr6r + yr7 - yr7r + yr8 - yr8r + yr9 - yr9r + yr10 - yr10r , "Z"



# Constraints
# Duty constraint
problem += x_11 - s1 == 300  # in kW
problem += x_12 - s2 == 300 
problem += x_13 - s3 == 400 
problem += x_14 - s4 == 200
problem += x_15 - s5 == 200 
problem += x_16 - s6 == 300 
problem += x_17 - s7 == 40
problem += x_18 - s8 == 10
problem += x_19 - s9 == 300 
problem += x_110 - s10 == 300 

# Overbuild constraint
problem += (y_1 + y_2 + y_3 + y_4 + y_5 + y_6 + y_7 + y_8 + y_9 + y_10) + (z_2 + z_3 + z_4 + z_5 + z_6 + z_7 + z_8 + z_9 + z_10)- (.5*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110)) + s11 == 0

# B2U procurement constraint
problem += z_2  - fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s12 == 0
problem += (z_2 + z_3)  - 2*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s13 == 0
problem += (z_2 + z_3 + z_4)  - 3*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s14 == 0
problem += (z_2 + z_3 + z_4 + z_5)  - 4*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s15 == 0
problem += (z_2 + z_3 + z_4 + z_5 + z_6)  - 5*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s16 == 0
problem += (z_2 + z_3 + z_4 + z_5 + z_6 + z_7)  - 6*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s17 == 0
problem += (z_2 + z_3 + z_4 + z_5 + z_6 + z_7 + z_8)  - 7*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s18 == 0
problem += (z_2 + z_3 + z_4 + z_5 + z_6 + z_7 + z_8 + z_9)  - 8*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s19 == 0
problem += (z_2 + z_3 + z_4 + z_5 + z_6 + z_7 + z_8 + z_9 + z_10)  - 9*fr*(x_11 + x_12 + x_13 + x_14 + x_15 + x_16 + x_17 + x_18 + x_19 + x_110) + s20 == 0

# Annual spending constraints, Sensitivity 

problem += (yr1 - 600000) + s21 == 0 
problem += (yr2 - 600000) + s22 == 0 
problem += (yr3 - 600000) + s23 == 0 
problem += (yr4 - 600000) + s24 == 0 
problem += (yr5 - 600000) + s25 == 0 
problem += (yr6 - 600000) + s26 == 0 
problem += (yr7 - 600000) + s27 == 0 
problem += (yr8 - 600000) + s28 == 0 
problem += (yr9 - 600000) + s29 == 0 
problem += (yr10 - 600000) + s30 == 0 


problem.solve()

#Gives objective, subject to etc. 
print(problem)

#Identifying status of problem (i.e. not solved, optimal, infeasible, unbounded)
print(pulp.LpStatus[problem.status])

#identifying optimal result (i.e. Z =)
print(pulp.value(problem.objective))

#identifying variables in optimal solution

var_name_list = ['Variable name']
var_value_list = ['Value']
seg1 = ['Vehicle capacity']
seg1_v = ['Value'] 
seg2 = ['New storage Capacity']
seg2_v = ['Value'] 
seg3 = ['Used storage Capacity']
seg3_v = ['Value'] 
seg4 = ['Overbuild slack']
seg4_v = ['Value'] 
seg5 = ['Vehicle capacity slack']
seg5_v = ['Value'] 
seg6 = ['Used procurement slack']
seg6_v = ['Value'] 
seg7 = ['Annual spending slack']
seg7_v = ['Value'] 

    
for variable in problem.variables():
    print("{} = {}".format(variable.name, variable.varValue))
    #var_name_list.append((variable.name + ' ' + str(variable.varValue)))
    var_name_list.append((variable.name))
    var_value_list.append((variable.varValue))
    if 'x_' in variable.name:
        seg1.append((variable.name))
        seg1_v.append((variable.varValue))
    if 'y_' in variable.name:
        seg2.append((variable.name))
        seg2_v.append((variable.varValue))
    if 'z_' in variable.name:
        seg3.append((variable.name))
        seg3_v.append((variable.varValue))
    if 'Overbuild' in variable.name:
        seg4.append((variable.name))
        seg4_v.append((variable.varValue))
    if 's_' in variable.name:
        seg5.append((variable.name))
        seg5_v.append((variable.varValue))
    if 'B2U' in variable.name:
        seg6.append((variable.name))
        seg6_v.append((variable.varValue))
    if 'spending' in variable.name:
        seg7.append((variable.name))
        seg7_v.append((variable.varValue))
    
   
#for name, c in list(problem.constraints.items()):
#    print(name, ":", c, "\t", c.pi, "\t\t", c.slack)
    
#print (si*1856, nb_1*2350, "837000", 9*vs*1856)
#print (var_name_list)
        
'''here we output csv of particular dvs over planning horizon'''

with open('Table5.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(["Table 5"])
    writer.writerows([seg1])
    writer.writerows([seg1_v])
    writer.writerows([seg2])
    writer.writerows([seg2_v])
    writer.writerows([seg3])
    writer.writerows([seg3_v])
    writer.writerows([seg4])
    writer.writerows([seg4_v])
    writer.writerows([seg5])
    writer.writerows([seg5_v])
    writer.writerows([seg6])
    writer.writerows([seg6_v])
    writer.writerows([seg7])
    writer.writerows([seg7_v])
