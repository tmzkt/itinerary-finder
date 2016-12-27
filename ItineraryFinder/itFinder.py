import busLogic
bl = busLogic.BusLogic()
bl.outputNetwork('nodes.csv', 'arcs.csv')
bl.outputTripPlans('tripplan.csv')
