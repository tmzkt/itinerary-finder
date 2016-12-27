import basicData

class Node:
    def __init__(self, nodeId, station, eventTime):
        self.nodeId = nodeId
        self.station = station
        self.eventTime = eventTime
        self.outboundArcs = []
        self.predecessorNode = None
        self.totalCost = 0
    def __str__(self):
        return '{self.nodeId},{self.station.stationNum},{self.eventTime.timeHHHMM}\n'.format(self=self)

class Arc:
    def __init__(self, arcId, fromNode, toNode, trainId):
        self.arcId = arcId
        self.fromNode = fromNode
        self.toNode = toNode
        self.trainId = trainId
    def getTransitTime(self):
        return self.toNode.eventTime.getTimeMMM() - self.fromNode.eventTime.getTimeMMM()
    def getType(self):
        raise NotImplementedError("getType function not implemented")
    def __str__(self):
        raise NotImplementedError("__str__ function not implemented")
        
class TrainArc(Arc):
    def __init__(self, arcId, fromNode, toNode, trainId):
        Arc.__init__(self, arcId, fromNode, toNode, trainId)
    def getType(self):
        return 'TRAIN'
    def __str__(self):
        return '{self.arcId},TRAIN,{self.fromNode.nodeId},{self.toNode.nodeId},{self.trainId}\n'.format(self=self)

class DwellArc(Arc):
    def __init__(self, arcId, fromNode, toNode):
        Arc.__init__(self, arcId, fromNode, toNode, None)
    def getType(self):
        return 'DWELL'
    def __str__(self):
        return '{self.arcId},DWELL,{self.fromNode.nodeId},{self.toNode.nodeId},\n'.format(self=self)

class Network:
    def __init__(self, trains):
        self.nodes = []
        self.arcs = []
        prevNode = None
        definedNodes = {}
        for day in range(21):
            for train in trains:
                if not train.daysOperated[day % 14]:
                    continue
                for trainRoute in train.trainRoutes:
                    arrivalNode = None
                    if trainRoute.arrivalTime != None:
                        arrivalNode = self._createNode(definedNodes, trainRoute.station, trainRoute.arrivalTime, day)
                        self._createArc(prevNode, arrivalNode, trainRoute)
                    departureNode = None
                    if trainRoute.departureTime != None and (arrivalNode == None or trainRoute.departureTime.timeHHHMM != trainRoute.arrivalTime.timeHHHMM):
                        departureNode = self._createNode(definedNodes, trainRoute.station, trainRoute.departureTime, day)
                    prevNode = departureNode if departureNode != None else arrivalNode
        self.nodes = sorted(self.nodes, key = lambda node: node.eventTime.timeHHHMM)
        self.nodes = sorted(self.nodes, key = lambda node: node.station.stationNum)
        prevNode = None
        for node in self.nodes:
            if prevNode != None and node.station.stationNum == prevNode.station.stationNum:
                self._createArc(prevNode, node, None)
            prevNode = node
        self.nodes = sorted(self.nodes, key = lambda node: node.station.stationNum)
        self.nodes = sorted(self.nodes, key = lambda node: node.eventTime.timeHHHMM)
    def _createNode(self, definedNodes, station, eventTime, daysPassed):
        t = basicData.EventTime(eventTime.timeHHHMM + (daysPassed * 24 * 100)) # create new event time with the hours passed added
        node = None
        if not (station.stationNum, t.timeHHHMM) in definedNodes:
            node = Node(len(self.nodes), station, t)
            definedNodes[(node.station.stationNum, node.eventTime.timeHHHMM)] = node
            self.nodes.append(node)
        else:
            node = definedNodes[(station.stationNum, t.timeHHHMM)]
        return node
    def _createArc(self, fromNode, toNode, trainRoute):
        arc = None
        if fromNode.station.stationNum == toNode.station.stationNum:
            arc = DwellArc(len(self.arcs), fromNode, toNode)
        else:
            arc = TrainArc(len(self.arcs), fromNode, toNode, trainRoute.trainId)
        self.arcs.append(arc)
        fromNode.outboundArcs.append(arc)
        return arc
    def dumpToFiles(self, nodesFileName, arcsFileName):
        nodesFile = open(nodesFileName, 'w')
        nodesFile.write('Node ID,Station ID,Event Time HHHMM\n')
        for node in self.nodes:
            nodesFile.write(str(node))
        nodesFile.close()
        arcsFile = open(arcsFileName, 'w')
        arcsFile.write('Arc ID,Arc Type,From Node ID,To Node ID,Transit Time,Train ID\n')
        for arc in self.arcs:
            arcsFile.write(str(arc))
        arcsFile.close()
        