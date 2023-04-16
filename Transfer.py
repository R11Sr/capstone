import queue
from dataclasses import dataclass, field
from typing import Any
from Course import *

class Transfer():
    def __init__(self,geneotype:str,courseAndSessionListing: list) -> None:
        self.fifoqueue = None
        self.priorityqueue = None
        self.geneotype = geneotype
        self.timeTable = None
        self.lecturePrefGeneome = None
        self.clashGenone = None
        self.roomProximityGenome = None
        self.CAIgenome = None
        self.timeUtilisationGenome = None
        self.placementUrgency = None # eager or lazy placement
        self.MAXIMUM_REQUEUE_ATTEMPTS = None
        self.allSessions = courseAndSessionListing
        self.placeDict = None


        


    """
        Description of the Queues:
        Back ->[*,*,*,*,*,*,*,*,*,*,*,*,*,*] <- Front
    """
 
    def setAttibutes(self):
        self.lecturePrefGeneome = self.geneotype[:3]
        self.clashGenone = self.geneotype[3:15]
        self.roomProximityGenome = self.geneotype[15:18]
        self.CAIgenome = self.geneotype[18:34]
        self.placementPlan=self.geneotype[34:37]
        self.placementUrgency= self.geneotype[37:42]
        self.setMaxRequeueAttempts()
        self.timeUtilisationGenome = self.geneotype[42:]



    def makeplacementPlans(self):
        self.placeDict  ={}
        self.placeDict['100'] = 'PriorityQStraightOrder'
        self.placeDict['000'] = 'PriorityQReverseOrder'
        self.placeDict['101'] = 'FIFOQStraightOrder'
        self.placeDict['001'] = 'FIFOQReveseOrder'
        self.placeDict['110'] = 'IterativeStraightOrder'
        self.placeDict['010'] = 'IterativeReverseOrder'

    """_summary_
        Responsible for setting the total number of attempts that can be made to requeue a session
        if conditions are unfavorable for its placement.
        it calculates the number by converted the placement urgency bit string to its decimal 
        value and then to increase the number of attempts its is arbitrarily multiplied by 5.
    """
    def setMaxRequeueAttempts(self) ->None:
            totalReQattempts =  int(self.placementUrgency,2) *5 
            self.MAXIMUM_REQUEUE_ATTEMPTS = totalReQattempts

    def isFIFOQueueAvailable(self)-> bool:
        if self.fifoqueue:
            return True
        return False
    
    def isPriorityQueueAvailable(self) -> bool:
        if self.priority:
            return True
        return False
    def buildFIFOQueue(self,courseListing) ->None:
        
        if self.FIFOQueueAvailable():
            for course in courseListing:
                allSessions = course.getSessions()
                for session in allSessions:
                    self.enqueueFIFO(session)

        

    def buildPriorityQueue(self) ->None:
        self.priorityqueue = queue.PriorityQueue()

    def buildFIFOQueue(self) ->None:
        self.fifoqueue = queue.Queue()

    '''These commented out methods are not supported by the Queue object from Python/Lib'''
    # def front(self):
    #     pass
    # def back(self):
    #     pass

    # This method may not be needed. But just in case. It is there as a wrapper class
    def enqueuePrioity(self) ->None:
        pass

    def FIFOrequeue(self,session: Session) ->None:
        if self.FIFOQueueAvailable():
            self.fifoqueue.put(session)
    
    def priorityRequeue(self,session: Session) ->None:
        
        self.priorityqueue.put((session.getPriority(),session))


    def getTimeTable(self) ->list:
        return self.timeTable
    
    def setTimeTable(self,tt: list)-> None:
        self.timeTable = tt

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
            Remember to block out CLUB time 
            Remember to block out time for other DEPT
        ]
    
    """
    def generateTimetable(self) ->None:
        
        timeTable = [
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
        #block out club time

        self.setTimeTable(self,timeTable)
    
    def checkCAI(self):
        pass
    def checkLecturerPref(self):
        pass
    def checkClashConstraint(self):
        pass

    def filter(self):
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
            

    def execute(self) ->list:

        self.setAttibutes()
        self.generateTimetable()
        self.makeplacementPlans()

        if self.getPlacement() in self.placeDict:
            self.placeDict[self.getPlacement()]()
        else:
            """ The placement gene is invalid and this time table should be discarded"""

        
            
        
    def PriorityQStraightOrder(self) -> list:
        pass
    def PriorityQReverseOrder(self) -> list:
        pass
    def FIFOQStraightOrder(self )-> list:
        pass
    def FIFOQReveseOrder(self) -> list:
        pass
    def IterativeStraightOrder(self) -> list:
      pass
    def IterativeReverseOrder(self) -> list :
      pass
        
                    


        
