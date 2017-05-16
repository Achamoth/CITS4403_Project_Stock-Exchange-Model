class Investor(object):

    numShares = 0
    inMarket = 0

    def __init__(self, numShares, startingPos):
        self.numShares = numShares
        self.inMarket = startingPos

    def enterMarket(self):
        inMarket = true

    def leaveMarket(self):
        inMarket = false

    def getNumShares(self):
        return self.numShares

    def isInMarket(self):
        return self.inMarket


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
