import mesa

# Data visualization tools.
import seaborn as sns

# Has multi-dimensional arrays and matrices. Has a large collection of
# mathematical functions to operate on these arrays.
import numpy as np

# Data manipulation and analysis.

def compute_S(model):
    agent_S = [agent.susceptible for agent in model.schedule.agents]
    x = sum(agent_S)
    return x

def compute_E(model):
    agent_E = [agent.exposed for agent in model.schedule.agents]
    x = sum(agent_E)
    return x

def compute_I(model):
    agent_I = [agent.infected for agent in model.schedule.agents]
    x = sum(agent_I)
    return x

def compute_R(model):
    agent_R = [agent.recovered for agent in model.schedule.agents]
    x = sum(agent_R)
    return x

class DisaseAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)
        # Create the agent's variable and set the initial values.
        a =self.random.random()
        if a < 0.1:   
            self.susceptible = 0
            self.exposed = 0
            self.infected = 1
            self.recovered = 0
        elif a < 0.3:   
            self.susceptible = 0
            self.exposed = 1
            self.infected = 0
            self.recovered = 0
        else:
            self.susceptible = 1
            self.exposed = 0
            self.infected = 0
            self.recovered = 0
        a =self.random.random()
        if a < .3:
            self.weakImmuneSystem = 1
        else: 
            self.weakImmuneSystem = 0
    def step(self):
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        self.move()
        if self.exposed == 1:
            a =self.random.random()
            if a < 0.05:   
                self.exposed = 0
                self.infected = 1
            elif a < .10:
                self.treat()
        elif self.infected == 1:
            self.infect()
            a =self.random.random()
            if a < 0.05:   
                self.infected = 0
                self.recovered = 1
            elif a < .20:
                self.treat()
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore = True,include_center = False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    def treat(self):
        a =self.random.random()
        if a < 0.1:   
            self.exposed = 0
            self.infected = 0
            self.recovered = 1
    def infect(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        cellmates.pop(cellmates.index(self))
        if len(cellmates) > 1:
            for i in cellmates:
                other = i
                if other.susceptible == 1:
                    a =self.random.random()
                    if a < .1 + other.weakImmuneSystem*.5:
                        other.susceptible = 0
                        other.exposed = 1
            if other == self:
                print("heheheheheh i just gave the infection to myself")

class SIRModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height,True)
        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = DisaseAgent(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a,(x,y))
        self.datacollector = mesa.DataCollector(
            model_reporters={"S_pop": compute_S,"E_pop": compute_E,"I_pop": compute_I,"R_pop": compute_R},
            agent_reporters={"Susceptible":"susceptible","Exposed":"exposed", "Infected": "infected","Recovered":"recovered"},
        )
    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()

model = SIRModel(500, 10, 10)
for i in range(500):
    model.step()
agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell_content, (x, y) in model.grid.coord_iter():
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
# Plot using seaborn, with a size of 5x5
g = sns.heatmap(agent_counts, cmap="viridis", annot=True, cbar=False, square=True)
g.figure.set_size_inches(4, 4)
g.set(title="Number of agents on each cell of the grid");
print("cat")

agent_states = model.datacollector.get_agent_vars_dataframe()

one_agent_wealth = agent_states.xs(14, level="AgentID")

# Plot the wealth of agent 14 over time
g = sns.lineplot(data=one_agent_wealth, x="Step", y="Susceptible")
g = sns.lineplot(data=one_agent_wealth, x="Step", y="Exposed")
g = sns.lineplot(data=one_agent_wealth, x="Step", y="Infected")
g = sns.lineplot(data=one_agent_wealth, x="Step", y="Recovered")
g.set(title="Wealth of agent 14 over time");
print("cat")

SIR_pop = model.datacollector.get_model_vars_dataframe()
# Plot the Gini coefficient over time
g = sns.lineplot(data=SIR_pop)
#g = sns.lineplot(data=I_pop, x="Step", y="Infected")
#g = sns.lineplot(data=R_pop, x="Step", y="Recovered")
#g.set(title="Gini Coefficient over Time", ylabel="Gini Coefficient");

print("cat")