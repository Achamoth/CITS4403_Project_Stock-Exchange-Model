Basic Operation:
-To run program, run “Runner.py” from terminal
-When the simulation finishes, the program will display a plot of the market values
over time
-It will also export the plot as an image titled “results.jpg”
-It will also export a csv file (can be opened in excel) containing all of the market
values. Filename will be “results.csv”

Setting Parameters:
-Can set parameters of interest through “config.txt”
-These parameters will be read in when the program is run

Parameter descriptions:
-model: Specifies the model to use for the social network of investors. ‘ba’ refers
to Barabasi-Albert, ‘ws’ refers Watts-Strogatz

-size: Specifies the number of investors in the market

-investor_start: When the market is initialised, each investor is given a chance to
start off already in the market. This specifies the probability (for each investor)
that they will start off in the market

-herd: Specifies whether or not investors react to the actions and stances of their
connections. If this is switched off, investors will only react to the movements of
the market, and will pay no attention at all to their connections. Thus the social
network (the graph of investors) will not be used, and will have no bearing. 
Essentially, switching this off will completely remove the social reactivity element
from the simulation. Switching it off produces the “No Herd Behaviour” mentioned in
the case study (figure 2)

-k: Parameter used for construction of Watts-Strogatz model (if that is not the
selected model, this parameter has no bearing). For ‘ws’ model, this value determines
the degree of the initial regular graph used to construct the Watts-Strogatz network

-rewire: Parameter used for construction of Watts-Strogatz model (has no bearing if
that is not the selected model). This parameter is the probability of edge rewiring.