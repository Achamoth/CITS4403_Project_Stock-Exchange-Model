import Market
import SocialSphere
import random

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
        numShares = random.random() * (len(sphere.g[node])+1) "TODO: Can experiment with how I decide this parameter"
        "Randomly decide whether or not the investor is in the stock market (50/50 chance)"
        startingPos = (random.random() <= 0.25) "TODO: Can experiment with this parameter"
        "Set up investor"
        investors[node.getLabel()] = Market.Investor(numShares, startingPos)

    "Return dictionary of investors"
    return investors


def setUpMarket(investors):
    """
    Given a dictionary of investors, sets up the stock market model, and returns it
    The market is given a number of purchased shares (representing how many people are invested in it, and how many shares they've purchased)
    """

    "Set up empty stock market"
    market = Market.Market()

    "Loop over all investors and check their starting position"
    for key in investors:
        curInvestor = investors[key]
        if(curInvestor.isInMarket()):
            "Add them to the market"
            market.addInvestor(curInvestor)

    "Return the market model"
    return market


def main():
    "Set up social sphere"
    s = SocialSphere.SocialSphere(1000) "TODO: Can experiment with this parameter"

    "Set up dictionary of investors"
    investors = setUpInvestors(s)

    "Set up stock market"
    market = setUpMarket(investors)

main()
