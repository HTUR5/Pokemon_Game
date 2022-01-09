import asyncio
from types import SimpleNamespace
import time
import json
from pygame import gfxdraw, display, RESIZABLE
import pygame
# from pygame import *
from pygame.color import Color

from client_python.Agent import Agents
from client_python.DiGraph import DiGraph
from client_python.GraphAlgo import GraphAlgo

from client import Client
from client_python.pokemon import Pokemons
from client_python.pokemon import Pokemon

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

# pokemons = client.get_pokemons()
# pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
#
# print(pokemons)

FONT = pygame.font.SysFont('Arial', 20, bold=True)


graph_json = client.get_graph()
print(graph_json)
graph = DiGraph(graph_json)
Agraph = GraphAlgo(graph)

# get data proportions
min_x = min(list(graph.nodes.values()), key=lambda n: n.x).x
min_y = min(list(graph.nodes.values()), key=lambda n: n.y).y
max_x = max(list(graph.nodes.values()), key=lambda n: n.x).x
max_y = max(list(graph.nodes.values()), key=lambda n: n.y).y
radius = 15


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


async def move_after(delay):
    await asyncio.sleep(delay)
    client.move()


async def move_pokemons(flag: bool = False):
    if not flag:
        await move_after(0.122)
    if flag:
        client.move()



info_details = json.loads(client.get_info())
num_of_agents = info_details['GameServer']['agents']
i = 0
while i < num_of_agents:
    client.add_agent("{\"id\":" + str(i) + "}")
    i += 1
client.start()

agents = Agents(client.get_agents(), graph)

while client.is_running() == 'true':
    # for agent in agents.agent_dict.values():
    #     print(agent.node_tasks)

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

    pokemons = Pokemons(client.get_pokemons(), graph)
    pokemons.pokemon_list.sort(key=lambda x: x.value)

    # agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
    # agents = [agent.Agent for agent in agents]
    # for a in agents:
    #     x, y, _ = a.pos.split(',')
    #     a.pos = SimpleNamespace(x=my_scale(float(x), x=True), y=my_scale(float(y), y=True))

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button.collidepoint(mouse_pos):
                client.stop()

    # draw nodes
    for node_id, node_data in graph.nodes.items():
        srcX = graph.nodes[node_id].x
        srcY = graph.nodes[node_id].y

        x = my_scale(srcX, x=True)
        y = my_scale(srcY, y=True)

        gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(node_id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for node_id, node_data in graph.nodes.items():
        for dest_node_id, edge_weight in graph.nodes[node_id].edge_out.items():
            srcX = graph.nodes[node_id].x
            srcY = graph.nodes[node_id].y
            destX = graph.nodes[dest_node_id].x
            destY = graph.nodes[dest_node_id].y

            src_x = my_scale(srcX, x=True)
            src_y = my_scale(srcY, y=True)
            dest_x = my_scale(destX, x=True)
            dest_y = my_scale(destY, y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents.agent_dict.values():
        pygame.draw.circle(screen, Color(122, 61, 23), (int(my_scale(float(agent.x), x=True)), int(my_scale(float(agent.y), y=True))), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons.pokemon_list:
        # if up and if down, different colors
        pygame.draw.circle(screen, p.color,
                           (int(my_scale(float(p.x), x=True)), int(my_scale(float(p.y), y=True))), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    agents.change_values(client.get_agents(), graph)
    for pokemon in pokemons.pokemon_list:
        min_path = float('inf')
        chosen_a = None
        short_path_of_chosen = []
        taken = False
        for agent in agents.agent_dict.values():
            if agent.already_taken(pokemon.src, pokemon.dest):
                taken = True
                break
        if taken:
            continue
        for agent in agents.agent_dict.values():
            if agent.node_tasks:
                n1 = agent.node_tasks[-1]
            else:
                if agent.dest == -1:
                    n1 = agent.current
                else:
                    n1 = agent.dest
            n2 = pokemon.src
            current = Agraph.shortest_path(n1, n2)
            if min_path > agent.path + (current[0]/agent.speed):
                min_path = agent.path + (current[0]/agent.speed)
                short_path_of_chosen = current[1]
                chosen_a = agent.id
        agents.agent_dict[chosen_a].add_task(short_path_of_chosen, pokemon.dest)
        agents.change_values(client.get_agents(), graph)


    # choose next edge
    for agent in agents.agent_dict.values():
        if agent.dest == -1 and len(agent.node_tasks) > 0:
            next_node = agent.next_node()
            agent.remove_task()
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())


    move = False
    for agent in agents.agent_dict.values():
        for pokemon in pokemons.pokemon_list:
            if agent.src == pokemon.src and agent.dest == pokemon.dest:
                move = True
                break
        if move:
            break

    asyncio.run(move_pokemons(move))
# game over: