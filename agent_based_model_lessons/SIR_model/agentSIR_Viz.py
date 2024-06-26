# If MoneyModel.py is where your code is:
from agentSIR import mesa, SIRModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if agent.susceptible == 1:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.exposed == 1:
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 1
    elif agent.infected == 1:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
    else:
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 3
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = mesa.visualization.ChartModule(
    [{"Label": "S_pop", "Color": "Green"},{"Label": "E_pop", "Color": "Yellow"},
     {"Label": "I_pop", "Color": "Red"},{"Label": "R_pop", "Color": "Purple"}], data_collector_name="datacollector"
)
server = mesa.visualization.ModularServer(
    SIRModel, [grid,chart], "SIRModel", {"N": 100, "width": 10, "height": 10}
)
server.port = 8521  # The default
server.launch()