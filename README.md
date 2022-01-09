# Pokemon_Game <br>
## Ex4 <br>
## Hodaya Turgeman & Sivan Cohen <br>

In this assignment, we were required to design a “Pokemon game” in which given a weighted graph,  a set of “Agents” should be located on it so they could “catch” as many “Pokemons” as possible. The pokemons are located on the graph’s (directed) edges, therefore, the agent needs to take (aka walk)  the proper edge to “grab” the pokemon. our goal is to maximize the overall sum of weights of the “grabbed” pokemons (while not exceeding the maximum amount of server calls allowed in a second - 10 max). <br>

In order to implement this game, we created this classes: <br>
### 1. Agent <br>
  this class represents an agent. for each agent we save this information: <br>
  its id, value, src, dest, speed and its pos. <br>
### 2. Pokemon <br>
  this class represents a pokemon. for each pokemon we save this information: <br>
  its value, type, edge and pos. <br>
  type is positive if the edge_dest > edge_src. <br> 
  The pokemon's edge is calculated according to its position by the "triangle inequality": <br>
  if the distance from u to v is close enough to the distance from u to pokemon p + distance from p to v than p lies on the edge (u,v). <br>
### 2. PokemonAlgo <br>
  this class represents a Pokemon game. for each game we save this information: <br>
  - its graph: <br>
    we used the last assignment and creat a GraphAlgo from the data of the graph game, in order to use its functions (like shortPath). <br>
  - A list of pokemons <br>
  - A dict of agents <br>
  so in this object we can read and update the pokemons and agents lists <br>
    
  

       


