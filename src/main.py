from types import SimpleNamespace
from src.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from src.GraphAlgo import GraphAlgo
from src.Pokemon import Pokemon
from src.Agent import Agent
import asyncio
from types import SimpleNamespace
from src.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from PokemonAlgo import PokemonAlgo

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)
FONT = pygame.font.SysFont('Arial', 20, bold=True)

numAgents = json.loads(client.get_info())['GameServer']['agents']
game = PokemonAlgo(client.get_graph(), client.get_pokemons(), int(numAgents))

# def makeAgents(self, numOFagents: int):
for index in range(numAgents):
    if index <= len(game.pokemonList):
        startNode = game.pokemonList[index].edge[0]
    else:
        startNode = random.randrange(game.graphAlgo.get_graph().v_size())
    client.add_agent('{id:' + str(startNode) + '}')


# get data proportions
min_x = min(list(game.graphAlgo.graph.nodes.values()), key=lambda n: n.pos[0]).pos[0]
min_y = min(list(game.graphAlgo.graph.nodes.values()), key=lambda n: n.pos[1]).pos[1]
max_x = max(list(game.graphAlgo.graph.nodes.values()), key=lambda n: n.pos[0]).pos[0]
max_y = max(list(game.graphAlgo.graph.nodes.values()), key=lambda n: n.pos[1]).pos[1]
radius = 15

def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen

# decorate scale with the correct values
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)

# this commnad starts the server - the game is running now
client.start()

game.loadAgents_from_json(client.get_agents())
# print(client.get_info())
# print(client.get_agents())
# print(client.get_pokemons())


async def move_after(delay):
    await asyncio.sleep(delay)
    client.move()

async def move_pokemons(flag: bool = False):
    if not flag:
        await move_after(0.122)
    if flag:
        client.move()

while client.is_running() == 'true':

    pygame.display.set_caption("Pokemon Game - Ex4")

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # Timer window
    pygame.draw.rect(screen, (255, 193, 193), [20, 10, 90, 45], border_radius=15)
    time_text = FONT.render("Time: " + str(int(pygame.time.get_ticks() / 1000)), True, Color(0, 0, 0))
    screen.blit(time_text, (30, 20))

    # Stop button
    button = pygame.Rect(120, 10, 90, 45)
    stop_text = FONT.render("Stop", True, Color(0, 0, 0))
    pygame.draw.rect(screen, (255, 193, 193), button, border_radius=15)
    screen.blit(stop_text, (148, 20))

    # Moves counter window
    pygame.draw.rect(screen, (255, 193, 193), [220, 10, 90, 45], border_radius=15)
    info_details = json.loads(client.get_info())
    moves = info_details['GameServer']['moves']
    moves_text = FONT.render("Moves: " + str(moves), True, Color(0, 0, 0))
    screen.blit(moves_text, (221, 20))

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button.collidepoint(mouse_pos):
                client.stop()

    # Draw the graph
    # draw nodes
    for node_id,node in game.graphAlgo.get_graph().get_all_v().items():
        srcX = node.get_pos()[0]
        srcY = node.get_pos()[1]

        x = my_scale(srcX, x=True, y=False)
        y = my_scale(srcY, x=False, y=True)

        gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(node_id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for node_id, node_data in game.graphAlgo.get_graph().get_all_v().items():
        for dest_node_id, edge_weight in game.graphAlgo.get_graph().all_out_edges_of_node(node_id).items():
            srcX = node_data.get_pos()[0]
            srcY = node_data.get_pos()[1]
            nodeDest = game.graphAlgo.get_graph().get_all_v()[dest_node_id]
            destX = nodeDest.get_pos()[0]
            destY = nodeDest.get_pos()[1]

            src_x = my_scale(srcX, x=True)
            src_y = my_scale(srcY, y=True)
            dest_x = my_scale(destX, x=True)
            dest_y = my_scale(destY, y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))

    game.loadPokemons_from_json(client.get_pokemons())
    game.loadAgents_from_json(client.get_agents())

    # Get pokemons
    pokemon_list = game.pokemonList
    for p in pokemon_list:
        if (p.type == 1):
            pygame.draw.circle(screen, (138, 43, 226), (int(my_scale(float(p.pos[0]), x=True)), int(my_scale(float(p.pos[1]), y=True))), 10) # Purple if up
        else:
            pygame.draw.circle(screen, (152, 245, 255), (int(my_scale(float(p.pos[0]), x=True)), int(my_scale(float(p.pos[1]), y=True))), 10)  # Light blue if down

    # Get agents
    agent_list = game.agentList
    for a in agent_list.values():  # Agents are green
        pygame.draw.circle(screen, Color(122, 61, 23), (int(my_scale(float(a.pos[0]), x=True)), int(my_scale(float(a.pos[1]), y=True))), 10)  # Agents are green


    # Update screen changes
    display.update()
    clock.tick(60)

    # Allocates a pokemon for each agent
    # pokemons_copy = pokemons.copy()
    for a, agent in game.agentList.items():
        if agent.dest == -1:
            pokemon, next_node = game.choosePokForAgent(agent)
            client.choose_next_edge('{"agent_id":' + str(agent._id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            # print(ttl, client.get_info())

    move = False
    for a, agent in game.agentList.items():
        for p, pokemon in enumerate(game.pokemonList):
            if agent.src == pokemon.edge[0] and agent.dest == pokemon.edge[1]:
                move = True
                break
        if move:
            break

    asyncio.run(move_pokemons(move))

# for agent in game.agentList.values():
    #     if agent.dest == -1:
    #         if len(agent.path) == 0:
    #             game.choosePockForAgent(agent._id)
    #         if agent.path[0] == agent.src:
    #             agent.path.pop(0)
    #     if len(agent.path) > 0:
    #         client.choose_next_edge('{"agent_id":' + str(agent._id) + ', "next_node_id":' + str(agent.path.pop(0)) + '}')
    # # oo = client.get_agents()
    # game.loadAgents_from_json(client.get_agents())
    # move = False
    # for agent in game.agentList.values():
    #     for pokemon in pokemon_list:
    #         if agent.src == pokemon.edge[0] and agent.dest == pokemon.edge[1]:
    #             move = True
    #             break
    #     if move:
    #         break
    # asyncio.run(move_pokemons(move))
# game over:

