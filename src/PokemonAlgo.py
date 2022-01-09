from types import SimpleNamespace
from src.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from src.GraphAlgo import GraphAlgo
from src.Pokemon import Pokemon
from src.Agent import Agent
import math
import random
class PokemonAlgo:

    def __init__(self,graph: str, pokemons: str, agents):
        self.graphAlgo = GraphAlgo()
        self.graphAlgo.load_from_json(graph)
        self.pokemonList = []
        self.loadPokemons_from_json(pokemons)
        self.agentList = {}

    def loadPokemons_from_json(self, pokemons):
        dict = json.loads(pokemons)
        pokemonList = []
        for pokemon in dict['Pokemons']:
            value = pokemon['Pokemon']['value']
            type = pokemon['Pokemon']['type']
            pos = list(map(float, pokemon['Pokemon']['pos'].split(',')))
            edge = self.findEdge(pos,type)
            pokemonList.append(Pokemon(value,type,edge,pos))
            pokemonList.sort(key=lambda x : x.value)
        self.pokemonList  = pokemonList

    def findEdge(self, pos, type):
        for src in self.graphAlgo.get_graph().nodes.keys():
            srcNode = self.graphAlgo.get_graph().nodes[src]
            for dest in self.graphAlgo.get_graph().edgesOut[src].keys():
                destNode = self.graphAlgo.get_graph().nodes[dest]
                if((type > 0 and src < dest) or (type < 0 and src > dest)):
                    line1 = PokemonAlgo.distance(srcNode.pos,destNode.pos)
                    line2 = PokemonAlgo.distance(srcNode.pos,pos) + PokemonAlgo.distance(pos,destNode.pos)
                    if(line1 > line2 - 0.0000001):
                        return [src,dest]
        return null

    def loadAgents_from_json(self,str):
        agent_dict = json.loads(str)
        # if first:
        agentList = {}
        for agent in agent_dict['Agents']:
            id = agent['Agent']['id']
            value = agent['Agent']['value']
            src = agent['Agent']['src']
            dest = agent['Agent']['dest']
            speed = agent['Agent']['speed']
            pos = list(map(float, agent['Agent']['pos'].split(',')))
            agentList[id] = Agent(id, value, src, dest, speed, pos)
        self.agentList = agentList
        # else:
        #     for agent in agent_dict['Agents']:
        #         id = agent['Agent']['id']
        #         self.agentList[id].value = agent['Agent']['value']
        #         self.agentList[id].src = agent['Agent']['src']
        #         self.agentList[id].dest = agent['Agent']['dest']
        #         self.agentList[id].speed = agent['Agent']['speed']
        #         self.agentList[id].pos = list(map(float, agent['Agent']['pos'].split(',')))

    # Finds pokemon to which to send the agent
    def choosePokForAgent(self, agent: Agent):
        minDist = float('inf')
        pokemonMin = None
        index = None
        next_node = None
        for p, pokemon in enumerate(self.pokemonList):
            if agent.src == pokemon.edge[0]:
                return pokemon, pokemon.edge[1]
            dist, next_node_temp = self.graphAlgo.shortest_path(agent.src, pokemon.edge[0])
            if dist < minDist:
                minDist = dist
                pokemonMin = pokemon
                index = p
                if len(next_node_temp) == 1:
                    next_node = next_node_temp[0]
                else:
                    next_node = next_node_temp[1]
        # self.pokemonList.remove(pokemon)
        del self.pokemonList[index]
        return pokemonMin, next_node

    # def choosePockForAgent(self, agent):
    #     minDist = float('inf')
    #     minPath = []
    #     pokemonMin = -1
    #     for i in range(len(self.pokemonList)):
    #         # if self.agentList[agent].src == self.pokemonList[i].edge[0]:
    #         #     self.agentList[agent].path = {self.pokemonList[i].edge[1]}
    #         if self.pokemonList[i].available is False:
    #             dist = self.graphAlgo.shortest_path(self.agentList[agent].src,self.pokemonList[i].edge[0])
    #             if dist[0] < minDist:
    #                 minDist = dist[0]
    #                 minPath = dist[1]
    #                 minPath.append(self.pokemonList[i].edge[1])
    #                 pokemonMin = i
    #     self.agentList[agent].path = list(self.agentList[agent].path) + list(minPath)
    #     self.pokemonList[pokemonMin].available = False
    #     # return pokemonMin

    @staticmethod
    def distance(pos1,pos2):
        dis =  math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2) + math.pow(pos1[2] - pos2[2], 2))
        return dis
