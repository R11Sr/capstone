class Transfer():
    def __init__(self,geneotype:str,) -> None:
        self.fifoqueue = None
        self.priority = None
        


    """
        Description of the Queues:
        Back ->[*,*,*,*,*,*,*,*,*,*,*,*,*,*] <- Front
    """
  
    def FIFOQueueAvailable(self):
        if self.fifoqueue:
            return True
        return False
    
    def PriorityQueueAvailable(self):
        if self.priority:
            return True
        return False
    def buildFIFOQueue(self,courseListing):
        
        if FIFOQueueAvailable():
            raise Exception

        

    def buildPriorityQueue(self):
        pass

    def front(self):
        pass
    def back(self):
        pass

    def remove(self):
        pass

    def requeue(self):
        pass


    def generateTimetable(self):
        pass
    
    def checkCAI(self):
        pass
    def checkLecturerPref(self):
        pass
    def checkClashConstraint(self):
        pass

    def placeSession(self):
        pass

        
