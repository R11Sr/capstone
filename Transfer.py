import queue
from dataclasses import dataclass, field
from typing import Any
from Course import *


"""Possible things for UI
max requeue attempts

"""


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
        self.CAIdecimal = None
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
        #CAI,16 bit gene sequence interpreted as  sign(0)0.0000 0000 0000 00
        self.CAIgenome = self.geneotype[18:34]
        self.setDecimalCAI()
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

    def getMaxRequeueAttempts(self) -> int:
        return self.MAXIMUM_REQUEUE_ATTEMPTS


    
    def setDecimalCAI(self):
        gene = self.CAIgenome
        def parse_bin(s):
            return int(s[1:], 2) / 2.**(len(s) - 1)

        if gene[0]:
             self.setDecimalCAI =  float(f'{gene[1]}') + parse_bin(fraction)
        else:
            self.setDecimalCAI = - float(f'{gene[1]}') - parse_bin(fraction)
        


    
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
    def enqueuePriority(self,priority: int, session: Session) ->None:
        if self.isPriorityQueueAvailable():
            self.priorityqueue.put(priority,session)
        else:
            raise Exception("The Queue must exist before elements can be added to it.")

    def enqueueFIFO(self,session: Session) -> None:
        if self.isFIFOQueueAvailable():
            self.fifoqueue.put(session)
        else:
            raise Exception("The Queue must exist before elements can be added to it.")


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
    
    def inCAI(self,session: Session, location: int)-> bool:
        const =  self.CAIgenome
    def inLecturerPref(self,session: Session, location: int)-> bool:
        pass
    def inClashConstraint(self,session: Session, location: int)-> bool:
        pass
    def inRoomProximity(self, session: Session, location: int) -> bool:
        pass

    def CAI(self,session: Session, location: int)-> float:
        pass
    def LecturerPref(self,session: Session, location: int)-> float:
        pass
    def ClashConstraint(self,session: Session, location: int)-> float:
        pass
    def RoomProximity(self, session: Session, location: int) -> float:
        pass

    def filter(self,session: Session) -> list:

        placementPoints=[]
        for spot in range(0,self.timeTable.length):
            '''available location should be a list [(score: float,location: list)]
                eg. for a session [(5.322,6),(7.456,8)]'''
            
            if self.isValid(session.getTimeSpan(),spot):
                cai = self.CAI(session,spot)
                LecturerPref = self.LecturerPref(session,spot)
                clash = self.clash(session,spot)
                RoomProximity = self.RoomProximity(session,spot)

                total = cai + LecturerPref + clash + RoomProximity

                placementPoints.append((total,spot))      

        return placementPoints



    def placeSession(self,session: Session,location= int) -> bool:
        length = session.getTimeSpan()
        
        if self.isValid(length,location):
            session.useEnergy()
            for time in range(0,length): 
                '''Add the price paid in this session'''  
                             
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


    def checkAllHardConstraint(self,session: Session, spot: int) -> list:
            cai = self.inCAI(session,spot)
            clash = self.inclash(session,spot)

            return [cai,clash]
            
        
    def PriorityQStraightOrder(self) -> list:
        self.buildPriorityQueue()

        if self.isPriorityQueueAvailable():
            for session in self.allSessions:
                self.enqueuePriority(self,session.getPriority(),session)
        
        while not self.priorityqueue.empty():
            session = self.priorityqueue.get()

            '''available location should be a list [(score: int,location: list)]
                eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
            allLocations = self.filter(session,self.getTimeTable())
            val = lambda tup: tup[0]
            allLocations.sort(key=val)

            if allLocations:
                location = allLocations.pop()
                if all(self.checkAllHardConstraint(session,location)): 
                    self.placeSession(session,location)
                elif session.getAttempts() >= self.getMaxRequeueAttempts:
                    self.placeSession(session,location)
                else:
                    session.useAttempt()
                    self.enqueuePriority(self,session.getPriority(),session)

        return self.priorityqueue



            

            
    def PriorityQReverseOrder(self) -> list:
        self.buildPriorityQueue()

        if self.isPriorityQueueAvailable():
            for session in self.allSessions:
                self.enqueuePriority(self,session.getPriority(),session)
        
        while not self.priorityqueue.empty():
            session = self.priorityqueue.get()

            '''available location should be a list [(score: int,location: list)]
                eg. for 2 hr session [(5,[6,11]),(7,[8,13])]'''
            allLocations = self.filter(session,self.getTimeTable())
            val = lambda tup: tup[0]
            allLocations.sort(key=val)

            if allLocations:
                location = allLocations.pop()
                if all(self.checkAllHardConstraint(session,location)): 
                    self.placeSession(session,location)
                elif session.getAttempts() >= self.getMaxRequeueAttempts:
                    self.placeSession(session,location)
                else:
                    session.useAttempt()
                    self.enqueuePriority(self,session.getPriority(),session)

        return self.priorityqueue
    def FIFOQStraightOrder(self )-> list:
        pass
    def FIFOQReveseOrder(self) -> list:
        pass
    def IterativeStraightOrder(self) -> list:
      pass
    def IterativeReverseOrder(self) -> list :
      pass
        
                    


        
