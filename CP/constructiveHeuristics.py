# This provide a set of constructive heuristics for the Happy Colourings Problem
import random, copy
import support as sp
from collections import deque

NIL = -1
# WHITE = 1
WHITE = 1
GREY = 2
BLACK = 3
    
#### Set of functions to add precolourings

# A modified version of BFS that starts at s (which is free)
#   and explores the graph induced by free d.vertices only.
# A list S is returned that gives all d.vertices reachable from S (including s itself)
def getFreeComponent(d, s, S):
    # Set up the arrays
    S = []
    col = []
    for i in range(d.vertices):
        col.append(WHITE)
    Q = deque([])
    
    # Start BFS
    col[s] = GREY
    Q.append(s);
    while len(Q) > 0:
        u = Q[0]
        for i in range(len(d.adjList[u])):
            v = d.adjList[u][i]
            if d.cv[v] == -1:
                # v is a free vertex
                if col[v] == WHITE:
                    # Have discovered a new unvisited vertex v from u
                    col[v] = GREY
                    Q.insert(-1, v)
        Q.pop()
        col[u] = BLACK
    # Get all the d.vertices in the component
    for i in range(d.vertices):
        if col[i] == BLACK:
            S.append(i)


# S is a component in the graph induced by free d.vertices.
# This procedure returns -1 if the d.vertices in S have no precoloured neighbours in G,
# NIL if S has more than one colour in adjacent preassignments, and the colour itself (uCol) otherwise.
def getColOfNeighbours(d, S):
    uCol = -1
    for i in range(len(S)):
        v = S[i]
        for j in range(len(d.adjList[v])):
            u = d.adjList[v][j]
            if d.cv[u] >= 0:
                if uCol < 0:
                    # u is a precoloured vertex that neighbours v
                    uCol = d.cv[u]
                elif uCol >= 0 and uCol != d.cv[u]:
                    #S neighbours precoloured d.vertices of more than one colour, so quit
                    return NIL;
    return uCol;

def moreThanOneAdjacentColour(d, v):
    uCol = -1
    for i in range(len(d.adjList[v])):
        u = d.adjList[v][i]
        if d.cv[u] >= 0:
            if uCol < 0:
                # u is a precoloured vertex that neighbours v
                uCol = d.cv[u]
            elif uCol >= 0 and uCol != d.cv[u]:
                # have identified that v neighbours more than one colour
                return 1
    # If we are here, v does not have more than one adjacent colour.
    return 0

def getStatus(d, v):
    # Takes an individual vertex in G and returns an integer indicating
    # whether is is a U-vertex (1), L_u vertex (2), or otherwise (3)
    if d.cv[v] >= 0:
        # v is precoloured. Check if it has at least one neighbour of a different colour (making it a U-vertex)
        for i in range(len(d.adjList[v])):
            u = d.adjList[v][i]
            if d.cv[u] >= 0 and d.cv[u] != d.cv[v]:
                return 1
        return 3;
    else:
        # v is not precoloured. Check to see if it has neighbours of two
        # or more different d.colours (making it an L_u-vertex)
        if moreThanOneAdjacentColour(d, v) == 1: return 2
        else: return 3

def noPotentiallyHappyNeighbours(d, v, status):
    #Returns true only if all of v's neighbours are U or L_u d.vertices (i.e. a guaranteed to be unhappy)
    for i in range(len(d.adjList[v])):
        u = d.adjList[v][i]
        if status[u] == 3:
            return 0
    return 1

# The main addPrecol function
def addPrecolourings(d, verbosity):
        S = []
        # Try to identify free d.vertices that can be precoloured.
        # Do this by looking at each free vertex, IDing free d.vertices
        #   that can be reached from it, and putting these into a set S.
        #Then look at the precoloured neighbours of S in G
        for v in range(d.vertices):
            if d.cv[v] == -1:
                getFreeComponent(d, v, S)
                col = getColOfNeighbours(d, S)
                if col == -1:
                    # Have identified a connected set of free d.vertices that are
                    # not adjacent to any precoloured d.vertices. They can all be
                    # precoloured to an arbitrary colour
                    col = random.randint(0,d.colours-1)
                    for i in range(len(S)):
                        u = S[i]
                        d.cv[u] = col
                    if verbosity >= 1:
                        print("The set of free d.vertices { ")
                        for i in range(len(S)):
                            print(str(S[i]) + " ", end = " ")
                        print("} has been precoloured to the same arbitrary colour (" + str(col) + ").")
                    elif col >= 0:
                        # Have identified a connected set of free d.vertices that are adjacent
                        # to precoloured d.vertices of just one colour. They can all be precoloured with this colour
                        for i in range(len(S)):
                            u = S[i]
                            d.cv[u] = col
                            if verbosity >= 1:
                                print("The set of free d.vertices { ")
                                for i in range(len(S)):
                                    print(str(S[i]) + " ", end = " ")
                                print("} has been precoloured to the same arbitrary colour (" + str(col) + ").")

        # Now identify (free) L_u d.vertices that can be precoloured. (I.e. ones who are free,
        # detined to be unhappy and whose neighbours are unhappy of desti\ ned to be unhappy.
        # These can be assigned to any arbitrarty colour. The staus labels are as follows: U-vertex (1), L_u vertex (2), or (3) otherwise
        status = []
        for v in range(d.vertices):
            status.append(getStatus(d, v))
        for v in range(d.vertices):            
            if status[v] == 2:
                if noPotentiallyHappyNeighbours(d, v, status) == 1:
                    #We can precolour v to an arbitrary colour
                    col = random.randint(0, d.colours - 1)
                    d.cv[v] = col
                    if verbosity >= 1:
                        print("Vertex-" + str(v) + " (and its neighbours) are guaranteed to be unhappy. It has been precoloured to an arbitrary colour (" + str(col) + ").")



################## The constuctive heuristics #################################


#---Functions for GreedyMHV-------------------------------------------------------------------
def evaluate(d, S):
    S.numHappy = d.vertices
    #Do a full evaluation of a solution S and update the relevant data structures
    for v in range(d.vertices):
        # Assume v is happy until determined otherwise
        S.isHappy[v] = 1
        for i in range(len(d.adjList[v])):
            u = d.adjList[v][i]
            if S.col[v] != S.col[u]:
                #v is adjacent to a different colour vertex so it is unhappy.
                S.isHappy[v] = 0
                S.numHappy -= 1
                break;

def emptyColourClass(d, S, c):
    # Removes all free vertices from colour class c
    numToDelete = len(S.items[c]) - d.numPreass[c]
    for i in range(numToDelete):
        v = S.items[c][-1]
        S.col[v] = -1
        S.items[c].pop(-1)

def fillColourClass(d, S, c):
    # Puts all free vertices into colour class c. Assumes S.items only contains precoloured at this point
    for v in range(d.vertices):
        if d.cv[v] == -1:
            S.items[c].append(v)
            S.col[v] = c

def GreedyMHV(d, S):
    maxHappy = -1
    bestJ = -1
    for j in range(d.colours):
        # Assign all free vertices to colour class j
        fillColourClass(d, S, j)
        evaluate(d, S)
        # Check if this is the best so far
        if S.numHappy > maxHappy:
            maxHappy = S.numHappy
            bestJ = j
        emptyColourClass(d, S, j)
    # Produce the solution by putting all free vertices into the best colour class
    fillColourClass(d, S, bestJ)
    evaluate(d, S)



###################### Functions for Growth MHV ###########################################

def determineColouredVertexStatus(d, v, S, status, numHappy):
    # Determines the status of a coloured vertex v by examining it neighbours u. Updates the numHappy variable where apt.
    if S.col[v] < 0:
        print("Error: have called the determineColouredVertexStatus function with an uncoloured vertex. Exiting...\n")
        
    # If a coloured vertex is already happy or destined to be unhappy, its status cannot change, so we end
    if status[v] == 0 or status[v] == 2: return status[v]
    # The status of this vertex is P and therfore has the potential to change, so calculate its new status
    oldstatus = status[v]
    freeNeighbour = 0
    for i in range(len(d.adjList[v])):
        u = d.adjList[v][i]
        if S.col[u] == -1:
            freeNeighbour = 1
        elif S.col[v] != S.col[u]:
            # v cannot be happy, so end immediately
            return 2;
    # If we are here, no neighbours of v are coloured differently
    if freeNeighbour == 0:
        # v has become happy
        numHappy[0] += 1
        S.isHappy[v] = 1
        return 0
    else:
        #v has uncoloured neighbours and has the potential to be happy
        return 1


def determineFreeVertexStatus(d, v, S, status):
    # Determines the status of an uncoloured (free) vertex v examining its neighbours u
    if S.col[v] >= 0: print("Error: have called the determineFreeVertexStatus function with a coloured vertex. Exiting...\n")
    anAdjColour = -1
    multipleAdjColoursToV = 0
    for i in range(len(d.adjList[v])):
        u = d.adjList[v][i]
        if status[u] == 1:
            # v is an L_p vertex (adjacent to a potentially happy, coloured vertex u). End immediately
            return 3
        if S.col[u] != -1 and anAdjColour == -1:
            # at least one colour adjacent to v
            anAdjColour = S.col[u]
        elif S.col[u] != -1 and S.col[u] != anAdjColour:
            # have observed at least two diff colours adjacent to v, so v cannot be happy
            multipleAdjColoursToV = 1
        #If we are here, v is not adjacent to a P-vertex -- it's status must be 4, 5, or 6.
    if anAdjColour != -1 and multipleAdjColoursToV == 0:
        # v is adjacent to vertices of only one colour, it has the potential to be happy
        return 4
    elif multipleAdjColoursToV == 1:
        #v is adjacent to vertices of more than one colour, it is destined to be unhappy
        return 5
    else:
        # all of v's neighbours are uncoloured.
        return 6


def getNextVertexToColour(d, status, PVertexExists, LHVertexExists, LUVertexExists):
    PVertexExists[0] = 0
    LHVertexExists[0] = 0
    LUVertexExists[0] = 0
    LUVertexPos = -1
    LFVertexPos = -1
    # Look for a coloured, potentially happy vertex v (a P-vertex)
    for i in range(d.vertices):
        if status[i] == 1:
            PVertexExists[0] = 1
            return i;
    # If we are here, we need to look for an uncoloured potentially happy, and then uncoloured unhappy, then uncoloured free vertex
    for i in range(d.vertices):
        if status[i] == 4:
            LHVertexExists[0] = 1
            return i
        elif status[i] == 5:
            LUVertexExists[0] = 1
            LUVertexPos = i
        elif status[i] == 6:
            LFVertexPos = i
    # If we are here, we have not found a P-vertex or a LH-vertex, but we have found a LU-vertex or, failing that, a LF-vertex
    if LUVertexExists[0] == 1:
        return LUVertexPos
    elif LFVertexPos < len(status):
        return LFVertexPos
    else:
        print("Error: Should not be here in the getNextVertexToColour function\n")
        return 0

def updateNeighboursStatus(d, v, S, status, numHappy):
    # A vertex v has just been coloured. Update the status of all neigbours
    for j in range(len(d.adjList[v])):
        u = d.adjList[v][j]
        if S.col[u] != -1:
            status[u] = determineColouredVertexStatus(d, u, S, status, numHappy);
        else:
            status[u] = determineFreeVertexStatus(d, u, S, status);

def updateDistanceTwo(d, v, status, S, numHappy):
    # Have had to modernise this function from algorithm description.
    # (Perhaps add this as an appendix to the paper's algorithm description).
    # Imagine we have a chain of vertices as follows [(1: P, red), (2: LP), (3: P, blue), (4: LP)]
    #  and we select vertex-1. This causes v-2 to become red too. Hence v-1 is happy, and v-2 is unhappy.
    # As a result v-3 now also changes it's state to unhappy, which should also change the status of v-4 to either LH or LU.
    # However, this will not happen with the Li-Zhang algorithm, because it tells us only
    # to update statuses of distance 2 from v. So if we have a vertex of distance-2 from
    # A vertex v and its neighbours have just been coloured with the same colour and v is happy.
    status[v] = 0
    numHappy[0] += 1
    S.isHappy[v] = 1
    # Update the statuses of all vertices adjacent to v
    for j in range(len(d.adjList[v])):
        u = d.adjList[v][j]
        status[u] = determineColouredVertexStatus(d, u, S, status, numHappy)
    # update status of each vertex u that has a distance of two from v
    for j in range(len(d.distTwoList[v])):
        u = d.distTwoList[v][j]
        if S.col[u] != -1:
            oldState = status[u]
            status[u] = determineColouredVertexStatus(d, u, S, status, numHappy)
            # This is the additional bit for dealing with the special cases noted in my paper
            if oldState != status[u]:
                for l in range(len(d.adjList[u])):
                    w = d.adjList[u][l]
                    if S.col[w] == -1:
                        status[w] = determineFreeVertexStatus(d, w, S, status)
        else:
            status[u] = determineFreeVertexStatus(d, u, S, status)

def getAdjacentColour(d, v, S):
    # Return a colour adjacent to vertex v
    for j in range(len(d.adjList[v])):
        u = d.adjList[v][j]
        if S.col[u] != -1:
            return S.col[u]
    # If we are here there is a problem
    print("Error: should not be here in function getAdjacentColour")
    return 0

def getUnhappyColouredNeighbour(d, v, status):
    # Return a vertex adjacent to v that is unhappy
    for j in range(len(d.adjList[v])):
        u = d.adjList[v][j]
        if status[u] == 2:
            return u
    #If we are here there is a problem
    print("Error: should not be here in function getUnhappyColouredNeighbour")
    return 0

def GrowthMHV(d, S):
    # Constructive algorithm for Happy Colouring Problem. Note that the precolourings have already been defined
    # Labels in the status array are as follows:
    # 0: (H-Vertex) Coloured and happy
    # 1: (P-vertex) Coloured and has potential to be happy
    # 2: (U-vertex) Coloured and destined to be unhappy
    # ---------
    # 3: (L_p-vertex) Not yet coloured, and adjacent to a P-vertex
    # 4: (L_h-vertex) Not yet coloured, not adjacent to a P-vertex, but has potential to be happy
    # 5: (L_u-vertex) Not yet coloured, not adjacent to a P-vertex, but destined to be unhappy
    # 6: (L_f-vertex) Not yet coloured, and not adjacent to any colured vertex
    numColoured = len(d.precolList)
    numHappy = [0]
    # Determine initial status of all coloured vertices, and then all uncoloured vertices
    status = []
    for i in range(d.vertices):
        status.append(-1)
    for i in range(d.vertices):
        if S.col[i] != -1:
            status[i] = determineColouredVertexStatus(d, i, S, status, numHappy)
    for i in range(d.vertices):
        if S.col[i] == -1:
            status[i] = determineFreeVertexStatus(d, i, S, status)

    # Main algorithm
    PVertex = [0]
    LHVertex = [0]
    LUVertex = [0]
    while numColoured < d.vertices:
        # Chooose next vertex v to colour
        v = getNextVertexToColour(d, status, PVertex, LHVertex, LUVertex)
        if PVertex[0] == 1:
            # v is a P-vertex with colour i. Colour all of its uncoloured neighbours u, with colour i
            i = S.col[v]
            for j in range(len(d.adjList[v])):
                u = d.adjList[v][j]
                if status[u] == 3 and S.col[u] == -1:
                    S.col[u] = i
                    S.items[i].append(u)
                    numColoured += 1
                    #update status of all vertices within distance 2 of v
            updateDistanceTwo(d, v, status, S, numHappy)
        elif LHVertex[0] == 1:
            #v is a LH-vertex adjacent to a colour i. Colour v and all its its uncoloured neighbours u with i.
            i = getAdjacentColour(d, v, S)
            S.col[v] = i
            S.items[i].append(v)
            numColoured += 1
            for j in range(len(d.adjList[v])):
                u = d.adjList[v][j]
                if S.col[u] == -1:
                    S.col[u] = i
                    S.items[i].append(u)
                    numColoured += 1
            # update status of all vertices within distance 2 of v
            updateDistanceTwo(d, v, status, S, numHappy)
        elif LUVertex[0] == 1:
            # v is an LU-vertex. When we colour it, it will be unhappy. Also, it must have an unhappy neighbour currently
            u = getUnhappyColouredNeighbour(d, v, status)
            i = S.col[u]
            S.col[v] = i
            S.items[i].append(v)
            numColoured += 1
            status[v] = 2
            # update the status of v's neighbours
            updateNeighboursStatus(d, v, S, status, numHappy)
        else:
            # v must be an LF-vertex (i.e. v is in a component in which none of the vertices are coloured). First choose a random colour for v
            i = random.randint(0, d.colours-1)
            S.col[v] = i
            S.items[i].append(v)
            numColoured += 1;
            if len(d.adjList[v]) == 0:
                # v is an isolated vertex so it is happy
                status[v] = 0
                S.isHappy[v] = 1
                numHappy[0] += 1
            else:
                # v has neighbours so we set it as potentially happy and update its neighbours
                status[v] = 1
                updateNeighboursStatus(d, v, S, status, numHappy)
    S.numHappy = numHappy[0]


# Make an initial solution, using GreedyMHV
def makeInitSol(d):
    # Clear the solution and set up the data structures
    items = []
    cols = []
    isHappy = []
    nHappy = 0
    
    for i in range(d.vertices):
        cols.append(-1)
        isHappy.append(0)
        
    for j in range(d.colours):
        items.append([])
        d.numPreass.append(0)
        
    S = sp.Sol(cols, isHappy, nHappy, items)

    # Assign all of the precolurings defined in G
    for i in range(d.vertices):
        if d.cv[i] == -1: continue
        colour = d.cv[i]
        S.items[colour].append(i)
        S.col[i] = d.cv[i]

    for i in range(d.vertices):
        if d.cv[i] != -1:
            d.numPreass[d.cv[i]] += 1

    # Make a copy of S called SPrime
    SPrime = copy.deepcopy(S)
            
    # Produce solutions using GreedyMHV and GrowthMHV and return the best of these
    GreedyMHV(d, S);
    print("GreedyMHV produced: " + str(S.numHappy))
    GrowthMHV(d, SPrime);
    print("GrowthMHV produced: " + str(SPrime.numHappy))
    if SPrime.numHappy > S.numHappy:
        S = SPrime
    return S


