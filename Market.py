import Graph
import SocialSphere
import random

class Investor(object):

    numShares = 0
    inMarket = False
    node = Graph.Vertex('')
    marketHistory = []
    lastChange = 10000
    numTimesLeft = 0

    def __init__(self, numShares, node):
        self.numShares = numShares
        self.node = node

    def enterMarket(self):
        self.inMarket = True
        self.marketHistory.append(True)
        self.lastChange = 0

    def leaveMarket(self):
        self.inMarket = False
        self.marketHistory.append(False)
        self.lastChange = 0
        self.numTimesLeft = self.numTimesLeft + 1

    def stayInMarket(self):
        self.marketHistory.append(True)
        self.lastChange = self.lastChange + 1

    def stayOutsideMarket(self):
        self.marketHistory.append(False)
        self.lastChange = self.lastChange + 1

    def getNumShares(self):
        return self.numShares

    def isInMarket(self):
        return self.inMarket

    def getMarketHistory(self):
        return self.marketHistory

    def changedStanceRecently(self):
        return self.lastChange < 15

    def recentlyLeftMarket(self):
        return ((self.lastChange <=20) and (not self.inMarket))

    def recentlyJoinedMarket(self):
        return ((self.lastChange <=20) and (self.inMarket))

    """
    This method calculates a probability for the investor (not currently in the market) to enter the market
    Probability depends on the following factors:"
    -Other investors connected to this investor in the social sphere: whether or not they are in the market; how many connections they have"
    -How this investor's connections have changed their stance in recent timesteps
    -How the market has changed from the first timestep to the current timestep
    -Whether the number of shares purchased is approaching the limit of the market
    -Whether the investor has previously left the market
    """
    def probToJoin(self, sphere, investors, marketValues, curTime, market, largestNumConnections, averageNumConnections, herdBehaviour):

        #Start off with a random probability
        prob = random.uniform(0.0, 0.2)

        #First look at all of the investor's connections in the social sphere
        connections = sphere.g[self.node]
        if(herdBehaviour == False):
            connections = []

        for connection in connections:

            #For each connection, look at the number of their connections as a 'strength'
            connectionStrength = len(sphere.g[connection])

            #Look at whether or not the connection is currently in the market
            currentlyInMarket = investors[connection.getLabel()].isInMarket()

            #Change probability depending on connection's current stance
            if(currentlyInMarket):
                #Move probability to join towards 1, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.3,0.6))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.3,0.6)))
                prob = prob + float(a * float(1.0-prob))
            else:
                #Move probability to join towards 0, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.35,0.7))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.35,0.7)))
                prob = prob - float(a * prob)
                pass

            #Determine whether or not the connection has left the market in the past (unless we're only in the first timestep)
            recentlyLeftMarket = investors[connection.getLabel()].recentlyLeftMarket()
            recentlyJoinedMarket = investors[connection.getLabel()].recentlyJoinedMarket()
            if(recentlyLeftMarket):
                #Move probability to join towards 0, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.4,0.8))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.4,0.8)))
                prob = prob - float(a * prob)
            elif(recentlyJoinedMarket):
                #Move probability to join towards 1, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.4,0.83))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.4,0.83)))
                prob = prob + float(a * float(1.0 - prob))


        #Now, after looking at all connections, look at whether or not the number of shares purchased is approaching the market's limit
        if(float(marketValues[curTime-1]) >= float(market.limit * random.uniform(0.75,0.95))):
            #Move probability to join towards 0, taking into account how close to the limit market is
            a = float(float(market.totalShares / market.limit) * random.uniform(0.3,0.7))
            prob = prob - float(a * prob)

        #Now, after looking at all connections and the limit, look at how the market has changed since the start
        recentChange = marketValues[curTime-1] - marketValues[0]

        #Now change probability depending on recentChange (if it's large and negative, probability should move towards 0, if it's large and positive, it should move towards 1)
        if(recentChange > 0):
            #Move probability to join towards 1, taking into account extent of change
            a = float(float(abs(recentChange) / market.limit) * random.uniform(0.25,0.65))
            prob = prob - float(a * float(1.0 - prob))

        elif(recentChange < 0):
            #Move proability to join towards 0, taking into account extent of change
            a = float(float(abs(recentChange) / market.limit) * random.uniform(0.25,0.65))
            prob = prob - float(a * prob)

        #Finally, look at whether or not the investor has left in the past. If they have, it should drastically reduce the probability of joining again
        a = 0.0
        if(self.numTimesLeft > 0):
            #a = float(0.85 + float(0.15 * float(self.numTimesLeft/3)))
            a = random.uniform(0.4,0.75)
        prob = prob - float(a * prob)

        #return prob
        return prob


    """
    This method calculates a probability for the investor (currently in the market) to leave the market
    Probability depends on the following factors:"
    -Other investors connected to this investor in the social sphere: whether or not they are in the market; how many connections they have"
    -How this investor's connections have changed their stance in recent timesteps
    -How the market has changed from the first timestep to the current timestep
    -Whether the number of shares purchased is approaching the limit of the market
    """
    def probToLeave(self, sphere, investors, marketValues, curTime, market, largestNumConnections, averageNumConnections, herdBehaviour):

        #Start off with a random probability
        prob = random.uniform(0.0, 0.3)

        #First look at all of the investor's connections in the social sphere
        connections = sphere.g[self.node]
        if(herdBehaviour == False):
            connections = []

        for connection in connections:

            #For each connection, look at the number of their connections as a 'strength'
            connectionStrength = len(sphere.g[connection])

            #Look at whether or not the connection is currently in the market
            currentlyInMarket = investors[connection.getLabel()].isInMarket()

            #Change probability depending on connection's current stance
            if(currentlyInMarket):
                #Move probability to leave towards 0, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.3,0.65))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.3,0.65)))
                prob = prob - float(a * prob)
            else:
                #Move probability to leave towards 1, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.45,0.9))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.45,0.9)))
                prob = prob + float(a *float(1.0 - prob))

            #Look at whether or not the connection has recently left the market
            recentlyLeftMarket = investors[connection.getLabel()].recentlyLeftMarket()
            recentlyJoinedMarket = investors[connection.getLabel()].recentlyJoinedMarket()
            if(recentlyLeftMarket):
                #Move probability to leave towards 1, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.55,0.99))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.55,0.99)))
                prob = prob + float(a * float(1.0-prob))
            elif(recentlyJoinedMarket):
                #Move probability to leave towards 0, taking into account connection strength
                #a = float(float(connectionStrength/largestNumConnections) * random.uniform(0.35,0.8))
                a = (random.uniform(0.7,0.9)) if (connectionStrength >= (averageNumConnections + 15)) else (float(float(connectionStrength/largestNumConnections) * random.uniform(0.35,0.8)))
                prob = prob - float(a * prob)


        #Now, after looking at all connections, look at whether or not the number of shares purchased is approaching the market's limit
        if(float(marketValues[curTime-1]) >= float(market.limit * random.uniform(0.75,0.95))):
            #Move probability to leave towards 1, taking into account how close to the limit market is
            a = float(float(market.totalShares / market.limit) * random.uniform(0.3,0.8))
            prob = prob + float(a * float(1.0-prob))

        #Now, after looking at all connections and the limit, look at how the market has changed since the first timestep
        recentChange = marketValues[curTime-1] - marketValues[0]

        #Now change probability depending on recentChange (if it's large and negative, probability should move towards 1, if it's large and positive, it should move towards 0)
        if(recentChange > 0):
            #Move probability to leave towards 0, taking into account extent of change
            a = float(float(abs(recentChange) / market.limit) * random.uniform(0.3,0.7))
            prob = prob - float(a * prob)

        elif(recentChange < 0):
            #Move proability to leave towards 1, taking into account extent of change
            a = float(float(abs(recentChange) / market.limit)) * random.uniform(0.3,0.7)
            prob = prob + float(a * float(1.0-prob))

        #return prob
        return prob


class Market(object):

    totalShares = 0
    limit = 0

    def __init__(self, newLim):
        self.totalShares = 0
        self.limit = newLim

    def addInvestor(self, i):
        "Adds an investor to the stock market (when they decide to purchase shares)"
        self.totalShares = self.totalShares + (i.getNumShares())

    def removeInvestor(self, i):
        "Removes an investor from the stock market (when they decide to sell their shares)"
        self.totalShares = self.totalShares - (i.getNumShares())

    def canJoin(self, i):
        "Returns whether or not the specified investor can join the market (True/False return value)"
        "Investor can join if there are enough shares left (i.e. difference between limit and totalShares) for that investor"
        remainingShares = self.limit - self.totalShares
        if(remainingShares >= i.getNumShares()):
            return True
        else:
            return False
