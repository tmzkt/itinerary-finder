import dataAccess
import network
import tripPlan
class BusLogic:
    def __init__(self):
        self._da = dataAccess.DataAccess()
        self._trains = self._getTrains()
        self._network = network.Network(self._trains)
        self._tripPlans = tripPlan.TripPlans(self._trains, self._da.loadPassengerScheduleRequests())
    def saveNetwork(self):
        self._da.saveNetwork(self._network)
    def outputNetwork(self, nodesFileName, arcsFileName):
        self._network.dumpToFiles(nodesFileName, arcsFileName)
    def saveTripPlans(self):
        self._da.saveTripPlans(self._tripPlans)
    def outputTripPlans(self, fileName):
        self._tripPlans.dumpToFile(fileName)
    def _getTrains(self):
        trains = self._da.loadTrains()
        trainRoutes = self._da.loadTrainRoutes()
        idx = 0
        for train in trains:
            while idx < len(trainRoutes) and train.trainId == trainRoutes[idx].trainId:
                train.trainRoutes.append(trainRoutes[idx])
                idx += 1
        return trains