import network

class AcyclicShortestPath:
    def __init__(self, network):
        self.nodes = sorted(network.nodes, key = lambda node: node.station.stationNum)
        self.nodes = sorted(self.nodes, key = lambda node: node.eventTime.timeHHHMM)
    def findNodeGivenStationAndTime(self, station, eventTime):
        for i,node in enumerate(self.nodes):
            if node.eventTime.timeHHHMM >= eventTime.timeHHHMM and node.station.stationNum == station.stationNum:
                return i
        return -1
    def findPath(self, startStation, startTime, endStation):
        path = []
        idx = self.findNodeGivenStationAndTime(startStation, startTime)
        if idx == -1:
            return path # no initial node, so no path can be found
        for node in self.nodes[idx + 1:]:
            node.predecessorNode = None
            node.totalCost = float('inf')
        self.nodes[idx].predecessorNode = None
        self.nodes[idx].totalCost = 0
        
        theNode = None
        for node in self.nodes[idx:]:
            if node.station.stationNum == endStation.stationNum and node.predecessorNode != None:
                theNode = node
                break
            if node.totalCost == float('inf'):
                continue
            for arc in node.outboundArcs:
                totalCost = node.totalCost + (arc.toNode.eventTime.getTimeMMM() - node.eventTime.getTimeMMM())
                if totalCost < arc.toNode.totalCost:
                    arc.toNode.totalCost = totalCost
                    arc.toNode.predecessorNode = node
        if theNode == None:
            return path # no path could be found
        while theNode.predecessorNode != None:
            for arc in theNode.predecessorNode.outboundArcs:
                if arc.toNode.nodeId == theNode.nodeId:
                    path.append(arc)
                    break
            theNode = theNode.predecessorNode
        rlist = []
        for p in reversed(path):
            rlist.append(p)
        return rlist

class TripPlanMove:
    def __init__(self, trainId, dwellTime, fromStation, toStation, startTime, endTime):
        self.trainId = trainId
        self.dwellTime = dwellTime
        self.fromStation = fromStation
        self.toStation = toStation
        self.startTime = startTime
        self.endTime = endTime
    def getTransitTimeMMM(self):
        return self.endTime.getTimeMMM() - self.startTime.getTimeMMM()
        
class TripPlan:
    def __init__(self, shortestPath, request):
        self.request = request
        self.moves = []
        arcs = shortestPath.findPath(request.origStation, request.departTime, request.destStation)
        if len(arcs) == 0:
            return # nothing else to initialize...
        prevTime = request.departTime.getTimeMMM()
        arcFirst = None
        arcLast = None
        for arc in arcs:
            if arc.trainId == None:
                continue # we are not interested in dwell arcs
            if arcFirst == None:
                arcFirst = arcLast = arc
                continue
            if arcFirst.trainId != arcLast.trainId:
                self.moves.append(TripPlanMove(arcFirst.trainId, arcFirst.fromNode.eventTime.getTimeMMM() - prevTime, arcFirst.fromNode.station, arcLast.toNode.station, arcFirst.fromNode.eventTime, arcLast.toNode.eventTime))
                prevTime = arcLast.toNode.eventTime.getTimeMMM()
                arcFirst = arc
            arcLast = arc
        self.moves.append(TripPlanMove(arcFirst.trainId, arcFirst.fromNode.eventTime.getTimeMMM() - prevTime, arcFirst.fromNode.station, arcLast.toNode.station, arcFirst.fromNode.eventTime, arcLast.toNode.eventTime))
    def __str__(self):
        r = list()
        i = 0
        if len(self.moves) == 0:
            r.append('{self.request.passengerId},1,,,,,,,,,,')
        for move in self.moves:
            startDDD = move.startTime.getTimeDDD()
            startHHMM = move.startTime.getTimeHHMM()
            endDDD = move.endTime.getTimeDDD()
            endHHMM = move.endTime.getTimeHHMM()
            transitTime = move.getTransitTimeMMM()
            r.append('{self.request.passengerId},{i},{move.trainId},{move.fromStation.stationNum},{move.toStation.stationNum},{startDDD},{startHHMM},{endDDD},{endHHMM},{transitTime},{move.dwellTime}'.format(self=self,i=i,move=move,startDDD=startDDD,startHHMM=startHHMM,endDDD=endDDD,endHHMM=endHHMM,transitTime=transitTime))
            i += 1
        r.append('') # adds newline when joined below
        return "\n".join(r)

class TripPlans:
    def __init__(self, trains, requests):
        self.trains = trains
        self.network = network.Network(self.trains)
        self.shortestPath = AcyclicShortestPath(self.network)
        self.tripPlans = []
        for request in requests:
            self.tripPlans.append(TripPlan(self.shortestPath, request))
    def dumpToFile(self, fileName):
        file = open(fileName, 'w')
        file.write('Psg ID,Seq,Train ID,From Station Num,To Station Num,Train Dept Day,Train Dept Time,')
        file.write('Train Arrival Day,Train Arrival Time,Transit Time,Dwell Time\n')
        for tripPlan in self.tripPlans:
            file.write(str(tripPlan))
        file.close()