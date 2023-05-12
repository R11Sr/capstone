import queue
import scipy.stats as stats
import statistics
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
        self.timeUtilisationGenome = None """This is to remove"""
        self.placementUrgency = None # eager or lazy placement
        self.MAXIMUM_REQUEUE_ATTEMPTS = None
        self.CLASH_PERCENT_INDEX = 0.025
        self.LECTURER_PREF_INDEX = 0.1
        self.allSessions = courseAndSessionListing
        self.placeDict = None


        


    """
        Description of the Queues:
        Back ->[*,*,*,*,*,*,*,*,*,*,*,*,*,*] <- Front
    """
 
    def setAttibutes(self):
        self.lecturePrefGeneome = self.geneotype[:3]
        self.clashGenone = self.geneotype[3:15] """Will need to reduce to 4 bits """
        self.roomProximityGenome = self.geneotype[15:18]
        #CAI,16 bit gene sequence interpreted as  sign(0)0.0000 0000 0000 00
        self.CAIgenome = self.geneotype[18:34]
        self.CAIconstraintDecimal = None
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
        self.placeDict['110'] = 'IterativeStraightOrder'  #tentative
        self.placeDict['010'] = 'IterativeReverseOrder'   #tentative

    """_summary_
        Responsible for setting the total number of attempts that can be made to requeue a session
        if conditions are unfavorable for its placement.
        it calculates the number by converted the placement urgency bit string to its decimal 
        value and then to increase the number of attempts its is arbitrarily multiplied by 5.
    """
    def setMaxRequeueAttempts(self) ->None:
            totalReQattempts =  int(self.placementUrgency,2) * 5 
            self.MAXIMUM_REQUEUE_ATTEMPTS = totalReQattempts

    def getMaxRequeueAttempts(self) -> int:
        return self.MAXIMUM_REQUEUE_ATTEMPTS


    # This also normalises the data. In that it changes the values from the range of -1 to 1, to 0 to 2.
    # makes it easier when running a minimising GA
    def setDecimalCAI(self):
        gene = self.CAIgenome
        def parse_bin(s):
            return int(s[1:], 2) / 2.**(len(s) - 1)
        
        fraction = '.' + gene[2:]

        if gene[0]:
            _ =  float(f'{gene[1]}') + parse_bin(fraction)
            self.CAIconstraintDecimal = 1 + _ 

        else:
            self.CAIconstraintDecimal = - float(f'{gene[1]}') - parse_bin(fraction)
        


    
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
        19    [56],[57],[58],[59],[60],
        20    [61],[62],[63],[64],[65],
        ]
            Remember to block out CLUB time 
            Remember to block out time for other DEPT
    
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
    
    def inCAI(self,s1: Session,location: int)-> bool:
        if self.CAI(s1,location) <= self.CAIconstraintDecimal:
            return True
        return False
    
    def inLecturerPref(self,session: Session, location: int)-> bool:
        pass
    def inClashConstraint(self,session: Session, location: int)-> bool:
        pass
    def inRoomProximity(self, session: Session, location: int) -> bool:
        pass

    def CAI(self,s1: Session, location: int)-> float:
        
        #if there is one or more courses in the spot
        if self.getTimeTable[location]:
            list_of_cai =[]
            for existingSession in self.getTimeTable[location]:
                #get all the majors for a selected course

                """
                CC          Majors
                INFO2180    Computer Science, Actorial Science, Marketing
                COMP1161    Information technology,Computer Science
                .......     ........
                """
                existingSessionMajor = allcourses[f'{existingSession.getcourseCode()}'].getMajors()
                s1Mojor = allcourses[f'{s1.getcourseCode()}'].getMajors()

                # if there exists majors between the current courses(likely students did both) run the kendal Tau
                for key in existingSessionMajor.keys():
                    if key in s1Mojor:
                        # print(key, "exists in both dictionaries")
                        """
                        YEAR    AMOUNT ENROLLED
                        2017        185
                        2016        155
                        2015        145
                        """
                        c1Data = allCoursesRegistration[f'{s1.getcourseCode()}']
                        c2Data = allCoursesRegistration[f'{existingSessionMajor.getcourseCode()}']
                        
                        
                        cai = self.kendalTau(c1Data,c2Data)

                        """Transform the data from the range -1 to 1, to 0 to 2.
                        Makes it easier when running a minimizing algorithm"""

                        if cai > 0:
                            cai +=1
                        elif cai < 0:
                            cai = abs(cai)
                        else:
                            cai = 0
                        list_of_cai.append(cai)
                        return statistics.mean(list_of_cai)
        else:
            return 0

    def kendalTau(c1Data: dict,c2Data: dict) ->float:
        tauList = []
        for key in c1Data:
            tau, p_value = stats.kendalltau(c1Data[key],c2Data[key])
            tauList.append(tau)
    
    """Weighting table
        Hrs outside     weight
        1               0.1
        2               0.2
        3               0.3
        4               0.4
        5               0.5
        6               0.6
    
    """
    def LecturerPref(self,session: Session, location: list)-> float:
        lectPrefTimes = allLecturerTimes[f'{session.facilitator}']
        lectPrefTimes.sort()
        timeDiff = 0

        timedict = self.makeTimedictionary()
        timesOfSesison = []
        for t in location:
            timesOfSesison.append(timedict[t])
        
        timesOfSesison.sort()


        if all(item in lectPrefTimes for item in timesOfSesison):
            timeDiff = 0
        else:
            Lset = set(lectPrefTimes)
            Sset = set(timesOfSesison)

            diff = Lset - Sset

            #if session is ahead of lect pref
            if Sset.pop(0) > Lset.pop():
                timeDiff = Sset.pop(0) - Lset.pop()
            else:
                # session behind lectPref
                timeDiff = Lset.pop(0) - Sset.pop()
                
        return timeDiff * self.LECTURER_PREF_INDEX
        



    def makeTimedictionary(self) ->dict:
        timedict = {}
        timedict['8'] = 1
        timedict['8'] = 2
        timedict['8'] = 3
        timedict['8'] = 4
        timedict['8'] = 5
        timedict['9'] = 6
        timedict['9'] = 7
        timedict['9'] = 8
        timedict['9'] = 9
        timedict['9'] = 10
        timedict['10'] = 11
        timedict['10'] = 12
        timedict['10'] = 13
        timedict['10'] = 14
        timedict['10'] = 15
        timedict['11'] = 16
        timedict['11'] = 17
        timedict['11'] = 18
        timedict['11'] = 19
        timedict['11'] = 20
        timedict['12'] = 21
        timedict['12'] = 22
        timedict['12'] = 23
        timedict['12'] = 24
        timedict['12'] = 25
        timedict['13'] = 26
        timedict['13'] = 27
        timedict['13'] = 28
        timedict['13'] = 29
        timedict['13'] = 30
        timedict['14'] = 31
        timedict['14'] = 32
        timedict['14'] = 33
        timedict['14'] = 34
        timedict['14'] = 35
        timedict['15'] = 36
        timedict['15'] = 37
        timedict['15'] = 38
        timedict['15'] = 39
        timedict['15'] = 40
        timedict['16'] = 41
        timedict['16'] = 42
        timedict['16'] = 43
        timedict['16'] = 44
        timedict['16'] = 45
        timedict['17'] = 46
        timedict['17'] = 47
        timedict['17'] = 48
        timedict['17'] = 49
        timedict['17'] = 50
        timedict['18'] = 51
        timedict['18'] = 52
        timedict['18'] = 53
        timedict['18'] = 54
        timedict['18'] = 55
        timedict['19'] = 56
        timedict['19'] = 57
        timedict['19'] = 58
        timedict['19'] = 59
        timedict['19'] = 60
        timedict['20'] = 61
        timedict['20'] = 62
        timedict['20'] = 63
        timedict['20'] = 64
        timedict['20'] = 65

        return timedict


    """
    What percentage of students of that slot hav clashes 
    e.g. 3 sessions in slot totaling 150 students 50 have clash with 2 or more sessions in slot
    30% clash weighting

    WEIGHTING TABLE FOR % OF STUDENT CLASH
      %             weighting
    0  - 5          0 -0.125
    6  - 10         0.150 - 0.250
    11 - 15         0.275 - 0.375
    16 - 20         0.400 - 0.500
    21 - 25         0.525 - 0.625
    26 - 30         0.650 - 0.750
    31 - 35         0.775 - 0.875
    36 - 40         0.900 - 1.000
    > 40            2.000

    
    Weighting           Clash Meaning
    100.00              Lecturer or room having Simultaneous classes
    0.90                Lab to Lecture
    0.80                Lab to Lab
    0.70                Tutorial to Lecture
    0.60                Lab to Tutorial
    0.50                Seminar to Lecture
    0.40                Seminar to Lab
    0.30                Seminar to Tutorial
    0.20                Tutorial to Tutorial
    0.00                No Clashes


    ENROLLMENT FILE(csv) FOR EACH SESSION to perform the analysis of those in this and the other sessions
    in the spot
    6023332
    6293333
    ......
    """
    def ClashConstraint(self,session: Session, location: int)-> float:
        clashSet = set() # number of students with the clashes
        total = 0
        listFacilitators =[]
        clashPercentScore = 0.00
        sessionEnrolled = set(registration[f'{sessionEnrolled.name}'])


        for existingSession in self.getTimeTable[location]:
            total += len(sessionEnrolled)

            existingSessionEnrolled = set(registration[f'{existingSession.name}'])
            listFacilitators.append(existingSessionEnrolled.facilitator)
            total += len(existingSessionEnrolled)

            clashSet = clashSet | sessionEnrolled | existingSessionEnrolled
            
        # calculates the percentage
        clashPercentage = (float(len(clashSet)) / float(total)) * 100
        
        clashPercentScore = round(clashPercentage) * self.CLASH_PERCENT_INDEX # in accord with clash weighting table above

        # to adhere to weighting table above
        if clashPercentage > 40:
            clashPercentScore = 2.0

        #check if a facilitator will have more than 1 session in that slot
        if session.facilitator in listFacilitators:
            clashPercentScore = 100.00 

        # also check if sessions clash in rooms
        """Rooms with special requirements are not taking into consideration at this time"""
        
        """Select Room for Session"""
        for room in listofRooms:
            if room.capacity < len(sessionEnrolled):
                pass
            else:
                flag = []
                for existingSession in self.getTimeTable[location]:
                    if existingSession.approvedRoom == room.name:
                        flag.append(True)
                    else:
                        flag.append(False)
                if not all(flag):
                    session.tentativeRoom = room.name

        return clashPercentScore
        

        


        




             
             
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
        
                    


        
