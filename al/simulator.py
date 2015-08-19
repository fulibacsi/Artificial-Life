# encoding: utf-8

import random

from grid import Grid
from resource import Resource
from consumer import Consumer


# handles the simulation
class Simulator(object):

    # init
    def __init__(self, size, num_of_resources, num_of_consumers, resource_popup,
                 base_hunger, hunger_function, seed=None):
        # set random seed
        random.seed(seed)
        # parameter setup
        self.size = size
        self.num_of_resources = num_of_resources
        self.num_of_consumers = num_of_consumers
        self.resource_popup = resource_popup
        self.base_hunger = base_hunger
        self.hunger_function = hunger_function

        # world creation
        self.world = Grid(size, self.world_type_determiner)
        self.resources = self.generate_resources(self.num_of_resources)
        self.consumers = self.generate_consumers(self.num_of_consumers)
        self.place_all()
        print 'world created!'

        # additional information storing
        self.reproducers = []
        self.round = 0
        self.action_list = []

    # determine type of the world
    def world_type_determiner(self, pos):
        return random.random()

    # generate resources
    def generate_resources(self, number):
        return [
            Resource(
                id=i,
                value=random.random() + 1.0,
                rate=random.random() * 0.5
            )
            for i in xrange(number)
        ]

    # generate consumers
    def generate_consumers(self, number):
        return [
            Consumer(
                id=i,
                aggression=random.random(),
                reproduction=random.random(),
                agility=random.random(),
                base_hunger=self.base_hunger,
                hunger_function=self.hunger_function
            ) for i in xrange(number)
        ]

    # place the initial objects to the grid
    def place_all(self):
        # place all resources and consumers to the world
        for resource in self.resources:
            num = random.randint(0, self.size**2 - 1)
            self.world.put_to_num(thing=resource, num=num)
        for consumer in self.consumers:
            num = random.randint(0, self.size**2 - 1)
            self.world.put_to_num(thing=consumer, num=num)

    # place an object randomly to the grid
    def place(self, thing):
        num = random.randint(0, self.size**2 - 1)
        self.world.put_to_num(thing=thing, num=num)

    def attack(self, attacker, attacked):
        place = self.world.where_is(attacker)
        winner, loser = sorted([attacker, attacked],
                                key=lambda x: x.agility,
                                reverse=True)
        if [attacker.id, attacked.id] == [winner.id, loser.id]:
            msg = ('test: Consumer {0} attacked'
                   ' and killed Consumer {1}!').format(attacker.id, attacked.id)
        else:
            msg = ('test: Consumer {0} attacked'
                   ' Consumer {1} and died!').format(attacker.id, attacked.id)
        self.world.remove_from_pos(thing=loser, pos=place)
        self.consumers.remove(loser)
        self.action_list.append(msg)

    # defines consume mechanism
    def consume(self, consumer, consumed):
        # add to the report
        self.action_list.append(
            'Consumer {0} consumed Resource {1}!'
            .format(consumer.id, consumed.id)
        )
        # consume the resource, lower the hunger
        consumer.decrease_hunger(consumed.consume())
        # if resource is consumed totally,
        if not consumed.value:
            # remove from world
            self.world.remove_from_pos(
                thing=consumed,
                pos=self.world.where_is(consumed)
            )
            # remove from exsistence
            self.resources.remove(consumed)

    # define reproducing
    def reproduce(self, initiator, target):
        # ensure order
        intention = sorted([initiator, target])
        if intention in self.reproducers:
            self.reproducers.remove(intention)
            # determine the replicant's values
            # randomly select between
            #   - mutation - new random value
            #   - crossover - average value
            #   - selection - better value
            #   - deflection - lower value
            aggression = random.choice([
                random.random(),
                (initiator.aggression + target.aggression) / 2.0,
                max(initiator.aggression, target.aggression),
                min(initiator.aggression, target.aggression)
            ])
            reproduction = random.choice([
                random.random(),
                (initiator.reproduction + target.reproduction) / 2.0,
                max(initiator.reproduction, target.reproduction),
                min(initiator.reproduction, target.reproduction)
            ])
            agility = random.choice([
                random.random(),
                (initiator.agility + target.agility) / 2.0,
                max(initiator.agility, target.agility),
                min(initiator.agility, target.agility)
            ])
            # increase the corresponding id
            self.num_of_consumers += 1
            # create the new consumer with the new attribute values
            temp = Consumer(
                id=self.num_of_consumers,
                aggression=aggression,
                reproduction=reproduction,
                agility=agility,
                base_hunger=self.base_hunger,
                hunger_function=self.hunger_function
            )
            # add the replicant to consumer list, and place it to the world
            self.consumers.append(temp)
            self.place(temp)
            # report success
            msg = ('Consumer {0} and Consumer {1} created Consumer {2}!'
                   .format(initiator.id, target.id, temp.id))
            self.action_list.append(msg)
        else:
            msg = ('Consumer {0} tried to reproduce'
                   ' with Consumer {1} (ag: {2})!'
                   .format(initiator.id, target.id, round(target.agility, 2)))
            self.action_list.append(msg)
            self.reproducers.append(intention)

    # defines move mechanism
    def move(self, thing, direction):
        pos = self.world.move_to_dir(
            thing=thing,
            start=self.world.where_is(thing),
            dir=direction
        )
        # report success
        self.action_list.append('Consumer {0} moved to {1}!'
                                .format(thing.id, pos))

    # one step of the worlds
    def tick(self):
        # set up round
        self.round += 1
        self.action_list = []

        # handle resources
        for resource in self.resources:
            resource.tick()
            # if the resource is out of power, remove it
            if resource.value <= 0.0:
                self.world.remove_from_pos(
                    thing=resource,
                    pos=self.world.where_is(resource)
                )
                self.resources.remove(resource)
        # there's a chance for a new resource to pop up
        if random.random() < self.resource_popup:
            # increase the corresponding id
            self.num_of_resources += 1
            # create the new resource
            temp = Resource(
                id=self.num_of_resources,
                value=random.random() + 1.0,
                rate=random.random() * 0.5
            )
            self.resources.append(temp)
            self.place(temp)
            # report success
            self.action_list.append('Resource {0} created!'.format(temp.id))

        # save actual populations, newborn consumers cannot act
        actPopulation = self.consumers
        # handle consumers
        for consumer in actPopulation:
            # if starved to death, remove it
            if consumer.hunger >= 1.0:
                # report death
                msg = 'Consumer {0} starved to death!'.format(consumer.id)
                self.action_list.append(msg)
                # remove from world, and from the consumer list
                self.world.remove_from_pos(
                    thing=item,
                    pos=self.world.where_is(consumer)
                )
                self.consumers.remove(consumer)
            # else act accordingly
            else:
                # get the decision that the consumer has taken
                todo = consumer.tick(
                    environment=self.world.on_which_tile(consumer).on_tile
                )

                # execute
                if todo[0] == 'hun':
                    self.consume(consumer, todo[1])
                elif todo[0] == 'agg':
                    self.attack(consumer, todo[1])
                elif todo[0] == 'mov':
                    self.move(consumer, todo[1])
                elif todo[0] == 'rep':
                    self.reproduce(consumer, todo[1])

        # report extreme values
        if not len(self.resources):
            self.action_list.append('Out of Resources!')
        if not len(self.consumers):
            self.action_list.append('Consumers extinct!')

    # print the collected reports
    def report(self):
        print 'Round ', self.round, ':'
        print ('{0} Consumer - {1} Resource'
               .format(len(self.consumers), len(self.resources)))
        for item in self.action_list:
            print item

    def get_report(self):
        pass
