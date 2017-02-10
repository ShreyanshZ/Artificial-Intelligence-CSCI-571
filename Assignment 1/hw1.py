def mainprog(ipfile):
	'''
	**** Taking a single line from file and storing it in 'line' lisy ****
	'''
	lines = [line.rstrip('\n') for line in open(ipfile)]
	'''
	**** Taking the values of Algo Type, StartState, EndState and No. of Edges ****
	'''
	close=[]
	goal=False
	opened = []
	finalop=[]
	algo=lines[0]
	startstate=lines[1]
	endstate=lines[2]
	notl=int(lines[3])
	'''
	**** Initializing ref - temporary list to store each item in a line ****
	**** Initializing dictionary - Storing nodes as they come in the edges ****
	'''
	ref=[]
	dictionary=[]
	'''
	**** Adding Nodes as they arrive in dictionary ****
	'''
	for i in range(4,4+notl):
		ref=lines[i].split(' ')
		if ref[0] not in dictionary:
			dictionary.append(ref[0])
		if ref[1] not in dictionary:
			dictionary.append(ref[1])
	n=len(dictionary)
	adjlist = []
	for j in range(0,n):
		node=[]
		for i in range(4,4+notl):
			ref=lines[i].split(' ')
			if (dictionary[j]==ref[0]):
				node.append([ref[1],int(ref[2])])
		adjlist.append(node)     
	print (adjlist)        
	'''
	**** Initializing the No. of Nodes in Sunday Traffice ****
	**** Initializing Heuristics List ****
	'''
	nosl=int(lines[4+notl])
	heuristics=[0]*nosl
	'''
	**** Adding Values in Heuristic List ****
	'''
	for i in range(4+notl+1,4+notl+nosl):
		ref=lines[i].split(' ')
		heuristics[dictionary.index(ref[0])]=int(ref[1])
	algo.upper()
	algo.strip()
	if algo=="BFS":
		bfs(ipfile,startstate,n,endstate,dictionary,adjlist)
	elif algo=="DFS":
		dfs(ipfile,startstate,n,endstate,dictionary,adjlist)
	elif algo=="UCS":
		ucs(ipfile,startstate,n,endstate,dictionary,adjlist)
	elif algo=="A*":
		Astar(ipfile,startstate,n,endstate,dictionary,adjlist,heuristics)
	
def output():
    op="output.txt"
    f=open(op,"w")
    #f=open("output.txt","w")
    ''' **** Writing to output.txt **** '''
    while finalop:
        temp=finalop.pop()
        #print(temp[0],temp[1],file=f)
        f.write(temp[0]+" "+str(temp[1])+"\n")
    f.close()
	
def bfs(ipfile,startstate,n,endstate,dictionary,adjlist):
    ''' **** Initializing The Variables **** '''
    print("BFS")
    close=[]
    goal=False
    opened = []
    ''' **** Adding startstate to StartNode **** '''
    StartNode=[startstate,0,int(-1)]
    ''' **** Putting StartNode in Open Queue **** '''    
    opened.append(StartNode)
    ''' **** Traversing The Adjacency List and Adding Nodes to Open and Close **** '''    
    while (goal!=True):
        if opened:
            start=opened.pop(0)
        else:
            break
        close.append(start)
        lenclose=len(close)
        if (close[len(close)-1][0]==endstate):
            goal=True
            temp=[endstate,int(start[1]+1),int(len(close)-1)]
            break
        node=dictionary.index(start[0])
        l=len(adjlist[node])
        for i in range (0,len(adjlist[node])):
            ele=adjlist[node][i][1]
            if dictionary[i] not in close:
                temp=[adjlist[node][i][0],int(start[1]+1),int(len(close)-1)]
                opened.append(temp)        
    ''' **** Adding The path to the Finalop List which is then popped to the output **** '''
    finalop=[]
    finalop.append(close[int(len(close)-1)])
    while finalop[int(len(finalop)-1)]!= close[0]:
        tempo=finalop[int(len(finalop)-1)][2]
        finalop.append(close[tempo])
        output()
        
def ucs(ipfile,startstate,n,endstate,dictionary,adjlist):
    ''' **** Initializing The Variables **** '''
    print("UCS")
    close=[]
    goal=False
    opened = []
    ''' **** Adding startstate to StartNode **** '''
    StartNode=[startstate,0,int(-1)]
    ''' **** Putting StartNode in Open Queue **** '''    
    opened.append(StartNode)
    ''' **** Traversing The Adjacency List and Adding Nodes to Open and Close **** '''    
    while (goal!=True):
        if opened:
            start=opened.pop(0)
        else:
            break
        close.append(start)
        lenclose=len(close)
        if (close[len(close)-1][0]==endstate):
            goal=True
            temp=[endstate,int(start[1]+1),int(len(close)-1)]
            break
        node=dictionary.index(start[0])
        l=len(adjlist[node])
        for i in range (0,len(adjlist[node])):
            ele=adjlist[node][i][1]
            if dictionary[i] not in close:
                temp=[adjlist[node][i][0],int(start[1]+ele),int(len(close)-1)]
                opened.append(temp)
                opened.sort(key=lambda x: x[1])
    ''' **** Adding The path to the Finalop List which is then popped to the output **** '''
    finalop=[]
    finalop.append(close[int(len(close)-1)])
    while finalop[int(len(finalop)-1)]!= close[0]:
        tempo=finalop[int(len(finalop)-1)][2]
        finalop.append(close[tempo])
    output()

def dfs(ipfile,startstate,n,endstate,dictionary,adjlist):
    ''' **** Initializing The Variables **** '''
    print("DFS")
    close=[]
    goal=False
    opened = []
    ''' **** Adding startstate to StartNode **** '''
    StartNode=[startstate,0,int(-1)]
    ''' **** Putting StartNode in Open Queue **** '''    
    opened.append(StartNode)
    ''' **** Traversing The Adjacency List and Adding Nodes to Open and Close **** '''    
    visited=[0]*n
    while (goal!=True):
        v=True
        sadalist=[]
        if opened:
            start=opened.pop()
            while v:
                if(visited[dictionary.index(start[0])]!=1):
                    close.append(start)
                    visited[dictionary.index(start[0])]=1
                    v=False
                else:
                    start=opened.pop()
        else:
            break
        count=0
        if (close[len(close)-1][0]==endstate):
            goal=True
            for openrow in opened:
                if(openrow[0]==endstate):
                    if(openrow[1]<close[len(close)-1][1]):
                        close.append(openrow)                
            temp=[endstate,int(start[1]+1),int(len(close)-1)]
            break
        node=dictionary.index(start[0])
        l=len(adjlist[node])
        for i in range (0,len(adjlist[node])):
            ele=adjlist[node][i][1]
            if dictionary[i] not in close:
                temp=[adjlist[node][i][0],int(start[1]+1),int(len(close)-1)]
                sadalist.append(temp)
        while sadalist:
            opened.append(sadalist.pop())                
    ''' **** Adding The path to the Finalop List which is then popped to the output **** '''
    finalop=[]
    finalop.append(close[int(len(close)-1)])
    while finalop[int(len(finalop)-1)]!= close[0]:
        tempo=finalop[int(len(finalop)-1)][2]
        finalop.append(close[tempo])
    output()
	
def Astar(ipfile,startstate,n,endstate,dictionary,adjlist,heuristics):
    ''' **** Initializing The Variables **** '''
    print("A*")
    close=[]
    goal=False
    opened = []
    ''' **** Adding startstate to StartNode **** '''
    StartNode=[startstate,0,int(-1),heuristics[dictionary.index(startstate)]]
    ''' **** Putting StartNode in Open Queue **** '''    
    opened.append(StartNode)
    ''' **** Traversing The Adjacency List and Adding Nodes to Open and Close **** '''    
    ele=0
    while (goal!=True):
        if opened:
            start=opened.pop(0)
        else:
            break
        close.append(start)
        lenclose=len(close)
        if (close[len(close)-1][0]==endstate):
            goal=True
            temp=[endstate,int(start[1]+1),int(len(close)-1),int(start[1]+ele+heuristics[dictionary.index(endstate)])]
            break
        node=dictionary.index(start[0])
        l=len(adjlist[node])
        for i in range (0,len(adjlist[node])):
            ele=adjlist[node][i][1]
            if dictionary[i] not in close:
                temp=[adjlist[node][i][0],int(start[1]+ele),int(len(close)-1),int(start[1]+ele+heuristics[dictionary.index(endstate)])]
                opened.append(temp)
                opened.sort(key=lambda x: x[1])
    ''' **** Adding The path to the Finalop List which is then popped to the output **** '''
    finalop=[]
    finalop.append(close[int(len(close)-1)])
    while finalop[int(len(finalop)-1)]!= close[0]:
        tempo=finalop[int(len(finalop)-1)][2]
        finalop.append(close[tempo])
    f=open("output.txt","w")
    ''' **** Writing to output.txt **** '''
    while finalop:
        temp=finalop.pop()
        f.write(temp[0]+" "+str(temp[1])+"\n")
    output()	

import os
close=[]
goal=False
opened = []
finalop=[]
startstate="s"
endstate="e"
n=0
dictionary=[]
path="input.txt"
count=0
ipdirs=os.listdir(path)
for file in ipdirs:
        ipfile=path
        mainprog(ipfile)
'''
**** Initializing ref - temporary list to store each item in a line ****
**** Initializing dictionary - Storing nodes as they come in the edges ****
'''
ref=[]
dictionary=[]


