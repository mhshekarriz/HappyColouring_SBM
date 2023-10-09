#!/usr/bin/python
from gurobipy import *
import math, argparse, time
import aco as aco
import random
# Display some information
def display(x,y,vertices,model):
    # Display some solution information
    usum = 0
    hsum = 0
    for i in range(vertices):
        name  = "x_"+str(i)
        x_var = model.getVarByName(name)
        print ("V " + str(i+1) + ": " + str(x_var.X) + ", connections: ", end="")
        count = 0
        for j in range(vertices):
            if mat[i][j] == 1:
                name  = "x_"+str(j)
                x_v = model.getVarByName(name)
                if count == 0:
                    print ("(" + str(j+1) + "," + str(x_v.X) + ") ",end="") 
                else:
                    print (",(" + str(j+1) + "," + str(x_v.X) + ") ",end="") 
                count += 1
        name  = "y_"+str(i)
        y_var = model.getVarByName(name)
        if y_var.X > 0.01:
            print ("\nV " + str(i+1) + " is unhappy") 
            usum+=1
        else:
            print ("\nV " + str(i+1) + " is happy") 
            hsum+=1
    print("Happy vertices: " + str(hsum) + " unhappy vertices: " + str(usum))

# Display some information for the second model
# Colours is also needed as an inout here
def display_mod2(x,y,vertices,colours,model):
    # Display some solution information
    usum = 0
    hsum = 0
    for i in range(vertices):
        for k in range(colours):
            name  = "x_"+str(i)+"_"+str(k)
            x_var = model.getVarByName(name)
            if x_var.X > 0.5:
                print ("V " + str(i+1) + ": " + str(x_var.X) + ", connections: ", end="")
        count = 0
        for j in range(vertices):
            if mat[i][j] == 1:
                for k in range(colours):
                    name  = "x_"+str(i)+"_"+str(k)
                    x_v = model.getVarByName(name)
                    if x_v.X > 0.5:
                        if count == 0:
                            print ("(" + str(j+1) + "," + str(x_v.X) + ") ",end="") 
                        else:
                            print (",(" + str(j+1) + "," + str(x_v.X) + ") ",end="") 
                count += 1
        name  = "y_"+str(i)
        y_var = model.getVarByName(name)
        if y_var.X > 0.01:
            print ("\nV " + str(i+1) + " is unhappy") 
            usum+=1
        else:
            print ("\nV " + str(i+1) + " is happy") 
            hsum+=1
    print("Happy vertices: " + str(hsum) + " unhappy vertices: " + str(usum))


# Solve the happy colouring problem with the first model
def solve(vertices, colours, mat, cv):
    model = Model("HappyColourings-Model")
    model.setParam(GRB.Param.TimeLimit, 600)
    model.setParam(GRB.Param.Threads, 1)
    x = [] # vector of integer variables, which colour is assigned to vertex i 
    y = [] # vector of binary variables, 1 if not happy
    for i in range(vertices):
        y.append(model.addVar(vtype=GRB.BINARY, name="y_"+str(i)))
        x.append(model.addVar(vtype=GRB.INTEGER, lb=0, ub=vertices, name="x_"+str(i)))
    model.update()

    # Constraints
    # Set the colours for the known vertices
    for i in range(vertices):
        if cv[i] >= 0:
            model.addConstr(x[i] == cv[i], "")
    model.update()
    
    #Mapping between x and y 
    for i in range(vertices):
        diff = model.addVar(vtype=GRB.INTEGER, lb=0, ub=vertices, name="diff")
        model.update()
        for j in range(vertices):
            if mat[i][j] != 1:
                continue
            model.addConstr(diff >= x[i]-x[j], "")
            model.addConstr(diff >= x[j]-x[i], "")
        model.addConstr(y[i] >= diff/vertices, "")
    model.update()

    # Objective
    tot = 0
    for i in range(vertices):
        tot += y[i]
    model.setObjective(tot,GRB.MINIMIZE)
    model.update()
    model.optimize()
    display(x,y,vertices,model)

# Solve the happy colouring problem with the second model
def solve_mod2(vertices, colours, mat, cv):
    model = Model("HappyColourings-Model")
    model.setParam(GRB.Param.TimeLimit, 600)
    model.setParam(GRB.Param.Threads, 1)
    x = [] # vector of integer variables, which colour is assigned to vertex i 
    y = [] # vector of binary variables, 1 if not happy
    for i in range(vertices):
        y.append(model.addVar(vtype=GRB.BINARY, name="y_"+str(i)))
        xt = []
        for j in range(colours):
            xt.append(model.addVar(vtype=GRB.BINARY, name="x_"+str(i)+"_"+str(j)))
        x.append(xt)
    model.update()

    # Constraints
    # Set the colours for the known vertices
    # Also have to ensure only one colour is selected
    for i in range(vertices):
        j = cv[i]
        if j >= 0:
            model.addConstr(x[i][j] == 1, "")
        stot = 0
        for k in range(colours):
            stot += x[i][k]
        model.addConstr(stot == 1, "")
    model.update()
    
    #Mapping between x and y 
    for i in range(vertices):
        diff = model.addVar(vtype=GRB.INTEGER, lb=0, ub=vertices, name="diff")
        model.update()
        for j in range(vertices):
            if mat[i][j] != 1:
                continue
            for k in range(colours):
                model.addConstr(diff >= x[i][k]-x[j][k], "")
                model.addConstr(diff >= x[j][k]-x[i][k], "")
        model.addConstr(y[i] >= diff, "")
    model.update()

    # Objective
    tot = 0
    for i in range(vertices):
        tot += y[i]
    model.setObjective(tot,GRB.MINIMIZE)
    model.update()
    model.optimize()
    display_mod2(x,y,vertices,colours,model)

# Solve Zhang's algorithm
# Assuming weights (w) are 1
def solve_Zhang(vertices, colours, mat, cv):
    print("Solving by Zhang's method")
    model = Model("HappyColourings-Model-Zhang")
    model.setParam(GRB.Param.TimeLimit, 600)
    # Here 0 is not happy and 1 is happy
    xi = [] # is vertex v happy by a colouring of colour i
    yi = [] # is vertex v coloured i
    x = [] # vector of binary variables, 1 if not happy
    for i in range(vertices):
        x.append(model.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub =1, name="x_"+str(i)))
        xt = []
        yt = []
        for j in range(colours):
            xt.append(model.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub = 1, name="xi_"+str(i)+"_"+str(j)))
            yt.append(model.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub = colours, name="yi_"+str(i)+"_"+str(j)))
        xi.append(xt)
        yi.append(yt)
    model.update()

    # Each vertex must be coloured and have only one colour
    for i in range(vertices):
        stot = 0
        for j in range(colours):
            stot += yi[i][j]
        model.addConstr(stot == 1, "")

    # Pre-defined colours
    # Set the colours for the known vertices
    for i in range(vertices):
        if cv[i] >= 0:
            model.addConstr(yi[i][cv[i]] == 1, "")

    # Mapping between xi and yi
    for i in range(vertices):        
        for j in range(colours):
            for u in range(vertices):        
                if mat[i][u] > 0:
                    model.addConstr(xi[i][j] <= yi[u][j], "")

    # A modelling trick to do the above more accurately
    # Need to work on this
    #for i in range(vertices):        
    #    for j in range(colours):
    #        for u in range(vertices):        
    #            if mat[i][u] > 0:
    #                w = model.addVar(vtype=GRB.BINARY, name="xi_"+str(i)+"_"+str(j)+"_"+str(u)))
    #                model.addConstr(xi[i][j] >= yi[u][j]+(), "")


    # Mapping between x and xi
    for i in range(vertices):
        stot = 0
        for j in range(colours):
            stot += xi[i][j]
        model.addConstr(stot == x[i], "")
    # Objective
    tot = 0
    for i in range(vertices):
        tot += x[i]
    model.setObjective(tot,GRB.MINIMIZE)
    model.update()
    model.optimize()
    # Now compute a proper colouring
    vertex_colours = []
    for i in range(vertices):
        vertex_colours.append(-1)
    vertex_left = 1
    while vertex_left == 1:
        for i in range(vertices):
            if vertex_colours[i] != -1: continue
            j = random.randint(0,range(colours)-1)
            name  = "yi_"+str(i)+"_"+str(j)
            y_var = model.getVarByName(name)
            rho = random.random()
            if y_var.X > rho:
                vertex_colours[i] = j
        # Check if the vertices are complete
        done = 1
        for i in range(vertices):
            if vertex_colours[i] == -1: 
                done = 0
                break
        if done == 1:
            vertex_left = 0
                
            
            
# Read the input file
def read_file(fileName):
    vertices = -1
    colours = -1
    mat = []
    cv = []

    oFile = open(fileName, 'r')
    lines = oFile.readlines()
    l = lines[0].split(" ")
    vertices = int(l[0])
    colours = int(l[1])
    # get the vertices and their colours
    l = lines[1].split(" ") 
    for i in range(vertices):
        cv.append(int(l[i]))

    k = 2
    for i in range(vertices):
        l = lines[k].split(" ")
        mat.append([])
        for j in range(vertices):
            mat[i].append(int(l[j]))
        k+=1
    #print(cv)
    #print(mat)
    return (vertices,colours,mat,cv)


# Read the input file
def read_DIMACS(fileName):
    vertices = -1
    colours = -1
    edges = -1
    mat = []
    cv = []

    oFile = open(fileName, 'r')
    lines = oFile.readlines()
    for line in lines:
        # A comment
        if line.startswith('c'):
            continue
        # high-level data
        if line.startswith('p'):
            l = line.split(" ")
            vertices = int(l[2])
            edges = int(l[3])
            colours = int(l[4])

            # Initialise some data structure
            for i in range(vertices):
                cv.append(-1)

            for i in range(vertices):
                mat.append([])
                for j in range(vertices):
                    if i==j:
                        mat[i].append(-1)
                    else:
                        mat[i].append(0)        
        # read in the edges
        if line.startswith('e'):
            l = line.split(" ")
            e1 = int(l[1])-1
            e2 = int(l[2])-1
            mat[e1][e2] = 1
            mat[e2][e1] = 1
        # read in the vertex colours
        if line.startswith('n'):
            l = line.split(" ")
            v = int(l[1])-1
            c = int(l[2])-1
            cv[v] = c
    #print(cv)
    #print(mat)
    return (vertices,colours,mat,cv)

# The main file starts here
ap = argparse.ArgumentParser()
ap.add_argument('--input', type=str,
    help='''The input file from which the problem data will be extracted.''')
ap.add_argument('--model', type=str,
    help='''Which model to use when optimising.''')
ap.add_argument('--meth', type=str,
    help='''What method to use, MIP or ACO.''')
ap.add_argument('--rtime', type=str,
    help='''What method to use, MIP or ACO.''')

args = ap.parse_args()
fileName = args.input
model = args.model
method = args.meth
rtime = float(args.rtime)

start_time=time.clock()
#(vertices,colours,mat,cv)=read_file(fileName)
(vertices,colours,mat,cv)=read_DIMACS(fileName)
if method == "aco":
    aco.ExeACO(vertices, colours, mat, cv, start_time, rtime)
else:
    if model == "1":
        solve(vertices, colours, mat, cv)
    elif model == "2":
        solve_mod2(vertices, colours, mat, cv)
    else:
        solve_Zhang(vertices, colours, mat, cv)
print('Total time taken\t',time.clock()-start_time)
