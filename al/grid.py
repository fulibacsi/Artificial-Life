# encding: utf-8

from tile import Tile


# grid
class Grid():

    # init
    # size - number
    # typer - a function to determine the type of the tile
    #         (arguments - the position as a list)
    def __init__(self, size, typer):
        self.size = size
        # grid[0] - y axis
        # grid[1] - x axis
        self.grid = self.create(self.size, typer)
        self.zero = Tile('null', 'null')

    # create the grid
    def create(self, size, typer):
        return [Tile((i, j), typer((i, j)))
                for j in xrange(size)
                for i in xrange(size)]

    # where is an object
    def where_is(self, thing):
        for tile in self.grid:
            if tile.has(thing):
                return tile.pos
        return ('null', 'null')


    def on_which_tile(self, thing):
        for tile in self.grid:
            if tile.has(thing):
                return tile
        return self.zero

    # move an object
    # by position
    def move_pos(self, thing, start, end):
        if start != end:
            for tile in self.grid:
                if tile.pos == start:
                    tile.remove_from(thing)
                if tile.pos == end:
                    tile.put_to(thing)
        return end

    # move an object
    # by tile number
    def move_num(self, thing, start, end):
        if start != end:
            self.grid[start].remove_from(thing)
            self.grid[end].put_to(thing)
        return end


    # move an object to a direction
    # 0 - up
    # 1 - down
    # 2 - right
    # 3 - left
    def move_to_dir(self, thing, start, dir):
        # determine destination
        # up
        if dir == 0:
            end = (start[0] + 1, start[1])
            if end[0] >= self.size:
                end = (0, start[1])
        # down
        elif dir == 1:
            end = (start[0] - 1, start[1])
            if end[0] < 0:
                end = (self.size - 1, start[1])
        # right
        elif dir == 2:
            end = (start[0], start[1] + 1)
            if end[1] >= self.size:
                end = (start[0], 0)
        # left
        elif dir == 3:
            end = (start[0], start[1] - 1)
            if end[1] < 0:
                end = (start[0], self.size - 1)

        # move
        return self.move_pos(thing, start, end)

    # remove an object
    # by position
    def remove_from_pos(self, thing, pos):
        for tile in self.grid:
            if tile.pos == pos and tile.has(thing) > 0:
                tile.remove_from(thing)
                break

    # remove an object
    # by tile number
    def remove_from_num(self, thing, num):
        if self.grid[num].has(thing) > 0:
            self.grid[num].remove_from(thing)

    # remove a type of object
    # by position
    def remove_a_from_pos(self, thing_type, pos):
        for tile in self.grid:
            if tile.pos == pos and tile.has_a(thing_type) > 0:
                tile.remove_a_from(thing_type)
                break

    # remove a type of object
    # by tile number
    def remove_a_from_num(self, thing_type, num):
        if self.grid[num].has_a(thing_type) > 0:
            self.grid[num].remove_a_from(thing_type)

    # put an object to a Tile
    # by position
    def put_to_pos(self, thing, pos):
        for tile in self.grid:
            if tile.pos == pos:
                tile.put_to(thing)
                break

    # put an object to a Tile
    # by tile number
    def put_to_num(self, thing, num):
        self.grid[num].put_to(thing)

    # print the grid
    def show(self):
        print 'the grid:'
        for tile in self.grid:
            print tile.pos, tile.type, tile.on_tile
