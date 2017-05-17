import SocialSphere
import random

class Investor(object):

    numShares = 0
    inMarket = 0
    node = Vertex('')
    marketHistory = []

    def __init__(self, numShares, startingPos, node):
        self.numShares = numShares
        self.inMarket = startingPos
        self.node = node
        self.marketHistory.add(startingPos)

    def enterMarket(self):
        self.inMarket = true
        self.marketHistory.add(true)

    def leaveMarket(self):
        self.inMarket = false
        self.marketHistory.add(false)

    def getNumShares(self):
        return self.numShares

    def isInMarket(self):
        return self.inMarket

    def getMarketHistory(self):
        return self.marketHistory

    """
    Calculates a probability for the investor (not currently in the market) to enter the market
    Probability depends on the following factors:"
    -Other investors connected to this investor in the social sphere: whether or not they are in the market; how many connections they have"
    -How this investor's connections have changed their stance in the last timestep
    -How the market has changed from the last timestep to the current timestep
    TODO: Can consider adding the following factors:
    -Whether or not this investor has been in the market before, and if so, how many times they've left (signs of instability?)
    -Can consider looking at a recent history of timesteps, rather than just the last timestep
    """
    def probToJoin(sphere, investors, marketValues, curTime, market):

        prob = 0

        "First look at all of the investor's connections in the social sphere"
        connections = sphere.g[self.node]
        for connection in connections:
            "For each connection, look at the number of their connections as a 'strength' "
            connectionStrength = len(sphere.g[connection])
            "Look at whether or not the connection is currently in the market"
            currentlyInMarket = investors[connection.getLabel()].isInMarket()
            "Look at whether or not the connection has recently left the market (unless we're only in the first timestep)"
            if(curTime > 1):
                connectionMarketHistory = investors[connection.getLabel()].getMarketHistory()
                recentlyLeftMarket = (connectionMarketHistory[curTime-2]==true && connectionMarketHistory[curTime-1]==false)
                recentlyJoinedMarket = (connectionMarketHistory[curTime-2]==false && connectionMarketHistory[curTime-1]==true)

            "Now, look at factors, and move probability closer to 0 or 1, depending on connection's stance and recent history"
            if(curTime <= 1):
                "Will need to calculate probability slightly differently, as I can't use the recent history of the connection"
                "TODO: Move probability towards 0 or 1"
            else:
                "Look at all factors to determine whether probability moves closer to 0 or 1"
                "TODO: Move probability towards 0 or 1"


        "If we're in the first timestep, we can't look at the market's recent change history. Just return the currently calculated probability"
        if(curTime <= 1):
            return prob

        "Now, after looking at all connections, look at how the market has changed recently"
        recentChange = market.totalShares - marketValues[curTime-1]
        "Now change probability depending on recentChange (if it's large and negative, probability should move towards 1, if it's large and positive, it should move towards 0)"
        "TODO: Move probability towards 0 or 1"

        return prob


    """
    Calculates a probability for the investor (currently in the market) to leave the market
    Probability depends on the following factors:"
    -Other investors connected to this investor in the social sphere: whether or not they are in the market; how many connections they have"
    -How this investor's connections have changed their stance in the last timestep
    -How the market has changed from the last timestep to the current timestep
    TODO: Can consider adding the following factors:
    -Whether or not this investor has been in the market before, and if so, how many times they've left (signs of instability?)
    -Can consider looking at a recent history of timesteps, rather than just the last timestep
    """
    def probToLeave(sphere, marketValues, curTime, market):

        prob = 0

        "First look at all of the investor's connections in the social sphere"
        connections = sphere.g[self.node]
        for connection in connections:
            "For each connection, look at the number of their connections as a 'strength' "
            connectionStrength = len(sphere.g[connection])
            "Look at whether or not the connection is currently in the market"
            currentlyInMarket = investors[connection.getLabel()].isInMarket()
            "Look at whether or not the connection has recently left the market (unless we're only in the first timestep)"
            if(curTime > 1):
                connectionMarketHistory = investors[connection.getLabel()].getMarketHistory()
                recentlyLeftMarket = (connectionMarketHistory[curTime-2]==true && connectionMarketHistory[curTime-1]==false)
                recentlyJoinedMarket = (connectionMarketHistory[curTime-2]==false && connectionMarketHistory[curTime-1]==true)

            "Now, look at factors, and move probability closer to 0 or 1, depending on connection's stance and recent history"
            if(curTime <= 1):
                "Will need to calculate probability slightly differently, as I can't use the recent history of the connection"
                "TODO: Move probability towards 0 or 1"
            else:
                "Look at all factors to determine whether probability moves closer to 0 or 1"
                "TODO: Move probability towards 0 or 1"


        "If we're in the first timestep, we can't look at the market's recent change history. Just return the currently calculated probability"
        if(curTime <= 1):
            return prob

        "Now, after looking at all connections, look at how the market has changed recently"
        recentChange = market.totalShares - marketValues[curTime-1]
        "Now change probability depending on recentChange (if it's large and negative, probability should move towards 1, if it's large and positive, it should move towards 0)"
        "TODO: Move probability towards 0 or 1"

        return prob



class Market(object):

    totalShares = 0

    def __init__(self):
        self.totalShares = 0

    def addInvestor(self, i):
        "Adds an investor to the stock market (when they decide to purchase shares)"
        self.totalShares = self.totalShares + (i.getNumShares())

    def removeInvestor(self, i):
        "Removes an investor from the stock market (when they decide to sell their shares)"
        self.totalShares = self.totalShares - (i.getNumShares())
