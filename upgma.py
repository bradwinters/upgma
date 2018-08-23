import itertools
import copy
import random 
  
################################################################
#  Accepts a Tree Dictionary of key (node) with value(list) of
#  parent nodes to its children.  Age is also a Dict with each
#  nodes age so Edges are the difference in Ages between nodes. 
#  
#  Compute the Edges of the Tree formed by finding the internal 
#  nodes up to the root.  Tree is node to children nodes, two
#  for this binary tree (speciation assumes single splits). With
#  the node to children map, edges are computed with the Age
#  Dictionary which has each nodes Age stored as a value.
#  To compute the whole tree, loop through the Tree dict, storing
#  node to children branching, followed by age that is subracted
#  by subtracking the child nodes age from the parents, both 
#  age values are in the Age dictionary.  
#  This routine also puts the Node->child:Age into the required
#  output and importantly, sorts them as expected in the requirements
################################################################
def orderedTree(pNodeTree,pWtList):

    niceTree=[]
    amax=max(pNodeTree)+1
    amin=min(pNodeTree)
    for x in range(amin,amax):
       for edge in pNodeTree[x]:
          edge=int(edge)
          Age=float(pWtList[x])-float(pWtList[edge])
          ss = "%02d->%s:%.3f" % (x, edge, Age)
          niceTree.append(ss)
          ss = "%02d->%s:%.3f" % (edge, x, Age)
          niceTree.append(ss)
          #print("Age of ",x," is ",float(pWtList[x]))
          #print("Age of ",edge," is ",float(pWtList[edge]))
          #print(str(x)+"=>"+str(edge)+":"+str(Age))

    return  niceTree

def ShowAll(D,Clusters,ClusterCnt,T,Age):
    print("++++++++++++++++++++++++++++++++")
    print("D") 
    print(D) 
    print("Clusters") 
    print(Clusters) 
    print("ClusterCnt") 
    print(ClusterCnt) 
    print("T") 
    print(T) 
    print("Age") 
    print(Age) 
    print("++++++++++++++++++++++++++++++++")

    return "Done"

################################################################
# Compress row/col gaps from combining the matrix.  This is done
# automatically in the matrix but not for the row/column labels
# They must be updated as well when holes are produced while 
# combining.  Loop thru the dict, noting the gap row and add 
# the missing gap in the lower numbered row.  
# Delete the last row as it has been moved to one less and not
# overwritten 
################################################################
def checkit(pClusters):
    sz=len(pClusters)
    missing=[]

    for x in range(sz):
       if x in pClusters:
           pass
       else:
           missing.append(x)

    if len(missing) > 1:
        print("Somethings wrong, Too many gaps in the dictionary")
        print(missing)
        exit()
    if len(missing)==1:
        marker=missing[0] 
        for x in range(marker,sz):
            pClusters[x]=pClusters[x+1]
            jj=x+1 
        del pClusters[jj]

    return pClusters

#####################################
#   -Add the averaged row, col i,j to D 
#   -Copy old to new but col j is filled with newNode i 
#     and when row i is processed, just add newNode vector 
#   -Track thru the 2x loop with different ptrs since they are
#     not the same size
#####################################
def integrateRow(ppD,aNewRow,pi,pj):
    Dl, Dw=len(ppD)+1, len(ppD[0])+1  # not to be tricky, just shows they are related
    oldi=oldj=0  # ptrs to the input array, which is smaller so separate loop

    Matrix = [[0 for x in range(Dw)] for y in range(Dl)] 
    #print("in integrate, i and j are ",pi," ",pj)
    for i in range(Dl):
       oldj=0
       if i==pi:
          for j in range(Dw):
             Matrix[i][j]=aNewRow[j]
       else:
          for j in range(Dw):
             if j==pi:
                Matrix[i][j]=aNewRow[i]
             else:
                Matrix[i][j]=ppD[oldi][oldj]
                oldj+=1
          oldi+=1
          

    return Matrix

#####################################
#   Remove the row, col i,j from D 
#   Copy rows 0 to i, then i+1 to n
#   Copy col 0 to j, then j+1 to m
#####################################
def removeRC(ppD,pi,pj):
    Dl=len(ppD)
    Dw=len(ppD[0]) 
    Matrix=[]

    # copy all cols except i
    for i in range(Dl):
       tRow=[]
       if i != pi and i != pj:
          for j in range(Dw):
             if j != pj and j!= pi: 
                tRow.append(ppD[i][j])
          Matrix.append(tRow)
    
    return Matrix


##############################################################################
#  Combine 2 rows, averaging them to create one 
##############################################################################
def CalcCombine(ppD,pi,pj,iWt,jWt):
    #print("Combine these two rows")
    newRow=[]
  
    for x in range(len(ppD[pi])):
       if x == pi:
          nrv=0.0
          newRow.append(nrv)      
       elif x==pj:
          pass
       else:
          nrv=(float(ppD[pi][x])*iWt+float(ppD[pj][x])*jWt)/(iWt+jWt)
          newRow.append(nrv)      
    
    return newRow 

##############################################################################
#   Find the row, col i,j with the smallest value, return them and the value
##############################################################################
def smallestNode(pD):
    age=999999
    si=0
    sj=0
    Dl=len(pD[0])
    Dw=len(pD)
    for i in range(Dl):
       for j in range(Dw):
          if pD[i][j] < age and j != i:
             age = pD[i][j] 
             si=i
             sj=j

    return si, sj, age 

######################################################################
#  -Purpose: Add or create an entry into a dictionary that represents a node in a Tree
#   The node is a key, its value is a list of children nodes
#   -The distance from the parent node to individual children is in another matrix
#  -Accept the dictionary as a parameter, as well as the parent node pKey and its child, pValue) 
#  First check to see if that node exists.  If it does, the existing children node list
#    is copied out into a temporary list, tList, the new child appended to tList, and the node deleted
#  The revised node is then entered back into the dictionary again with the appended list  
######################################################################
def addNode(aDict,pKey,pValue):  # update a dict of lists

    tList=[]
    if pKey in aDict:  # exists, extract, update list.  Replace list
       for i in aDict[pKey]:
           tList.append(i)
       tList.append(pValue)
       del aDict[pKey]
       aDict[pKey]=set(tList)
    else:
       tList.append(pValue)  # create list, put val in it
       aDict[pKey]=set(tList)

    return aDict

######################################################################
#  -Purpose: Add or create an entry into a dictionary that represents a each nodes age
#   The node is a key, its value is its age 
#  -Accept the dictionary as a parameter, as well as the node as a key and its age
#  -First check to see if that node exists.  If it does, show a warning condition and move on 
######################################################################
def nodeAge(aDict,pKey,pValue):  # update a dict of lists

    if pKey in aDict:  # exists, extract, update list.  Replace list
       aDict[pKey]=pValue
       print("Possible double entry of an edge in the wts dictionary")
    else:
       aDict[pKey]=pValue

    return aDict


def upgma(pD,pn):
    ## pn is the number of leaf nodes originally, newNode will be used to create internal branches
    ## newNode is a node labelling variable using consecutivly available numbers starting from the leaves
    Cntr=0
    Cnew=pn-1
    Age={} # age of the node
    for x in range(pn):
       Age[x]=0
    T={}  # a given nodes children in a list
    Clusters={}
    ClusterCnt={}
    for x in range(pn):
       nd=x
       Clusters[x]=nd 
       ClusterCnt[x]=1
    while len(pD) > 2:
       Cntr+=1
       # step one, find the smallest pairs and get thier cluster names
       # the pairs are simply the row/column of the matrix D, but they have been combined
       # into the internal nodes while the Tree forms
       # this requires looking up the clusters in the LookupRC table
       #######
       #  1  Find 2 smallest entries, return their position in the matrix and the value #
       #######
       i,j, sAge = smallestNode(pD)

       #find the numbers of the rows/cols before, make a list
       #attach that list to the newly formed interal nodes
       #the new node is just the next available number

       #######
       #  2  Merge Ci and Cj into Cnew and note the counts of the merged  Cnew #
       #######
       # Get cluster name from its row in current D
       Ci=Clusters[i]
       # Get cluster name from its col in current D
       Cj=Clusters[j]
       # put old Cs, children, to be combined, in an array,  Keep open for multi children in future
       CiCj=[]
       CiCj.append(Ci)
       CiCj.append(Cj)
       CiWt=ClusterCnt[i]
       CjWt=ClusterCnt[j]
       CiCjCount=CiWt+CjWt
       #######
       #  3 and 4  Add Cnew to T and connect the tow new Child nodes, Ci and Cj  #
       #######
       Cnew+=1 
       #Clusters[i]=Cnew
       #ClusterCnt[i]=CiCjCount
       T[Cnew]=CiCj

       #######
       #  5  #
       #######
       Age[Cnew]=float(sAge/2.0)

       #Compute new row, must be done before the row is removed 
       newRow=CalcCombine(pD,i,j,CiWt,CjWt)
       #######
       #  6  #
       #######
       pD=removeRC(pD,i,j)
       # delete its previous values as they will be merged
       del ClusterCnt[i]
       del ClusterCnt[j]
       del Clusters[i]
       del Clusters[j]
       Clusters[i]=Cnew
       ClusterCnt[i]=CiCjCount
       #######
       #  8  #
       #######
       #New row is ready, so get rid of the old row
       #place the new row in there, to the lower of the two, and get rid of the other row
       pD=integrateRow(pD,newRow,i,j)

       # Compact the lookup node row/column dictionary, Clusters, close gaps from merging
       # next in line, just a sequence
       #ShowAll(pD,Clusters,ClusterCnt,T,Age)
       Clusters=checkit(Clusters)
       ClusterCnt=checkit(ClusterCnt) 
       #ShowAll(pD,Clusters,ClusterCnt,T,Age)
    #process the root
    i,j, sAge = smallestNode(pD)

    pre=Clusters[i]
    post=Clusters[j]
    oldN=[]
    oldN.append(pre)
    oldN.append(post)
    Cnew+=1 
    #fish
    T[Cnew]=oldN

    del Clusters[i]
    del Clusters[j]
    Clusters[i]=Cnew
    Age[Cnew]=float(sAge/2.0)
    return T, Age 



def copy_2D(pM):
    return copy.deepcopy(pM)

def MatrixtoGraph(rMatrix):

    lG=len(rMatrix)
    wG=len(rMatrix[0])

    pMatrix=copy_2D(rMatrix) 

    for i in range(lG):
       for j in range(wG):
          if i != j and pMatrix[i][j]!= -99:
             ci=str(i)
             cj=str(j)
             #print(ci+"->"+cj+":"+str(int(pMatrix[i][j])))
             #pMatrix[j][i]=-99

    return "Done" 

def bfs_paths(pGraph,pStart,pGoal):
    queue = [(pStart, [pStart])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in pGraph[vertex] - set(path):
            if next == pGoal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

###########################################################
# Given a list, return a list of all combinations of pairs
# 
#########################################################
def permuter(aList):
    newList=[]
    n = len(aList)
    m = n
    a = [[0] * m for i in range(n)]
    for i in itertools.product(aList,aList):
        if i[0] != i[1]:
           start=i[0]
           goal=i[1]
           #print("Start:",start,"  Goal:",goal)
           newList.append((start,goal))
    return newList

#########################################################
# Given a list, return a tagList which simply tupleizes
# the list items by their position in the list
#########################################################
def tagR(alist):
    tagList=[]
    for x in range(len(alist)):
        tagList.append((x,alist[x]))   

    return tagList


#########################################################
#
#########################################################
def smallestLimb(pMatrix,pRow):
    minum=99999
    theRow=pMatrix[pRow] 
    #print(theRow)
    labRow=tagR(theRow)
    #print("Tagged list is ")
    #print(labRow) 
    ans=permuter(labRow)
    for x in range(len(ans)):
        i_index=ans[x][0][0]
        k_index=ans[x][1][0]
        if i_index==pRow or k_index==pRow:
           continue
        #print(pRow," to ",ans[x][0][0],"  costs ",ans[x][0][1])
        #print(pRow," to ",ans[x][1][0],"  costs ",ans[x][1][1])
        i=ans[x][0][1]
        k=ans[x][1][1]
        #print("i is ",i)
        #print("k is ",k)
        ik=i+k
        #print("They add to ",ik)
        lu=pMatrix[i_index][k_index]
        #print("Minus ",lu)
        answ=(ik-lu)/2
        if answ < minum: 
           minum=answ
        
    return minum 




def readData():
    '''
    Open hardcoded file, parse data anticipataed but may change
    Load just data into a numpy array, 
    '''
  
    f = open('wk1.dat', 'r')   #Smaller dataset 
    #f = open('p1.dat', 'r')   #Smaller dataset 
    #f = open('p2.dat', 'r')   #Smaller dataset 
    #f = open('p5.dat', 'r')   #Smaller dataset 
    #f = open('p4.dat', 'r')   #Smaller dataset 
    #f = open('l.dat', 'r')   #Smaller dataset 
    #f = open('ed.dat', 'r')   #Smaller dataset 
    #f = open('extras6.dat', 'r')   #Smaller dataset 
    #f = open('test3', 'r')   #Smaller dataset 
    cnt=0
    Matrix=[] # 2D list 
    nodeDict={} # dict of sets
    wtDict={} # dict 
    for line in f:
        xx=line.rstrip() # get rid of cr
        if cnt==0:       # known line to contain only K and M
           n=int(xx)   # n leaves
        elif cnt >= 1:
           ##Parse data, put rows in list, list appended to a numpy array
           # Rows will be as 0->4:11 where node 0 points to a node 4 with wt 11 
           #aRow=xx.split("\t")
           aRow=xx.split(" ")
           tempRow=[]
           for leaf in range(len(aRow)):
              tempRow.append(int(aRow[leaf]))
           Matrix.append(tempRow)
        else:
           print("Something is wrong, bail")

        cnt+=1

    return n, Matrix

##################################################
#  find first occurance of a value in a 2 D grid 
##################################################
def FindX(nGrid,value):

    sizeD=len(nGrid)
    for i in range(sizeD):
        for j in range(sizeD):
             if nGrid[i][j]==value:
                return str(i), str(j)
    return -99, -99 

############################################################
##  Load a 2D array with a sum of their row/col 
############################################################
def ezGrid(nGrid):

    sizeD=len(nGrid)
    for i in range(sizeD):
        for j in range(sizeD):
             if j!=i:
                 nGrid[i][j]=i+j
             else:
                 nGrid[i][j]=0

    return nGrid

def main():
   
    # read file, load edge dictionarys of nodes:set and one of edges 
    # ---- nodes ------
    # nodes  Node: { Child1, Child2, etc}
    #  '5' : { '1','4','3'}    (String: List of Strings)
    #
    # ---- wts ------
    # edge wt  Edge: Wt  where Edge is a tuple 
    # ('4','3') : 11    (S1,S2), Integer)
    #  
    #  1.  Make a list of leafs 
    #  2.  Round robin leafs against each other, both directions, but exclude diagonal edge
    #  3.  Pass the graph, start and end into dfs, producing a path 
    #  4.  Go through each path element, trace the path summing edge wts 
    #  5.  As step 4 is being summed, place the result into the i,j position of the matrix 
    #  6.  Output the matrix as specified.


    n, D = readData() #load Data and Params from file




    Tree, age=upgma(D,n)
    finalAns=orderedTree(Tree,age)
    finalAns.sort()
    for row in finalAns:
       if row[0]=='0':
          print(row[1:])
       else:
          print(row)

if __name__ == "__main__":
    main()
