#!/usr/bin/python

from copy import deepcopy 
import random, time

# Run an ACO to solve the graph colouring problem

# A solution class
class solution:
    def __init__(self, v, cv, m):
        self.init(v, cv, m)
    def valid(self): return hasattr(self,"ACO solution information")
    def init(self, v, cv, m):
        self.happy = []
        self.totalHappy = 0
        self.seq = []
        for i in range(v):
            self.seq.append(-1)
            self.happy.append(-1)
            self.seq[i] = cv[i]
        # Do some additional preprocessing to ensure verteces are fixed to colours if all its neighbours are the same colour
        done = 0
        while done == 0:
            change = 0
            for i in range(v):
                if self.seq[i] > -1 : continue
                cols = set([])
                for j in range(v):
                    if m[i][j] < 1 or self.seq[j] == -1: continue
                    cols.add(self.seq[j])
                if len(cols) == 1:
                    self.seq[i] = cols.pop()
                    change = 1
                    #print("Set vertex: " + str(self.seq[i]))
            if change == 0: done = 1

    # Compute the objective
    def computeHappy(self, v, m):
        for i in range(v):
            # Check if the vertex is already done
            if self.happy[i] == 0 or self.happy[i] == 1: continue 
            for j in range(v):
                if m[i][j] < 1 or i==j: continue # No link
                if self.seq[i] != self.seq[j]:
                    self.happy[i] = 0
                    self.happy[j] = 0
                    break
            # If the node is not unhappy, it must be happy
            if self.happy[i] == -1: 
                self.happy[i] = 1
            if self.happy[i] == 1:
                self.totalHappy += 1

        
    # Display the solution
    def display(self, vertices, mat):
        # Display some solution information
        usum = 0
        hsum = 0
        for i in range(vertices):
            print ("V " + str(i+1) + ": " + str(self.seq[i]) + ", connections: ", end="")
            count = 0
            for j in range(vertices):
                if mat[i][j] == 1:
                    if count == 0:
                        print ("(" + str(j+1) + "," + str(self.seq[j]) + ") ",end="") 
                    else:
                        print (",(" + str(j+1) + "," + str(self.seq[j]) + ") ",end="") 
                    count += 1
            if self.happy[i] == 0:
                print ("\nV " + str(i+1) + " is unhappy") 
                if count == 0:
                    print("This results is surprising")
                usum+=1
            else:
                print ("\nV " + str(i+1) + " is happy") 
                hsum+=1
        print("Happy vertices: " + str(hsum) + " unhappy vertices: " + str(usum))
                    
# A pheromones class, needed relly for choice information
class pher:
    def __init__(self, v, c, cv, mat, lrate):
        self.init(v, c, cv, mat, lrate)
    def valid(self): return hasattr(self,"Pheromone object")
    # Initialise pheromones
    def init(self, v, c, cv, mat, lrate):
        self.p = []
        self.ci = []
        self.lrate = lrate
        for i in range(v):
            self.p.append([])
            self.ci.append([])
            for j in range(c):
                self.p[i].append(0.0)    
                self.ci[i].append(0.0)    
            # Change probabilities depending on neighbour colours
            for j in range(v):
                if mat[i][j] < 1 or cv[j] == -1: continue
                col = cv[j]
                self.p[i][col] += 3.0 # Double the weight for a colour that is already known
            
            # Now mormalise the pis across colours
            sump = 0
            for j in range(c):
                if self.p[i][j] == 0:
                    self.p[i][j] = 1.0 # Need some probability to start with
                sump += self.p[i][j]
            for j in range(c):
                self.p[i][j] = self.p[i][j] / max(1.0,sump)
                factor = 1.0
                for k in range(len(cv)):
                    if cv[k] == -1 or mat[i][k] < 1: continue
                    if cv[k] == col:
                        factor += 1.0
                self.ci[i][j] = self.p[i][j]*factor
    # A local pheromone update
    def localUpdate(self, j, col, seq, mat):
        # Modify factor to include heuristic information
        factor = 1.0
        for i in range(len(seq)):
            if seq[i] == -1 or mat[j][i] < 1: continue
            if seq[i] == col:
                factor += 1.0
        factor = factor / 10.0
        self.p[j][col] = (1.0-self.lrate)*self.p[j][col]    
        self.ci[j][col] = self.p[j][col]*factor
    # A global pheromone update
    def globalUpdate(self, v, c, best):
        # If the colour is in the neighbourhood, give it a higher reward
        reward = float(best.totalHappy)+1.0
        while reward > 0.1: 
              reward = reward / 10.0
        for j in range(v):
            col = best.seq[j]
            self.p[j][col] = (1.0-self.lrate)*self.p[j][col] + reward
            self.ci[j][col] = self.p[j][col]
    
    #Reset the pheromones if they have converged
    def reset(self, v, c, mat, cv):
        for i in range(v):
            for j in range(c):
                self.p[i][j] = 1.0
            # Change probabilities depending on neighbour colours
            for j in range(v):
                if mat[i][j] < 1 or cv[j] == -1: continue
                col = cv[j]
                self.p[i][col] = 3.0 # Double the weight for a colour that is already known
            
            # Now mormalise the pis across colours
            sump = 0
            for j in range(c):
                sump += self.p[i][j]
            for j in range(c):
                self.p[i][j] = self.p[i][j] / max(1.0,sump)
                self.ci[i][j] = self.p[i][j]

    # Display some pheromone information, just for debugging
    def display(self, v, c):
        for j in range(v):
            print("")
            for i in range(c):
                print(self.p[j][i]),


# A probabilistic selection
# ri is the removed index, same length as dist
def roulette_wheel(dist):
   sumProbs = 0.0
   selectionProb = []
   for l in range(0,len(dist)):
      selectionProb.append(0.0)
   for l in range(0,len(dist)):
      selectionProb[l] = dist[l]
      sumProbs += selectionProb[l]
   r_num = random.random()
   r = sumProbs*r_num
   j = 0
   prob=selectionProb[j]
   while prob < r:
      j += 1
      prob += selectionProb[j]
   return j

# A greedy selection
def greedy(dist):
    j = -1
    prob = 0.0
    for l in range(0,len(dist)):
        if dist[l] > prob:
            j = l
            prob = dist[l]
    return j

# Select a colour for a vertex using the pheromones
def selectColour(j, c, p, q0):
    r = random.random()
    #print(p.ci[j])
    if r < q0:
        col = roulette_wheel(p.ci[j])
    else:
        col = greedy(p.ci[j])
    return col

# Construct colourings
def constructSolutions(v, c, n, p, m, cv, lrate, q0):
    best = solution(v, cv, m)
    for i in range(n):
        sol = solution(v, cv, m)
        for j in range(v):
            # Ifwe already have a colour, don't do anything
            if sol.seq[j] != -1: continue
            col = selectColour(j, c, p, q0)
            sol.seq[j] = col
            # Need to include a local pheromone update here
            p.localUpdate(j, col, sol.seq, m)
            #h = 1
            #for k in range(v):
            #    if k == j or m[j][k] < 1: continue
            #    if sol.seq[k] != sol.seq[j]:
            #        h = 0
            #        break
            #if h == 1: # set all its connected vertices to the same colour
            #    for k in range(j+1,v):
            #        if k == v or m[j][k] < 1: continue
            #        sol.seq[k] = col
        sol.computeHappy(v, m)
        #localSearch(v, c, m, cv, sol)

        if i == 0:
            best = deepcopy(sol)
        else:
            if sol.totalHappy > best.totalHappy:
                best = deepcopy(sol)
    return best


# Local search
# Swap a colour for a vertex tothe most common colour of its neighbours
# Accept if an improvment over one pass
def most_common(lst):
    return max(set(lst), key=lst.count)

def localSearch(v, c, mat, cv, sol):
    ib = deepcopy(sol)
    for i in range(v):
        if cv[i] == -1: continue # A colour that can't change
        col = []
        for j in range(v):
            if mat[i][j] < 1: continue
            if ib.happy[j] == 0: continue
            col.append(ib.seq[j])
        if col == []: continue
        ib.seq[i] = most_common(col)
        ib.computeHappy(v, mat)
        if ib.totalHappy > sol.totalHappy:
            sol = deepcopy(ib)
            print("\n\tSolution found with ls: " + " happy: " + str(sol.totalHappy) + " unhappy: " + str(v-sol.totalHappy))

# Main function - execute ACO
def ExeACO(vertices, colours, mat, cv, stime, limit):
    nants = 30
    iter_limit = 5000
    lrate = 0.01
    q0 = 0.1
    # A solution
    best = solution(vertices, cv, mat)
    # A pheromone matrix
    pheromones = pher(vertices, colours, cv, mat, lrate)
    iter = 0
    terminate = 0
    print("Starting ACO ... ")
    ibSolutions = []
    while terminate == 0:
        ib = constructSolutions(vertices, colours, nants, pheromones, mat, cv, lrate, q0)
        ibSolutions.append(deepcopy(ib))
        #if len(ibSolutions) > 10:
        #    ibSolutions.pop(0)
        if iter == 0:
            best = deepcopy(ib)
            print("Solution found at iteration " + str(iter + 1) +" happy: " + str(best.totalHappy) + " unhappy: " + str(vertices-best.totalHappy))
        else:
            if ib.totalHappy > best.totalHappy:
                print("Solution found at iteration " + str(iter + 1) +" happy: " + str(ib.totalHappy) + " unhappy: " + str(vertices-ib.totalHappy))
                best = deepcopy(ib)
        iter += 1
        # Do a global pheromone update
        pheromones.globalUpdate(vertices, colours, best)
        if (time.clock()-stime > limit) or (iter > iter_limit) :
            terminate = 1
        # Check to make sure the last n solutions are not the same
        #if len(ibSolutions) == 10:
        #    same = 1
        #    for k in range(len(ibSolutions)-1):
        #        for l in range(k+1,len(ibSolutions)):
        #            if k == l : continue
        #            if ibSolutions[k].happy != ibSolutions[l].happy:
        #                same = 0
        #                break
        #    if same == 1:
        #        print("Pheromones converged, resetting ... ")
        #        pheromones.reset(vertices, colours, mat, cv)
        #        ibSolutions = []
        #pheromones.display(vertices, colours)
    best.display(vertices,mat)
    print("Termination criteria reached ...")
