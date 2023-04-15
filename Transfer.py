import queue
from dataclasses import dataclass, field
from typing import Any
from Course import *

class Transfer():
    def __init__(self,geneotype:str) -> None:
        self.fifoqueue = None
        self.priorityqueue = None
        self.geneotype = geneotype
        self.timeTable = None
        


    """
        Description of the Queues:
        Back ->[*,*,*,*,*,*,*,*,*,*,*,*,*,*] <- Front
    """
 
  
    def isFIFOQueueAvailable(self)-> bool:
        if self.fifoqueue:
            return True
        return False
    
    def isPriorityQueueAvailable(self) -> bool:
        if self.priority:
            return True
        return False
    def buildFIFOQueue(self,courseListing):
        
        if self.FIFOQueueAvailable():
            for course in courseListing:
                allSessions = course.getSessions()
                for session in allSessions:
                    self.enqueueFIFO(session)

        

    def buildPriorityQueue(self):
        self.priorityqueue = queue.PriorityQueue()

    def buildFIFOQueue(self):
        self.fifoqueue = queue.Queue()

    '''These commented out methods are not supported by the Queue object from Python/Lib'''
    # def front(self):
    #     pass
    # def back(self):
    #     pass

    # This method may not be needed. But just in case. It is there as a wrapper class
    def enqueuePrioity(self):
        pass

    def FIFOrequeue(self,session):
        if self.FIFOQueueAvailable():
            self.fifoqueue.put(session)
    
    def priorityRequeue(self,session):
        
        self.priorityqueue.put((session.getPriority(),session))


    """
        Session Position In Time Table
        [
                M   T   W   Th  F
        8       [1],[2],[3],[4],[5],
        9       [6],[7],[8],[9],[10],
        10    [11],[12],[13],[14],[15],
        11    [16],[17],[18],[19],[20],
        12    [21],[22],[23],[24],[25],
        13    [26],[27],[28],[29],[30],
        14    [31],[32],[33],[34],[35],
        15    [36],[37],[38],[39],[40],
        16    [41],[42],[43],[44],[45],
        17    [46],[47],[48],[49],[50],
        18    [51],[52],[53],[54],[55],
        18    [56],[57],[58],[59],[60],
        19    [61],[62],[63],[64],[65],
        20    [66],[67],[68],[69],[70],

        ]
    
    """
    def generateTimetable(self):
        
        self.timeTable = [
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
            [],[],[],[],[],
        ]
    
    def checkCAI(self):
        pass
    def checkLecturerPref(self):
        pass
    def checkClashConstraint(self):
        pass

    def placeSession(self,session: Session,location= int) -> bool:
        length = session.getTimeSpan()
        
        if self.isValid(length,location):
            for time in range(0,length):                
                self.timeTable[location + 5* time].append(session)
        else:
            session.useEnergy()

    def isValid(self,length: int,location: int) -> bool:
        flag = []
        for time in range(0,length):
            try:
                self.timeTable[location + 5* time]
                flag.append(True)
            except IndexError:
                flag.append(False)
                
        return all(flag)
            
            


        
