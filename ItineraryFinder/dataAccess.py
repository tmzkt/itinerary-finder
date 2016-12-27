import pyodbc
import basicData

class DataAccess:
    def __init__(self):
        self._cnxn = pyodbc.connect('''DRIVER={Microsoft Access Driver (*.mdb)};DBQ=C:\Trains.mdb''')
        self._cursor = self._cnxn.cursor()
        self._stations = None
    def _loadStations(self):
        if self._stations != None:
            return
        self._cursor.execute("select * from STATION_MASTER")
        self._stations = {}
        for row in self._cursor:
            self._stations[row.STATION_NUM] = basicData.Station(row.STATION_NUM, row.STATION_NAME)
    def loadTrains(self):
        self._cursor.execute("select * from TRAIN order by TRAIN_ID")
        trains = []
        for row in self._cursor:
            daysOperated = [row.OPERATES_DAY_1,
                            row.OPERATES_DAY_2,
                            row.OPERATES_DAY_3,
                            row.OPERATES_DAY_4,
                            row.OPERATES_DAY_5,
                            row.OPERATES_DAY_6,
                            row.OPERATES_DAY_7,
                            row.OPERATES_DAY_8,
                            row.OPERATES_DAY_9,
                            row.OPERATES_DAY_10,
                            row.OPERATES_DAY_11,
                            row.OPERATES_DAY_12,
                            row.OPERATES_DAY_13,
                            row.OPERATES_DAY_14]
            trains.append(basicData.Train(row.TRAIN_ID, row.TRAIN_CATEGORY, daysOperated))
        return trains
    def loadTrainRoutes(self):
        self._loadStations()
        self._cursor.execute("select * from TRAIN_ROUTE order by TRAIN_ID, ROUTE_POINT_SEQ")
        trainRoutes = []
        for row in self._cursor:
            trainRoutes.append(basicData.TrainRoute(row.TRAIN_ID,
                                                    self._stations[row.STATION_NUM],
                                                    basicData.EventTime(row.ARRIVE_TIME_HHHMM) if row.ARRIVE_TIME_HHHMM != -1 else None,
                                                    basicData.EventTime(row.DEPART_TIME_HHHMM) if row.DEPART_TIME_HHHMM != -1 else None))
        return trainRoutes
    def loadPassengerScheduleRequests(self):
        self._loadStations()
        self._cursor.execute("select * from PASSENGER_OD_TIME")
        requests = []
        for row in self._cursor:
            requests.append(basicData.PassengerScheduleRequest(row.PSG_ID, self._stations[row.ORIG_STATION_NUM], self._stations[row.DEST_STATION_NUM],basicData.EventTime((row.PASSENGER_DEPT_DAY - 1) * 2400 + row.PASSENGER_DEPT_HHMM)))
        return requests
    def saveNetwork(self, network):
        # Empty node and arc tables
        self._cursor.execute("delete from ARC")
        self._cursor.execute("delete from NODE")
        self._cnxn.commit()
        # Insert data into tables
        nodeRows = []
        for node in network.nodes:
            nodeRows.append([node.nodeId, node.station.stationNum, node.eventTime.timeHHHMM])
        self._cursor.executemany("insert into NODE values (?, ?, ?)", nodeRows)
        arcRows = []
        for arc in network.arcs:
            arcRows.append([arc.arcId, arc.arcType, arc.FromNode.nodeId, arc.ToNode.nodeId, arc.transitTime, arc.trainId])
        self._cursor.executemany("insert into ARC values (?, ?, ?, ?, ?, ?)", arcRows)
        self._cnxn.commit()
    def saveTripPlans(self, tripPlans):
        # Empty trip plan table
        self._cursor.execute("delete from TRIP_PLAN")
        self._cnxn.commit()
        # Insert data into tables
        tripPlanRows = []
        for tripPlan in tripPlans.tripPlans:
            if len(tripPlan.moves) == 0:
                tripPlanRows.append([tripPlan.request.passengerId, 1])
                continue
            seq = 1
            for tripPlanMove in tripPlan.moves:
                tripPlanRows.append([tripPlan.request.passengerId, seq, tripPlanMove.trainId, tripPlanMove.fromStation.stationNum, tripPlanMove.fromStation.stationName, tripPlanMove.toStation.stationNum, tripPlanMove.toStation.stationName, tripPlanMove.startTime.getTimeDDD(),tripPlanMove.startTime.getTimeHHMM(), tripPlanMove.endTime.getTimeDDD(), tripPlanMove.endTime.getTimeHHMM(), tripPlanMove.getTransitTimeMMM(), tripPlanMove.dwellTime])
                seq += 1
        self._cursor.executemany("insert into TRIP_PLAN values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tripPlanRows)