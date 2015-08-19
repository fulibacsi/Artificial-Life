# encoding: utf-8

import random
from operator import itemgetter


# consumer entities
class Consumer(object):

    # init
    # aggression - the rating of attacking other consumers
    # agility - the rating of dodgeing attacks and attacking successfully
    # hunger - the overall hunger
    def __init__(self, id, aggression, reproduction, agility,
                 base_hunger, hunger_function):
        self.id = id
        self.type = 'con'
        self.aggression = aggression
        self.reproduction = reproduction
        self.agility = agility
        self.hunger = base_hunger
        self.hunger_function = hunger_function

    # decrease hunger
    def decrease_hunger(self, value):
        self.hunger = max(0.0, self.hunger - value)

    # create a need pyramid, then decide based on the created pyramid
    def create_piramid(self, environment):
        # create the piramid with the actual values
        pyramid = (
            ('hun', self.hunger),
            ('agg', self.aggression),
            ('rep', self.reproduction)
        )
        # get the dominant need
        dominant, dom_value = max(pyramid, key=itemgetter(1))

        # if hungry
        # if there's resource consume, else move
        if dominant == 'hun':
            resources = [res for res in environment if res.type == 'res']
            if len(resources):
                return ('hun', resources[0])

        # if aggressive or reproductive
        else:
            consumers = [con for con in environment
                         if con.type == 'con' and con.id != self.id]
            if len(consumers):
                return (dominant, max(consumers, key=lambda con: con.agility))

        # default action - random movement
        return ('mov', random.randint(0, 3))

    # what to do in a round
    # environment - the other objects in the tile
    def tick(self, environment):
        # determine action
        decision = self.create_piramid(environment)
        # increase hunger
        self.hunger = self.hunger_function(self.hunger)

        # send the decision to the evironment
        return decision

    def __repr__(self):
        return ('Consumer {id} (agg: {agg}, rep: {rep}, agi: {agi})'
                .format(
                    id=self.id,
                    agg=self.aggression,
                    rep=self.reproduction,
                    agi=self.agility))
