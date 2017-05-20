import Market
import SocialSphere
import random
import csv

def setUpInvestors(sphere):
    """
    Given a social sphere, this function sets up a dictionary of investors, and returns it
    Each investor is given a number of shares (that they can invest), and a starting position (whether or not they start off in the stock market)
    """

    "Set up empty dictionary"
    investors = {}
    "Start by getting all nodes from social sphere (each node represents one investor)"
    nodes = sphere.g.vertices()
    for node in nodes:
        "Probabilistically decide on number of shares for investor, depending on that investor's number of social links"
        numShares = random.random() * 10 * (len(sphere.g[node])+1) #TODO: Can experiment with how I decide this parameter
        "Set up investor"
        investors[node.getLabel()] = Market.Investor(numShares, node)

    "Return dictionary of investors"
    return investors


def setUpMarket(investors):
    """
    Given a dictionary of investors, sets up the stock market model, and returns it
    The market is given a number of purchased shares (representing how many people are invested in it, and how many shares they've purchased)
    """

    "Work out how many stocks all investors together can by"
    totalSharesPurchasable = 0
    for key in investors:
        totalSharesPurchasable = totalSharesPurchasable + investors[key].getNumShares()

    "Set up empty stock market, with stock limit at a fraction of total stocks purchasable by investors"
    market = Market.Market(float(100000000000000.0) * totalSharesPurchasable) #TODO: Can experiment with this parameter

    "Loop over all investors, and probabilistically determine their starting position"
    for key in investors:
        curInvestor = investors[key]
        "Randomly decide whether or not the investor is in the stock market"
        startingPos = (random.random() <= 0.3) #TODO: Can experiment with this parameter
        if(startingPos == False):
            curInvestor.stayOutsideMarket()
        "If they're in the market, add them to the market model, if there are enough shares available"
        if(startingPos == True):
            "Check if there are enough shares"
            if(market.canJoin(curInvestor)):
                "Add them to the market"
                market.addInvestor(curInvestor)
                curInvestor.enterMarket()
            else:
                "Investor can't join market"
                curInvestor.stayOutsideMarket()

    "Return the market model"
    return market


def tick(market, investors, sphere, marketValues, curTime, largestNumConnections):
    """
    Performs a 'tick' operation on the simulation, moving it forward by one timestep
    For each investor, calculates a probability for them to join/leave the market based on certain factors, and then executes that probabily, and changes market accordingly
    """

    "Loop  over all investors"
    numJoined = 0
    numLeft = 0
    for key in investors:
        investor = investors[key]
        "For current investor, check whether they're inside/outside the market"
        if(investor.isInMarket()):
            "Calculate a probability for them to leave"
            probToLeave = investor.probToLeave(sphere, investors, marketValues, curTime, market, largestNumConnections)
            "Determine whether or not they leave"
            if(random.random() <= probToLeave and numLeft < 3000/4):
                numLeft = numLeft + 1
                market.removeInvestor(investor)
                investor.leaveMarket()
            else:
                investor.stayInMarket()
        else:
            "Calculate a probability for them to join"
            probToJoin = investor.probToJoin(sphere, investors, marketValues, curTime, market, largestNumConnections)
            "Determine whether or not they join"
            if(random.random() <= probToJoin and market.canJoin(investor) and numJoined < 3000/4):
                market.addInvestor(investor)
                investor.enterMarket()
                numJoined = numJoined + 1
            else:
                investor.stayOutsideMarket()
    print(str(numJoined) + ' ' + str(numLeft))

def getLargestNumConnections(sphere):
    largest = 0
    nodes = sphere.g.vertices()
    for key in nodes:
        numConnections = len(sphere.g[key])
        largest = max(numConnections, largest)
    return largest


def main():
    "Set up social sphere"
    s = SocialSphere.SocialSphere(3000) #TODO: Can experiment with this parameter

    "Set up dictionary of investors"
    investors = setUpInvestors(s)

    "Set up stock market"
    market = setUpMarket(investors)

    "Get largest number of connections any one investor has"
    largestNumConnections = getLargestNumConnections(s)

    "Run simulation over multiple time steps, and plot results as they're generated"
    marketValues = []
    marketValues.append(market.totalShares)
    for i in range(1,150):
        tick(market, investors, s, marketValues, i, largestNumConnections)
        marketValues.append(market.totalShares)

    "Print all results to a csv file"
    with open('results.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(marketValues)

main()
