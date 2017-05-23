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


def setUpMarket(investors, probToStartInMarket):
    """
    Given a dictionary of investors, sets up the stock market model, and returns it
    The market is given a number of purchased shares (representing how many people are invested in it, and how many shares they've purchased)
    """

    "Work out how many stocks all investors together can by"
    totalSharesPurchasable = 0
    for key in investors:
        totalSharesPurchasable = totalSharesPurchasable + investors[key].getNumShares()

    "Set up empty stock market, with stock limit at a fraction of total stocks purchasable by investors"
    market = Market.Market(float(random.uniform(0.45, 0.85)) * totalSharesPurchasable)

    "Loop over all investors, and probabilistically determine their starting position"
    for key in investors:
        curInvestor = investors[key]
        "Randomly decide whether or not the investor is in the stock market"
        startingPos = (random.random() <= probToStartInMarket)
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


def tick(market, investors, sphere, marketValues, curTime, largestNumConnections, averageNumConnections, herdBehaviour):
    """
    Performs a 'tick' operation on the simulation, moving it forward by one timestep
    For each investor, calculates a probability for them to join/leave the market based on certain factors, and then executes that probabily, and changes market accordingly
    """

    "Loop  over all investors"
    marketSize = len(sphere.g)
    numJoined = 0
    numLeft = 0
    for key in investors:
        investor = investors[key]
        "For current investor, check whether they're inside/outside the market"
        if(investor.isInMarket()):
            "Calculate a probability for them to leave"
            probToLeave = investor.probToLeave(sphere, investors, marketValues, curTime, market, largestNumConnections, averageNumConnections, herdBehaviour)
            "Determine whether or not they leave (if the investor has joined recently, they can't leave yet)"
            if(random.random() <= probToLeave and (not investor.changedStanceRecently()) and numLeft <= marketSize/50):
                numLeft = numLeft + 1
                market.removeInvestor(investor)
                investor.leaveMarket()
                if(len(sphere.g[investor.node]) > averageNumConnections + 15):
                    print(str(len(sphere.g[investor.node]))) + ' left market at ' + str(curTime)
            else:
                investor.stayInMarket()
        else:
            "Calculate a probability for them to join"
            probToJoin = investor.probToJoin(sphere, investors, marketValues, curTime, market, largestNumConnections, averageNumConnections, herdBehaviour)
            "Determine whether or not they join (if the investor has left recently, they can't join yet)"
            if(random.random() <= probToJoin and market.canJoin(investor) and (not investor.changedStanceRecently()) and numJoined <= marketSize/50):
                market.addInvestor(investor)
                investor.enterMarket()
                numJoined = numJoined + 1
                if(len(sphere.g[investor.node]) >= averageNumConnections + 15):
                    print(str(len(sphere.g[investor.node]))) + ' joined market at ' + str(curTime)
            else:
                investor.stayOutsideMarket()
    #print(str(numJoined) + ' ' + str(numLeft))

def getLargestNumConnections(sphere):
    "Given a social sphere object, return the largest number of connections any node in the graph has (i.e. largest degree)"
    largest = 0
    nodes = sphere.g.vertices()
    for key in nodes:
        numConnections = len(sphere.g[key])
        largest = max(numConnections, largest)
    return largest

def getAverageNumConnections(sphere):
    "Given a social sphere object, return the average number of connections for a node in the social sphere's graph"
    total = 0
    nodes = sphere.g.vertices()
    for key in nodes:
        numConnections = len(sphere.g[key])
        total = total + numConnections
    return (total / len(nodes))

def readConfig(filename):
    "Given the filename of a config file, read all of the parameters in the file, and return them"
    parameters = {}
    fin = open(filename)
    #Read all lines in file
    for line in fin:
        #Remove leading and trailing whitespace, and trailing newline character
        line = line.strip()
        line = line.strip('\n')
        #If line is empty, or a comment, skip it
        if (not line or line[0] == '#'):
            continue
        #Split around '='  character, and strip tokens of leading and trailing whitespace
        tokens = line.split('=')
        tokens[0] = tokens[0].strip()
        tokens[1] = tokens[1].strip()
        #First token is name of parameter (second token is value)
        if(tokens[0] == 'model'):
            parameters['model'] = tokens[1]
        elif(tokens[0] == 'size'):
            parameters['size'] = int(tokens[1])
        elif(tokens[0] == 'timesteps'):
            parameters['timesteps'] = int(tokens[1])
        elif(tokens[0] == 'investor_start'):
            parameters['investor_start'] = float(tokens[1])
        elif(tokens[0] == 'herd'):
            parameters['herd'] = (tokens[1] == 'on')
        elif(tokens[0] == 'k'):
            parameters['k'] = int(tokens[1])
        elif(tokens[0] == 'rewire'):
            parameters['rewire'] = float(tokens[1])
    return parameters

def main():
    "Read all parameters from config file"
    params = readConfig('config.txt')

    "Set up social sphere"
    if(params['model'] == 'ba'):
        s = SocialSphere.SocialSphere(params['size'], params['model'])
    else:
        s = SocialSphere.SocialSphere(params['size'], params['model'], params['k'], params['rewire'])

    "Set up dictionary of investors"
    investors = setUpInvestors(s)

    "Set up stock market"
    market = setUpMarket(investors, params['investor_start'])

    "Get largest number of connections any one investor has"
    largestNumConnections = getLargestNumConnections(s)
    "Get average number of connections within social sphere (B-A model)"
    averageNumConnections = getAverageNumConnections(s)

    "Run simulation over multiple time steps, and plot results as they're generated"
    marketValues = []
    marketValues.append(market.totalShares)
    for i in range(1,(params['timesteps']+1)):
        tick(market, investors, s, marketValues, i, largestNumConnections, averageNumConnections, params['herd'])
        marketValues.append(market.totalShares)

    "Print all results to a csv file"
    with open('results.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(marketValues)

main()
