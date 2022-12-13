'''Solution to the Assignment2:
 Firstly I iterated over the objects and checked whether the collisions between the i and i+1 objects is valid if
 its is then I inserted it in my heap as a tuple of total time taken for that collsion plus the current time and the index of colliding ball.
 as well as keep track of the current valid collisions times in an array named "track".
 Then we will run a while loop until the number of collisions or the current time reaches m or T whichever earlier .
 We will remove the minimum time from heap and also since that collision will affect the collisions between j j-1 j+1 and j+2 ,So we will append their valid collisions
 time in heap and also update the track array so that if in future that previous node comes at min position in heap with previous time value we will eliminate it by matching
 it with the track time.

'''
class Warning(Exception):#ADT for modifying error exceptions
    pass

class PriorityQ:#Priority queue base class
    class _qnode:#node of the queue to store time and index value
        __Slots__ = '_time', '_index'

        def __init__(self, timecur, indexcur):
            self._time =  timecur
            self._index = indexcur
        #overloading < == operator
        def __lt__(self, other):
            return self._time < other._time
        def __eq__(self, other):
            return self._time == other._time 
    def empty(self):
        return len(self) == 0
class HeapPQ(PriorityQ): #ADT heap  based on the priority queue
    def _parentnode(self, p): #the parent node of the node at index p of the array would be at (p-1) // 2 index
        return (p-1) // 2
    def _leftnode(self, p):#the left child node of the node at index p of the array would be at 2*p+1 index
        return 2*p+1
    def _rightnode(self, p):#the right child node of the node at index p of the array would be at 2*p+2 index
        return 2*p+2
    def _existleft(self, p):
        return self._leftnode(p) < len(self._prioqu) 
    def _existright(self, p):
        return self._rightnode(p) < len(self._prioqu) 
    def _change(self, p, q):#For swapping the nodes 
        self._prioqu[p], self._prioqu[q] = self._prioqu[q], self._prioqu[p]
    def _heap_up(self, p):#to heap up the node and restructure the tree
        parentnode = self._parentnode(p)
        if p > 0 and self._prioqu[p] < self._prioqu[parentnode]:
            self._change(p, parentnode)
            self._heap_up(parentnode)
    def _heap_down(self, p):#to heap down the node and restructure the tree
        if self._existleft(p):
            left = self._leftnode(p)
            small_child = left 
            if self._existright(p):
                right = self._rightnode(p)
                if self._prioqu[right] < self._prioqu[left]:
                    small_child = right

                
            if self._prioqu[small_child] < self._prioqu[p]:
                self._change(p, small_child)
                self._heap_down(small_child)
            if self._prioqu[small_child]==self._prioqu[p]:
                self._prioqu[small_child]._index,self._prioqu[p]._index=self._prioqu[p]._index,self._prioqu[small_child]._index
            
    def __init__ (self):#initialising the heap with an empty array
        self._prioqu = [ ]
    def __len__ (self):#overloading len operator
        return len(self._prioqu)
    def insert(self, tt, ii):#inserting a node in heap and then restructuring it by heap down
        self._prioqu.append(self._qnode(tt,ii))
        self._heap_up(len(self._prioqu) - 1) 
    def min(self):#min value of heap 
        if self.empty( ):
            raise Warning( 'Priority queue is empty. ')
        qNode= self._prioqu[0]
        return (qNode._time, qNode._index)
    def remove_min_val(self):#removing min value of heap
        if self.empty( ):        
            raise Warning( 'Priority queue is empty' )
        self._change(0, len(self._prioqu) - 1) 
        qNode = self._prioqu.pop( ) 
        self._heap_down(0) 
        return (qNode._time,qNode._index)
    
    def __str__(self) -> str:#for representation of array
        return str([(x._time,x._index) for x in self._prioqu])
        




def after_collision_velocity(m1,m2,u1,u2):
    #calculating the velocities after collision for the colliding  objects 
    v1=(((m1-m2)*u1)/(m1+m2))+((2*m2*u2)/(m1+m2))
    v2=((2*m1*u1)/(m1+m2))+((m2-m1)*u2)/(m1+m2)
    return v1,v2
def after_collision_pos(x1,v1,t,prevt):#after collision position of object 
    pos=x1+v1*(t-prevt)
    return pos

def valid_collision(u1,u2):
    #accounting for cases of valid collisions between two objects
   
    if (u1>0 and u2>0) or (u1<0 and u2<0) :
        if (u1<=u2):
            return False
        else:
            return True
    elif (u1>0 and u2<0):
        return True
    elif (u1<0 and u2>0):
        return False
    elif u1==0:
        if u2>=0:
            return False
        elif u2<0:
            return True
    elif u2==0:
        if u1>0:
            return True
        elif u1<=0:
            return False
def timecalc(x1,x2,u1,u2):
    #calculating time of collision between two objects impending to collide 
    dist=(x2-x1)
    rel_vel=(u2-u1)
    timetaken=abs(dist/rel_vel)
    return timetaken

def check(p,track):
        #varifying whether the top / min node of the heap is not the node to be eliminated and if it is we remove it.
        t1,j1=p.min()[0],p.min()[1]
        if track[j1]==t1:
            return
         
        else:
            
            p.remove_min_val()
            
            check(p,track)

def listCollisions(M,x,v,m,T):#O(n+mlogn)
    
    n=len(M)#no of objects
    
    t=0                 #initial time 
    collisions=0        #initial collisions
    collision_list=[]   #initial list
    p=HeapPQ()          #initial heap
    
    track=[None]*n      #initial track array
    for i in range(n-1):#iterating for valid collisions O(n)
        
        if valid_collision(v[i],v[i+1]):
            timetaken=timecalc(x[i],x[i+1],v[i],v[i+1])
            p.insert(timetaken,i) #inserting in heap
            track[i]=timetaken  #updating track 
    prev=[0]*n   # maintaining the array of previous times of collision
    

    if p.empty():  # checking if no collisions
        return collision_list
    while  (not p.empty()) and  collisions<=m and t<=T:  #termination conditions
        
        check(p,track)  #checking array for nodes to be eliminated 
        t,j=p.remove_min_val()  #updating  values O(logn)
        
        collisions+=1       
        
        x[j]=after_collision_pos(x[j],v[j],t,prev[j])   
        x[j+1]=after_collision_pos(x[j+1],v[j+1],t,prev[j+1])


        v[j],v[j+1]=after_collision_velocity(M[j],M[j+1],v[j],v[j+1])

        if collisions<=m and t<=T:
            collision_list.append((round(t,4),j,round(x[j],4)))
        
        prev[j]=t
        prev[j+1]=t
        

        for i in [j-1,j,j+1]: #reinserting the impacted collisions
            if i>=0 and i<n-1:

                
                if valid_collision(v[i],v[i+1]):
                    
                    timetaken=timecalc(after_collision_pos(x[i],v[i],t,prev[i]),after_collision_pos(x[i+1],v[i+1],t,prev[i+1]),v[i],v[i+1])
                    
                    track[i]=t+timetaken 
                    p.insert(t+timetaken,i)
    return collision_list
