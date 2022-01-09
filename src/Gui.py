import asyncio
import sys
from client import Client
import json
import pygame
from GraphAlgo import GraphAlgo
from pygame import *
from src import PokemonUtils
from src.AgentUtils import Agent
from src.PokemonUtils import Pokemon

WIDTH, HEIGHT = 1080, 720
PORT = 6666
HOST = '127.0.0.1'

pygame.init()

client = Client()
client.start_connection(HOST, PORT)

# Get the graph
file = client.get_graph()
graph = GraphAlgo()
graph.load_from_json(file)
print(graph)


# Get the pokemons
pokemon_list = client.get_pokemons()
pokemons = graph.load_pokemons(pokemon_list)
print(pokemons)

# Get the agents
info = json.loads(client.get_info())
num_agents = info['GameServer']['agents']
for n in range(num_agents):
    name = "{\"id\":"+str(n)+"}"
    client.add_agent(name)

agent_list = client.get_agents()
agents = graph.load_agents(agent_list)
print(agents)

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)

pygame.font.init()
FONT = pygame.font.SysFont("comicsansms", 17, bold=True)
clock = pygame.time.Clock()

client.start()

minX = sys.float_info.max
minY = sys.float_info.max
maxX = sys.float_info.min
maxY = sys.float_info.min

for n, node in graph.nodes.items():
    point_x = float(node.getPos()[0])
    point_y = float(node.getPos()[1])
    if point_x > maxX:
        maxX = point_x
    if point_y > maxY:
        maxY = point_y
    if point_x < minX:
        minX = point_x
    if point_y < minY:
        minY = point_y

absX = abs(maxX-minX)
absY = abs(maxY-minY)

scaleX = (WIDTH/absX)*0.9
scaleY = (HEIGHT/absY)*0.9

# Moves counter
moves = info['GameServer']['moves']

async def move_after(delay):
    await asyncio.sleep(delay)
    client.move()

async def move_pokemons2(flag: bool = False):
    if not flag:
        await move_after(0.15)
    if flag:
        client.move()

while client.is_running() == 'true':

    pygame.display.set_caption("Pokemon Game - Ex4")

    # Color the screen
    screen.fill(Color(173,216,230))
    bg = pygame.image.load("img.png")

    # INSIDE OF THE GAME LOOP
    screen.blit(bg, (0, 0))
    # Update number of moves
    moves = info['GameServer']['moves']

    # Draw the graph

    # Get nodes
    for n, node in graph.nodes.items():
        x = int((float(node.getPos()[0]) - minX) * scaleX * 0.9 + 32)
        y = int((float(node.getPos()[1]) - minY) * scaleY * 0.9 + 32)
        pygame.draw.circle(screen, (0,205,102), [x-7,y-7], 20)

        # draw node id
        id_srf = FONT.render(str(node.getId()), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # Get edges
    for e, edge in graph.edges.items():
        src = graph.nodes.get(edge['src'])
        dest = graph.nodes.get(edge['dest'])
        src_x = int((float(src.getPos()[0]) - minX) * scaleX * 0.9 + 32)
        src_y = int((float(src.getPos()[1]) - minY) * scaleY * 0.9 + 32)
        dest_x = int((float(dest.getPos()[0]) - minX) * scaleX * 0.9 + 32)
        dest_y = int((float(dest.getPos()[1]) - minY) * scaleY * 0.9 + 32)
        pygame.draw.line(screen, Color(0,0,0), (src_x, src_y), (dest_x, dest_y), 2)

    # Get pokemons
    pokemon_list = client.get_pokemons()
    pokemons = graph.load_pokemons(pokemon_list)

    for p,pokemon in pokemons.items():
        positions = pokemon.get_pos().split(',')
        x = int((float(positions[0]) - minX) * scaleX * 0.9 + 32)
        y = int((float(positions[1]) - minY) * scaleY * 0.9 + 32)
        if(pokemon.type==1):
            pygame.draw.circle(screen, (152,245,255), [x - 7, y - 7], 20) # Light blue if up
        else:
            pygame.draw.circle(screen, (255,255,0), [x - 7, y - 7], 20) # Yellow if down

    # Get agents
    info = json.loads(client.get_info())
    num_agents = info['GameServer']['agents']
    for n in range(num_agents):
        name = "{\"id\":" + str(n) + "}"
        client.add_agent(name)

    agent_list = client.get_agents()
    agents = graph.load_agents(agent_list)

    for a, agent in agents.items():
        positions = agent.get_pos().split(',')
        x = int((float(positions[0]) - minX) * scaleX * 0.9 + 32)
        y = int((float(positions[1]) - minY) * scaleY * 0.9 + 32)
        pygame.draw.circle(screen, (127,255,0), [x - 7, y - 7], 20) # Agents are green

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # Timer window
    pygame.draw.rect(screen, (198,226,255), [20, 5, 75,45], border_radius=15)
    time_text = FONT.render("Time: " + str(int(pygame.time.get_ticks() / 1000)), True, Color(0,0,0))
    screen.blit(time_text, (23, 12))

    # Stop button
    button = pygame.Rect(20, 55, 75,45)
    stop_text = FONT.render("Stop", True, Color(0, 0, 0))
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if button.collidepoint(mouse_pos):
            client.stop()
    pygame.draw.rect(screen, (198,226,255), button, border_radius=15)
    screen.blit(stop_text, (30, 65))

    # Moves counter window
    pygame.draw.rect(screen, (198,226,255),[20, 105, 75,45] ,border_radius=15)
    moves_text = FONT.render("Moves: " + str(moves), True, Color(0,0,0))
    screen.blit(moves_text, (20, 110))

    # Update screen changes
    display.update()
    clock.tick(60)

    # Allocates a pokemon for each agent
    pokemons_copy = pokemons.copy()
    for a, agent in agents.items():
        if agent.get_dest() == -1:
            pokemon, next_node = graph.choosePokForAgent(agent, pokemons_copy)
            client.choose_next_edge('{"agent_id":' + str(agent.get_id()) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    move = False
    for a, agent in agents.items():
        for p, pokemon in pokemons.items():
            if agent.get_src() == pokemon.get_src() and agent.get_dest() == pokemon.get_dest():
                move = True
                break
        if move:
            break

    asyncio.run(move_pokemons2(move))