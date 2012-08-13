# -*- coding:Utf-8 -*-
## ----- AL.py -----
##
##  Usage:
##      python AL.py
##
##	A small and simple experiment with simulating artificial life.
##
##          Tested on Windows 7 and Ubuntu environment!
##
## Copyright (C) 2012, Fülöp András, fulibacsi@gmail.com
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http:##www.gnu.org/licenses/>.
##

# imports
from random import random, randint, choice




# tile
class Tile():
	
	# init
	def __init__(self, pos, type, onTile):
		self.pos = pos
		self.type = type
		self.onTile = onTile
	
	
	
	# position of the Tile
	def getPos(self):
		return self.pos
	
	
	# type of the Tile
	def getType(self):
		return self.type
	
	
	# objects on the Tile
	def getOnTile(self):
		return self.onTile
		
		
	# put an object to the Tile
	def putTo(self, thing):
		self.onTile.append(thing)
		
		
	# object is on the Tile
	def has(self, thing):
		return self.onTile.count(thing)
		
		
	# a type of object is on the Tile
	def hasA(self, thingType):
		for item in self.onTile:
			if item.getType() == thingType:
				return 1		
		return 0
		
		
	# remove an object from the Tile
	def removeFrom(self, thing):
		if self.has(thing):
			self.onTile.remove(thing)
		
		
	# remove a type of object from the Tile
	def removeAFrom(self, thingType):
		if self.hasA(thingType):
			count = 0
			for item in self.onTile:
				if item.getType() == thingType and count == 0:
					self.onTile.remove(item)
					count = 1
					break
		



		
# grid
class Grid():

	# init
	# size - number
	# typer - a function to determine the type of the tile (arguments - the position as a list)
	def __init__(self, size, typer):
		self.size = size
		# grid[0] - y axis 
		# grid[1] - x axis
		self.grid = self.create(self.size, typer)
		self.zero = Tile('null', 'null', [])
	
	
	
	# create the grid
	def create(self, size, typer):
		grid = []
		for i in range(0, size):
			for j in range(0, size):
				grid.append(Tile((i, j), typer((i, j)), []))
		
		return grid
		
		
		
	# where is an object	
	def whereIs(self, thing):
		for tile in self.grid:
			if tile.has(thing) > 0:
				return tile
				
		return self.zero
	
	
	
	# move an object
	# by position
	def movePos(self, thing, _from_, _to_):
		if _from_ != _to_:
			for tile in self.grid:
				if tile.getPos() == _from_:
					tile.removeFrom(thing)
				if tile.getPos() == _to_:
					tile.putTo(thing)

				
				
	# move an object
	# by tile number
	def moveNum(self, thing, _from_, _to_):
		if _from_ != _to_:
			self.grid[_from_].removeFrom(thing)
			self.grid[_to_].putTo(thing)
			
	
	
	# move an object to a direction
	# 0 - up
	# 1 - down
	# 2 - right
	# 3 - left
	def moveToDirection(self, thing, _from_, dir):
		# determine destination
		# up
		if dir == 0:
			_to_ = (_from_[0] + 1, _from_[1])
			if _to_[0] >= self.size:
				_to_ = (0, _from_[1])
		# down
		elif dir == 1:
			_to_ = (_from_[0] - 1, _from_[1])
			if _to_[0] < 0:
				_to_ = (self.size - 1, _from_[1])
		# right
		elif dir == 2:
			_to_ = (_from_[0], _from_[1] + 1)
			if _to_[1] >= self.size:
				_to_ = (_from_[0], 0)
		# left
		elif dir == 3:
			_to_ = (_from_[0], _from_[1] - 1)
			if _to_[1] < 0:
				_to_ = (_from_[0], self.size - 1)
		
		# move
		self.movePos(thing, _from_, _to_)
	
	
	
	# remove an	object
	# by position
	def removeFromPos(self, thing, _from_):
		for tile in self.grid:
			if tile.getPos() == _from_ and tile.has(thing) > 0:
				tile.removeFrom(thing)
				
			
			
	# remove an object
	# by tile number
	def removeFromNum(self, thing, _from_):
		if self.grid[_from_].has(thing) > 0:
			self.grid[_from_].removeFrom(thing)
	
	
	
	# remove a type of object
	# by position
	def removeAFromPos(self, thingType, _from_):
		for tile in self.grid:
			if tile.getPos() == _from_ and tile.hasA(thingType) > 0:
				tile.removeAFrom(thingType)
				
				
				
	# remove a type of object
	# by tile number
	def removeAFromNum(self, thingType, _from_):
		if self.grid[_from_].hasA(thingType) > 0:
			self.grid[_from_].removeAFrom(thingType)
	
	
	
	# put an object to a Tile
	# by position
	def putToPos(self, thing, _to_):
		for tile in self.grid:
			if tile.getPos() == _to_:
				tile.putTo(thing)
	
	
	
	# put an object to a Tile
	# by tile number	
	def putToNum(self, thing, _to_):
		self.grid[_to_].putTo(thing)
		
		
		
	# print the grid	
	def printGrid(self):
		print 'the grid:'
		for tile in self.grid:
			print tile.getPos(), tile.getType(), tile.getOnTile()



			
		
# resources
class Resource():

	# init
	def __init__(self, id, value, rate):
		self.id = id
		self.type = 'res'
		self.value = value
		self.rate = rate
	
	
	# get resource id
	def getId(self):
		return self.id
	
	
	# type
	def getType(self):
		return self.type
		
		
	# value
	def getValue(self):
		return self.value
	
			
	# what happens, when consumed
	def consume(self):
		self.value -= 1.0
		if self.value <= 0.0:
			temp = 1.0 + self.value
			self.value = 0.0
			return temp
		else:
			return 1.0
		
		
	# for one round, this happens to the resource
	def tick(self):
		self.value *= self.rate

		
		
		

# consumer entities
class Consumer():

	# init
	# aggression - the rating of attacking other consumers
	# agility - the rating of dodgeing attacks and attacking successfully
	# hunger - the overall hunger
	def __init__(self, id, aggression, reproduction, agility, baseHunger, hungerFunction):
		self.id = id
		self.type = 'con'
		self.aggression = aggression
		self.reproduction = reproduction
		self.agility = agility
		self.hunger = baseHunger
		self.hungerFunction = hungerFunction

	
	# get the id
	def getId(self):
		return self.id
		
	
	# get the type
	def getType(self):
		return self.type

	
	# get agility
	def getAgility(self):
		return self.agility
	
	
	# get aggression
	def getAggression(self):
		return self.aggression
		
	
	# get reproduction rate
	def getReproduction(self):
		return self.reproduction
	
	
	# get actual hunger value
	def getHunger(self):
		return self.hunger
		
		
	# decrease hunger
	def decreaseHunger(self, value):
		self.hunger = max(0.0, self.hunger - value)
		
	
	# what to do in a round
	# environment - the other objects in the tile
	def tick(self, environment):
		# determine action
		decision = self.createPiramid(environment) 
		# increase hunger
		self.hunger = self.hungerFunction(self.hunger)
		
		# send the decision to the evironment
		return decision	
	

	
	# create a need pyramid, then decide based on the created pyramid
	def createPiramid(self, environment):
		# create the piramid with the actual values
		pyramid = {'hun' : self.hunger, 'agg' : self.aggression, 'rep' : self.reproduction}
		
		# get the dominant need
		dominant, domValue = 'hun', self.hunger
		for need, value in pyramid.iteritems():
			if value > domValue:
				dominant = need
				domValue = value
		
		# get the information from the environment
		res = []
		con = []
		for item in environment:
			if item.getType() == 'res':
				res.append(item)
			elif item.getType() == 'con':
				con.append(item)
		
		# if hungry
		if dominant == 'hun':
			# if there's resource, eat
			if len(res) > 0:
				return ('hun', res[0])
			# else move
			else:
				return ('mov', randint(0, 3))
		
		# if aggressive
		elif dominant == 'agg':
			# if there's an another consumer
			if len(con) > 1:
				# find the weakest that is not me
				if con[0].getId() == self.getId():
					weak = con[1]
				else:
					weak = con[0]
				for item in con:
					if item.getId() != self.getId() and item.getAgility() < weak.getAgility():
						weak = item
				# and attack it
				return ('agg', weak)
			# else move
			else:
				return ('mov', randint(0, 3))
		
		# if reproductive
		elif dominant == 'rep':
			# if there's an another consumer
			if len(con) > 1:
				# find the best that is not me
				if con[0].getId() == self.getId():
					best = con[1]
				else:
					best = con[0]
				for item in con:
					if item.getId() != self.getId() and item.getAgility() > best.getAgility():
						best = item
				# and try to reproduce with it
				return ('rep', best)
			# else move
			else:
				return ('mov', randint(0, 3))


				
				

# handles the simulation				
class Simulator():

	# init
	def __init__(self, size, numOfRes, numOfCon, resPopUp, baseHunger, hungerFunction):
		# parameter setup
		self.size = size
		self.numOfRes = numOfRes
		self.numOfCon = numOfCon
		self.resPopUp = resPopUp
		self.baseHunger = baseHunger
		self.hungerFunction = hungerFunction
		
		# world creation
		self.world = Grid(size, self.worldTypeDeterminer)
		self.res = self.generateResources(self.numOfRes)
		self.con = self.generateConsumers(self.numOfCon)
		self.placeAll()
		print 'world created!'
		
		# additional information storing
		self.reproducers = []
		self.round = 0
		self.actionList = []
		
		
	# determine type of the world
	def worldTypeDeterminer(self, pos):
		return random()
		
	
	# generate resources
	def generateResources(self, number):
		res = []
		for i in range(0, number):
			res.append(Resource(i, random() + 1.0, random() * 0.5))
		return res
	
	
	# generate consumers
	def generateConsumers(self, number):
		con = []
		for i in range(0, number):
			con.append(Consumer(i, random(), random(), random(), self.baseHunger, self.hungerFunction))
		return con
	
	
	# place the initial objects to the grid
	def placeAll(self):
		# place all resources and consumers to the world
		for item in self.res:
			self.world.putToNum(item, randint(0, self.size**2 - 1))
		for item in self.con:
			self.world.putToNum(item, randint(0, self.size**2 - 1))
	
	
	# place an object randomly to the grid
	def place(self, thing):
		# place a resource or a consumer to the world
		self.world.putToNum(thing, randint(0, self.size**2 - 1))
	
	
	# get the grid
	def getWorld(self):
		return self.world
	
	
	# get the consumers
	def getConsumers(self):
		return len(self.con)
	
	
	# defines the attack mechanism
	def attack(self, attacker, attacked):
		# if attacker is stronger
		if attacker.getAgility() > attacked.getAgility():
			# remove from world
			self.world.removeFromPos(attacked, self.world.whereIs(attacked).getPos())
			# remove from exsistence
			self.con.remove(attacked)
			# report success
			self.actionList.append('Consumer {0} attacked and killed Consumer {1}!'.format(attacker.getId(), attacked.getId()))
			
		# if attacked is stronger
		elif attacker.getAgility() < attacked.getAgility():
			# remove from world
			self.world.removeFromPos(attacker, self.world.whereIs(attacker).getPos())
			# remove from exsistence
			self.con.remove(attacker)
			# report failure
			self.actionList.append('Consumer {0} attacked Consumer {1} and died!'.format(attacker.getId(), attacked.getId()))
	
	
	# defines consume mechanism
	def consume(self, consumer, consumed):
		# add to the report
		self.actionList.append('Consumer {0} consumed Resource {1}!'.format(consumer.getId(), consumed.getId()))
		# consume the resource, lower the hunger
		consumer.decreaseHunger(consumed.consume())
		# if resource is consumed totally,
		if consumed.getValue() == 0.0:
			# remove from world
			self.world.removeFromPos(consumed, self.world.whereIs(consumed).getPos())
			# remove from exsistence 
			self.res.remove(consumed)
		
		
	# define reproducing	
	def reproduce(self, initiator, target):
		# append the intention to the reproduction list
		self.reproducers.append(sorted([initiator, target]))
		# if there were already an intention to this reproduction
		if self.reproducers.count(sorted([initiator, target])) > 1:
			# remove intensions
			self.reproducers.remove(sorted([initiator, target]))
			self.reproducers.remove(sorted([initiator, target]))
			
			# determine the replicant's values
			# randomly select between
			# 	- mutation - new random value
			#	- crossover - average value
			#	- selection - better value
			#	- deflection - lower value
			aggression = choice([random(), (initiator.getAggression() + target.getAggression()) / 2.0,\
								 max(initiator.getAggression(), target.getAggression()),\
								 min(initiator.getAggression(), target.getAggression())])
			reproduction = choice([random(), (initiator.getReproduction() + target.getReproduction()) / 2.0,\
								 max(initiator.getReproduction(), target.getReproduction()),\
								 min(initiator.getReproduction(), target.getReproduction())])
			agility = choice([random(), (initiator.getAgility() + target.getAgility()) / 2.0,\
								 max(initiator.getAgility(), target.getAgility()),\
								 min(initiator.getAgility(), target.getAgility())])
			# increase the corresponding id
			self.numOfCon += 1
			# create the new consumer with the new attribute values
			temp = Consumer(self.numOfCon, aggression, reproduction, agility, self.baseHunger, self.hungerFunction)
			# add the replicant to consumer list, and place it to the world
			self.con.append(temp)
			self.place(temp)
			# report success
			self.actionList.append('Consumer {0} and Consumer {1} created Consumer {2}!'.format(initiator.getId(), target.getId(), temp.getId()))
		else:
			# report intention
			self.actionList.append('Consumer {0} tried to reproduce with Consumer {1} (ag: {2})!'.format(initiator.getId(), target.getId(), round(target.getAgility(), 2)))
			
		
		
	# defines move mechanism
	def move(self, mover, direction):
		self.world.moveToDirection(mover, self.world.whereIs(mover).getPos(), direction)
		# report success
		self.actionList.append('Consumer {0} moved!'.format(mover.getId()))
	

	# one step of the worlds
	def tick(self):
		# set up round
		self.round += 1
		self.actionList = []
		
		# handle resources
		for item in self.res:
			item.tick()
			# if the resource is out of power, remove it
			if item.getValue() <= 0.0:
				self.world.removeFromPos(item, self.world.whereIs(item).getPos())
				self.res.remove(item)
		# there's a chance for a new resource to pop up
		if random() < self.resPopUp:
			# increase the corresponding id
			self.numOfRes += 1
			# create the new resource
			temp = Resource(self.numOfRes, random() + 1.0, random() * 0.5)
			self.res.append(temp)
			self.place(temp)
			# report success
			self.actionList.append('Resource {0} created!'.format(temp.getId()))
		
		# save actual populations, newborn consumers cannot act
		actPopulation = self.con
		# handle consumers 
		for item in actPopulation:
			# if starved to death, remove it
			if item.getHunger() >= 1.0:
				# report death
				self.actionList.append('Consumer {0} starved to death!'.format(item.getId()))
				# remove from world, and from the consumer list
				self.world.removeFromPos(item, self.world.whereIs(item).getPos())
				self.con.remove(item)
			# else act accordingly
			else:
				# get the decision that the consumer has taken
				todo = item.tick(self.world.whereIs(item).getOnTile())
				# execute
				if todo[0] == 'hun':
					self.consume(item, todo[1])
				elif todo[0] == 'agg':
					self.attack(item, todo[1])
				elif todo[0] == 'mov':
					self.move(item, todo[1])
				elif todo[0] == 'rep':
					self.reproduce(item, todo[1])
		
		# report extreme values
		if len(self.res) == 0:
			self.actionList.append('Out of Resources!')
		if len(self.con) == 0:
			self.actionList.append('Consumers extinct!')
			
	
	# print the collected reports
	def report(self):
		print 'Round ', self.round, ':'
		print '{0} Consumer - {1} Resource'.format(len(self.con), len(self.res))
		for item in self.actionList:
			print item
		

# main function		
if __name__ == '__main__':

	# hunger function for specifing starvation
	def hf(value):
		return value - max(0.1, value * 0.2)
	
	# create simulation	
	# size, resource, consumer, new resource chance, base hunger value, hunger function (hunger value)
	sim = Simulator(5, 10, 10, 0.2, 0.4, hf)
	
	# run it as you like 
	while sim.getConsumers() > 0 and sim.getConsumers() < 100:
		sim.tick()
		#print sim.getConsumers()
		sim.report()
	