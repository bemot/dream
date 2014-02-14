from dream.simulation.imports import Machine, Source, Exit, Part, Queue, G, Globals, Failure 
from dream.simulation.imports import simulate, activate, initialize, infinity

#the custom queue
class SelectiveQueue(Queue):
    def haveToDispose(self,callerObject=None):
        caller=callerObject
        # if the caller is M1 then return true if there is an Entity to give
        if caller.id=='M1':
            return len(self.getActiveObjectQueue())>0
        # else return true only if M1 cannot accept the Entity
        if caller.id=='M2':
            # find M1
            M1=Globals.findObjectById('M1') # global method to obtain an object from the id
            return len(self.getActiveObjectQueue())>0 and (not (M1.canAccept()))
        
#define the objects of the model
S=Source('S','Source', mean=0.5, item=Part)
Q=SelectiveQueue('Q','Queue', capacity=infinity)
M1=Machine('M1','Milling1', mean=0.25)
M2=Machine('M2','Milling2', mean=0.25)
E=Exit('E1','Exit')  

F=Failure(victim=M1, distributionType='Fixed', MTTF=60, MTTR=5)

G.ObjList=[S,Q,M1,M2,E]   #add all the objects in G.ObjList so that they can be easier accessed later

G.ObjectInterruptionList=[F]     #add all the objects in G.ObjList so that they can be easier accessed later


#define predecessors and successors for the objects    
S.defineRouting([Q])
Q.defineRouting([S],[M1,M2])
M1.defineRouting([Q],[E])
M2.defineRouting([Q],[E])
E.defineRouting([M1,M2])

initialize()                        #initialize the simulation (SimPy method)
    
for object in G.ObjList:
    object.initialize()
    
for objectInterruption in G.ObjectInterruptionList:
    objectInterruption.initialize()

#activate all the objects 
for object in G.ObjList:
    activate(object, object.run())

for objectInterruption in G.ObjectInterruptionList:
    activate(objectInterruption, objectInterruption.run())

G.maxSimTime=1440.0     #set G.maxSimTime 1440.0 minutes (1 day)
    
simulate(until=G.maxSimTime)    #run the simulation

#carry on the post processing operations for every object in the topology       
for object in G.ObjList:
    object.postProcessing()

#print the results
print "the system produced", E.numOfExits, "parts"
print "the working ratio of", M1.objName,  "is", (M1.totalWorkingTime/G.maxSimTime)*100, "%"
print "the working ratio of", M2.objName,  "is", (M2.totalWorkingTime/G.maxSimTime)*100, "%"
