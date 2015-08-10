# encoding: utf-8

class Tile():

    def __init__(self, pos, type, on_tile=[]):
        self.pos = pos
        self.type = type
        self.on_tile = on_tile

    # put an object to the Tile
    def put_to(self, thing):
        self.on_tile.append(thing)

    # object is on the Tile
    def has(self, thing):
        return self.on_tile.count(thing)

    # a type of object is on the Tile
    def has_a(self, thing_type):
        return any(item.type == thing_type for item in self.on_tile)

    # remove an object from the Tile
    def remove_from(self, thing):
        if self.has(thing):
            self.on_tile.remove(thing)

    # remove a type of object from the Tile
    def remove_a_from(self, thing_type):
        if self.has_a(thing_type):
            for item in self.on_tile:
                if item.type == thing_type:
                    self.on_tile.remove(item)
                    return
