import Graph
import SocialSphere
import random

class Investor(object):

    numShares = 0
    inMarket = False
    node = Graph.Vertex('')
    marketHistory = []

    def __init__(self, numShares, node):
        self.numShares = numShares
        self.node = node

    def enterMarket(self):
        self.inMarket = True
        self.marketHistory.append(True)

    def leaveMarket(self):
        self.inMarket = False
        self.marketHistory.append(False)

    def stayInMarket(self):
        self.marketHistory.append(True)

    def stayOutsideMarket(self):
        self.marketHistory.append(False)

    def getNumShares(self):
        return self.numShares

    def isInMarket(self):
        return self.inMarket

    def getMarketHistory(self):
        return self.marketHistory

    """
    This method calculates a probability for the investor (not currently in the market) to enter the market
    Probability depends on the following factors:"
    -Other investors connected to this investor in the social sphere: whether or not they are in the market; how many connections they have"
    -How this investor's connections have changed their stance in the last timestep
    -How the market has changed from the last timestep to the current timestep
    -Whether the number of shares purchased is approaching the limit of the market (within 80%)
    TODO: Can consider adding the following factors:
    -Whether or not this investor has been in the market before, and if so, how many times they've left (signs of instability?)
    -Can consider looking at a recent history of timesteps, rather than just the last timestep
    """
    def probToJoin(self, sphere, investors, marketValues, curTime, market, largestNumConnections):

        #Start off with a random probability
        prob = random.random()

        #First look at all of the investor's connections in the social sphere
        connections = sphere.g[self.node]

        for connection in connections:

            #For each connection, look at the number of their connections as a 'strength'
            connectionStrength = len(sphere.g[connection])

            #Look at whether or not the connection is currently in the market
            currentlyInMarket = investors[connection.getLabel()].isInMarket()

            #Change probability depending on connection's current stance
            if(currentlyInMarket):
                #Move probability to join towards 1, taking into account connection strength
                #TODO: Calculate a between 0 and 1. a increases with connection strength
                a = max(0.5, float(connectionStrength/largestNumConnections))
                prob = prob + float(a * float(1.0-prob))
            else:
                #Move probability to join towards 0, taking into account connection strength
                #TODO: Calculate a between 0 and 1. a increases with connection strength
                a = max(0.5, float(connectionStrength/largestNumConnections))
                prob = prob - float(a * prob)

            #Determine whether or not the connection has recently left the market (unless we're only in the first timestep)
            if(curTime > 1):
                connectionMarketHistory = investors[connection.getLabel()].getMarketHistory()
                recentlyLeftMarket = (connectionMarketHistory[curTime-2]==True and connectionMarketHistory[curTime-1]==False)
                recentlyJoinedMarket = (connectionMarketHistory[curTime-2]==False and connectionMarketHistory[curTime-1]==True)
                if(recentlyLeftMarket):
                    #Move probability to join towards 0, taking into account connection strength
                    #TODO: Calculate a between 0 and 1. a increases with connection strength
                    a = max(0.6, float(connectionStrength/largestNumConnections))
                    prob = prob - float(a * prob)
                elif(recentlyJoinedMarket):
                    #Move probability to join towards 1, taking into account connection strength
                    #TODO: Calculate a between 0 and 1. a increases with connection strength
                    a = max(0.6, float(connectionStrength/largestNumConnections))
                    prob = prob + float(a * float(1.0 - prob))


        #Now, after looking at all connections, look at whether or not the number of shares purchased is approaching the market's limit
        if(float(market.totalShares) >= float(market.limit * 0.75)): #TODO: Can experiment with this parameter
            #Move probability to join towards 0, taking into account how close to the limit market is
            #TODO: Calculate a between 0 and 1. a increases as market approaches limit
            a = max(0.7, float(market.totalShares / market.limit))
            prob = prob - float(a * prob)

        #If we're in the first timestep, we can't look at the market's recent change history. Just return the currently calculated probability
        if(curTime <= 1):
            return prob

        #Now, after looking at all connections and the limit, look at how the market has changed recently
        recentChange = marketValues[curTime-1] - marketValues[curTime-2]

        #Now change probability depending on recentChange (if it's large and negative, probability should move towards 0, if it's large and positive, it should move towards 1)
        if(recentChange > 0):
            #Move probability to join towards 1, taking into account extent of change
            #TODO: Calculate a between 0 and 1. The larger the change, the larger a
            a = float(abs(recentChange) / market.limit)
            prob = prob - float(a * float(1.0 - prob))

        elif(recentChange < 0):
            #Move proability to join towards 0, taking into account extent of change
            #TODO: Calculate a between 0 and 1. The larger the change, the larger a
            a = float(abs(recentChange) / market.limit)
            prob = prob - float(a * prob)

        return prob


    """
    This method calculates a probability for the investor (currently in the market) to leave the market
    Probability depends on the following factors:"
    -Other investors connected to this investor in the social sphere: whether or not they are in the market; how many connections they have"
    -How this investor's connections have changed their stance in the last timestep
    -How the market has changed from the last timestep to the current timestep
    -Whether the number of shares purchased is approaching the limit of the market (within 80%)
    TODO: Can consider adding the following factors:
    -Whether or not this investor has been in the market before, and if so, how many times they've left (signs of instability?)
    -Can consider looking at a recent history of timesteps, rather than just the last timestep
    """
    def probToLeave(self, sphere, investors, marketValues, curTime, market, largestNumConnections):

        #Start off with a random probability
        prob = random.random()

        #First look at all of the investor's connections in the social sphere
        connections = sphere.g[self.node]

        for connection in connections:

            #For each connection, look at the number of their connections as a 'strength'
            connectionStrength = len(sphere.g[connection])

            #Look at whether or not the connection is currently in the market
            currentlyInMarket = investors[connection.getLabel()].isInMarket()

            #Change probability depending on connection's current stance
            if(currentlyInMarket):
                #Move probability to leave towards 0, taking into account connection strength
                #TODO: Calculate a. The larger connection strength is, the larger a should be (between 0 and 1)
                a = max(0.5, float(connectionStrength/largestNumConnections))
                prob = prob - float(a * prob)
            else:
                #Move probability to leave towards 1, taking into account connection strength
                #TODO: Calculate a. The larger connection strength is, the larger a should be (between 0 and 1)
                a = max(0.5, float(connectionStrength/largestNumConnections))
                prob = prob + float(a *float(1.0 - prob))

            #Look at whether or not the connection has recently left the market (unless we're only in the first timestep)
            if(curTime > 1):
                connectionMarketHistory = investors[connection.getLabel()].getMarketHistory()
                recentlyLeftMarket = (connectionMarketHistory[curTime-2]==True and connectionMarketHistory[curTime-1]==False)
                recentlyJoinedMarket = (connectionMarketHistory[curTime-2]==False and connectionMarketHistory[curTime-1]==True)
                if(recentlyLeftMarket):
                    #Move probability to leave towards 1, taking into account connection strength
                    #TODO: Calculate a between 0 and 1. Larger connection strength means larger a
                    a = max(0.6, float(connectionStrength/largestNumConnections))
                    prob = prob + float(a * float(1.0-prob))
                elif(recentlyJoinedMarket):
                    #Move probability to leave towards 0, taking into account connection strength
                    #TODO: Calculate a between 0 and 1. Larger connection strength means larger a
                    a = max(0.6, float(connectionStrength/largestNumConnections))
                    prob = prob - float(a * prob)


        #Now, after looking at all connections, look at whether or not the number of shares purchased is approaching the market's limit
        if(float(market.totalShares) >= float(market.limit * 0.75)): #TODO: Can experiment with this parameter
            #Move probability to leave towards 1, taking into account how close to the limit market is
            #TODO: Calculate a between 0 and 1. Closer to limit means larger a
            a = max(0.7, float(market.totalShares / market.limit))
            prob = prob + float(a * float(1.0-prob))

        #If we're in the first timestep, we can't look at the market's recent change history. Just return the currently calculated probability
        if(curTime <= 1):
            return prob

        #Now, after looking at all connections and the limit, look at how the market has changed recently
        recentChange = market.totalShares - marketValues[curTime-1]

        #Now change probability depending on recentChange (if it's large and negative, probability should move towards 1, if it's large and positive, it should move towards 0)
        if(recentChange > 0):
            #Move probability to leave towards 0, taking into account extent of change
            #TODO: Calculate a between 0 and 1. Larger change means larger a
            a = float(abs(recentChange) / market.limit)
            prob = prob - float(a * prob)

        elif(recentChange < 0):
            #Move proability to leave towards 1, taking into account extent of change
            #TODO: Calculate a between 0 and 1. Larger change means larger a
            a = float(abs(recentChange) / market.limit)
            prob = prob + float(a * float(1.0-prob))

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
