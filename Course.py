class Course:

    def __init__(self,courseTitle,courseCode,lectuerName,Components):
        """_summary_
        This is the constructor for the Course object. Before sessions can be generated 
        the Course objects must exists. 

        Args:
            courseTitle (_type_): _description_
            courseCode (_type_): _description_
            lectuerName (_type_): _description_
            Components (_type_): _description_
        """

        self.courseTitle=  courseTitle
        self.courseCode  = courseCode
        self.lectuerName = lectuerName
        self.registrationData = {}

        #components refer to the different session for the course 
        # Lectures, Seminars, Labs, Tutorials
        self.Components = []

        #Lists all session objects for the course, all the lectures, all the tutorals etc. 
        #eg. two sessions for M11, several tutorial sessions T01, T02, T03
        self.sessions = []
       
        for item in Components:
            self.Components.append( item)



        """_summary_
            This expects to receive the registration list for that 
            course as a list of tuples. it will then convert to a dictionary.

            Args:
            registrationList (dictionary): dictionary that contains the year of registration and amount of
            students registered based on the major pursuing.
            eg.reg['2002'] = [(205,'Computer Science'),(304,'Software Engineering'),(180,'Mathematics')]
               reg['2009'] = [(306,'Computer Science'),(507,'Software Engineering'),(254,'Mathematics'),(98,'Electronics')]
        """
    def setPastResgistration(self,registrationList):
             
        self.registrationData = registrationList


        """_summary_
            returns a list of tuples for the registration data for this course for a particular year
        """
    def getRegistrationForYear(self,year):
        return self.registrationData[f'{year}']
    
    def getTitle(self):
        return self.courseTitle 
    
    def getRegistrationData(self) ->dict:
        if bool(self.registrationData):
            return self.registrationData
        return None
    
    def setSessions(self,sessionList):
        self.sessions = sessionList

    def addSession(self,session):
        self.sessions.append(session)

    def createSession(self,faciltator: str,type: str,capacity: int):
        session = Session(faciltator,type,capacity)
        session.setCourse(self.getTitle)
        session.setRegistrationData(self.getRegistrationData)
        self.addSession(session)

        
    
    
    
    

class Session():
    def __init__(self, facilitator: str,type: str,capacity: int) -> None:
        #the person who is in charge of administering this session
        self.facilitator = facilitator

        #course title
        self.course = None

        #the day of this session
        self.day = None

        #the span of time that the session is earmarked for
        self.timeSpan = None

        #the type of session, must be listed in the component of the course
        self.type = type
        
        #the amount of students registered for a course
        self.registered = 0

        #The maximum capacity that this session can accomodate given constraints eg. physical lab components
        #for a lab session
        self.MAXIMUM_CAPACITY = capacity

        #room of the session
        self.room =  None

        #the energy level that this sesison has ie the number of attempts to be placed on time table by the
        #transfer function
        self.energyLevel = 0 #this is arbitrary lilkely will need a gene to decide this

        #this records the amount of times that the transfer function attempts to place the session,
        # gives up due to lack of energy and returns it to the placement queue
        self.placementAttempts = 0

        #check if the session has been placed on the time table
        self.placed = False

        #priority, to be used for the priority queue
        self.priority = None

        #copy of the course registration Data
        self.regdata = None

        #energy that is used to place course on the time table
        self.energyAllocation = {}
        self.energyAllocation['lecture'] = 25
        self.energyAllocation['seminar'] = 12
        self.energyAllocation['lab'] = 8
        self.energyAllocation['tutorial'] = 4 

        self.energyCapacity = self.energyAllocation[f'{type}']

        self.currentLevel = self.energyCapacity

    def setCourse(self, title: str):
        self.course = title

    def getCourseTitle(self) ->str:
        if self.course:
            return self.course
        return None
    
    def getType(self) ->str:
        return self.type
    
    def setRegistrationData(self,data: dict):
        self.regdata = data

    def getRegistrationData(self) ->dict:
        if self.regdata:
            return self.regdata
        return None
    
    def setPriority(self,pri: int):
        self.priority = pri

    def getPriority(self)->int:
        return self.priority
    
    def refill(self):
        self.currentLevel = self.energyCapacity

    def energyAvailable(self)->bool:
         if self.currentLevel >0:
            return True
         return False
    
    def getEnergyLevel(self):
        return self.currentLevel

    def useEnergy(self):
        if self.currentLevel >0:
            self.currentLevel-=1
        else: 
            raise ValueError("Energy cannot go into deficit")
        
    def useAttempt(self):
        self.placementAttempts +=1
    
    def resetAttempt(self):
        self.placementAttempts = 0
        
    def __repr__(self) -> str:
        return f"<course:{self.getCourseTitle()}, session{self.getType()}, energy Level{self.getEnergyLevel()}>"





