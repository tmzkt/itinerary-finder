class Station:
    def __init__(self, stationNum, stationName):
        self.stationNum = stationNum
        self.stationName = stationName

class EventTime:
    def __init__(self, timeHHHMM):
        self.timeHHHMM = timeHHHMM
    def getTimeMMM(self):
        return (self.timeHHHMM // 100 * 60) + self.timeHHHMM % 100
    def getTimeHHMM(self):
        return ((self.timeHHHMM // 100 % 24) * 100) + self.timeHHHMM % 100
    def getTimeDDD(self):
        return self.timeHHHMM // 100 // 24

class Train:
    def __init__(self, trainId, trainCategory, daysOperated):
        self.trainId = trainId
        self.trainCategory = trainCategory
        self.daysOperated = daysOperated
        self.trainRoutes = []

class TrainRoute:
    def __init__(self, trainId, station, arrivalTime, departureTime):
        self.trainId = trainId
        self.station = station
        self.arrivalTime = arrivalTime
        self.departureTime = departureTime

class PassengerScheduleRequest:
    def __init__(self, passengerId, origStation, destStation, departTime):
        self.passengerId = passengerId
        self.origStation = origStation
        self.destStation = destStation
        self.departTime = departTime
