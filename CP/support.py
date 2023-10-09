import random

# This class keeps track of a solution
class Sol:
    def __init__(self, col, isHappy, numHappy, items):
        self.col = col
        self.isHappy = isHappy
        self.numHappy = numHappy
        self.items = items

# This class keep track of the data
class Data:
    def __init__(self, vertices, colours, cv, mat, adjList):
        self.UB = 0
        self.vertices = vertices
        self.colours = colours
        self.cv = cv
        self.mat = mat
        self.adjList = adjList
        self.numPreass = []
        self.distTwoList = []
        self.freeList = []
        self.compDistTwoList()
        self.precolList = []
        self.computeProcolList()

    def computeProcolList(self):
        for i in range(self.vertices):
            if self.cv[i] == -1:
                self.freeList.append(i)
            else:
                self.precolList.append(i)
            
    def compDistTwoList(self):
        distTwo = []
        for i in range(self.vertices):
            distTwo.append([])
            self.distTwoList.append([])
            for j in range(self.vertices):
                distTwo[i].append(0)

        for i in range(self.vertices):
            if len(self.adjList[i]) > 0:
                for j in range(len(self.adjList[i]) - 1):
                    for l in range(j+1, len(self.adjList[i])):
                        v = self.adjList[i][j]
                        u = self.adjList[i][l]
                        if self.mat[u][v] == 0:
                            # u and v are neighbours with i, but not with each other. So they have distance of two
                            distTwo[u][v] = 1
                            distTwo[v][u] = 1
        # and populate the distTwoList
        for i in range(self.vertices):
            for j in range(self.vertices):
                if distTwo[i][j] == 1: self.distTwoList[i].append(j)

class INFO:
    def __init__(self):
        self.timeOfBest = 0.0        #Tells us the number of seconds after the start of the algorithm the best solution was found
        self.itOfBest = 0            #Tells us the number of iterations that it took to find the best solution in the run
        self.numIts = 0              #Tells us the total number of iterations tabuSearch was run for
        self.numSecs = 0.0           #Tells us the total time tabuSearch was run for
                
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

    # Compute an adjacency list
    adjList = []
    for i in range(vertices):
        lst = []
        for j in range(vertices):
            if mat[i][j] == 1:
                lst.append(j)
        adjList.append(lst)

    d = Data(vertices,colours,cv,mat,adjList)
    return d


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

    # Compute an adjacency list
    adjList = []
    for i in range(vertices):
        lst = []
        for j in range(vertices):
            if mat[i][j] == 1:
                lst.append(j)
        adjList.append(lst)

    d = Data(vertices,colours,cv,mat,adjList)
    return d


# Initialise data needed by the model
def initialiseData(d, isols):
    fixed = []
    for i in range(d.vertices):
        fixed.append(-1)
    sols = []
    for i in range(isols):
        b = generateRandomSolution(d)
        sols.append(b)
    #b_sol = sp.generateRandomSolution(d)

    # The age parameter for each variable
    age = {}
    for i in range(d.vertices):
        for k in range(d.colours):
            age[i,k] = 0
    
    return (fixed, sols, age)

# Generate a random solution
def generateRandomSolution(d):
    cols = []
    happyV = []
    for i in range(d.vertices):
        happyV.append(1)
        if d.cv[i] != -1:
            cols.append(d.cv[i])
        else: # Select a random colour
            rnd = random.randint(0,d.colours-1)
            cols.append(rnd)

    nHappy = 0
    for i in range(d.vertices):
        happy = 1
        for j in range(d.vertices):
            if (d.mat[i][j] != 1) or (i == j): continue
            if cols[i] != cols[j]:
                happy = 0
                break
        if happy == 1:
            happyV[i] = 1
            nHappy += 1

    items = []
    bsol = Sol(cols, happyV, nHappy, items)
    return bsol

# Use the best known solution to generate a probability distribution
def findProbsBest(d, b_sol):
    probs = {}
    for i in range(d.vertices):
        for k in range(d.colours):
                probs[i,k] = 0.0
        if d.cv[i] != -1: continue
        prob_tot = len(d.adjList[i])
        # Find the number of neighbours assigned colours 
        for j in range(len(d.adjList[i])):
            colour = b_sol.col[d.adjList[i][j]]
            probs[i,colour] += 1.0;
        # Normalise the probabilities
        for j in range(len(d.adjList[i])):
            colour = b_sol.col[d.adjList[i][j]]
            probs[i,colour] /= prob_tot;
    return probs

# Generate the probabilities uniformly randomly
def findProbsRandom(d):
    probs = {}
    for i in range(d.vertices):
        for k in range(d.colours):
            probs[i,k] = 1.0/d.colours
    return probs

# Some old code to generate probabilities
    # check every node's neighbour and
    # compute a probability distribution for vertex/colour pairs
    #for i in range(vertices):
    #    for k in range(colours):
    #            probs[i,k] = 1/colours
    #    if cv[i] != -1: continue
        # Find the number of neighbours assigned colours 
    #    prob_tot = colours
    #    for j in range(vertices):
    #        if mat[i][j] != 1: continue
    #        probs[i,b_sol.col[j]] += 1.0;
    #        prob_tot += 1;
        # Normalise the probabilities
    #    for k in range(colours):
    #        probs[i, k] /= prob_tot;

def changeCols(d, sols, b_sol, isols, age, itr):
    # A data structure to keep track of the neighbourhood of the vertex
    # This will determine the probability of flipping a node's colour

    #if itr > 5:
    #probs = findProbsBest(d, b_sol)
    #else:
    probs = findProbsRandom(d)
            
    # Change colours among the solutions using a probabilistic scheme
    for s in range(isols - 1):
        #print("Solution " + str(s))
        for i in range(d.vertices):
            if d.cv[i] == -1:
                # Change the colour with some probability
                #if len(d.adjList[i]) <= 1:
                #    sols[s].col[i] = b_sol.col[i];
                #else: # do a probabilistic selection (uniformly not including the colour)
                sumProbs=0.0
                prob=0.0
                rnd = 0.0
                selectionProb = []
                for j in range(d.colours):
                    selectionProb.append(0.0)
                for j in range(d.colours):
                    #if j == b_sol.col[i]: continue
                    selectionProb[j] = probs[i,j]
                    sumProbs+=selectionProb[j]
                r_num= random.uniform(0,1)
                #print(sumProbs)
                rnd=sumProbs*r_num#random.randrange(floor(sumProbs)+1)
                #print(rnd)
                j=0
                prob=selectionProb[j]
                while prob<rnd:
                    j+=1
                    prob+=selectionProb[j]
                sols[s].col[i] = j
                    #if i < 100:
                        #print ("Chose " + str(j) + " for " + str(i))
            else:
                sols[s].col[i] = b_sol.col[i]
    return (probs)
