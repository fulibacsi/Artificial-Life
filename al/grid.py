# encding: utf-8


class Tile(object):
    """Base class for handling the Grid's tiles.

    Parameters:
    -----------
    pos: tuple of ints
        The absolute position in the grid.

    type: object
        The type of the tile - unused at the moment.

    on_tile: list
        The list of objects on the tile.

    Returns:
    --------
    None
    """

    def __init__(self, pos, type, on_tile=None):
        self.pos = pos
        self.type = type
        self.on_tile = on_tile or []

    def put_to(self, thing):
        """Put an object to the Tile.

        Parameters:
        -----------
        thing: object
            The object to add to the Tile.

        Returns:
        --------
        None
        """
        self.on_tile.append(thing)

    def has(self, thing):
        """Returns if the specified object is on the Tile.

        Parameters:
        -----------
        thing: object
            The searched object.

        Returns:
        --------
        count: int
            The number of searched objects on the tile.
        """
        return self.on_tile.count(thing)

    def has_a(self, thing_type):
        """Returns if a type of object is on the Tile.

        Parameters:
        -----------
        thing_type: string
            The type of the object to search for.

        Returns:
        --------
        has: bool
            Returns if at least one objet of the specified type is on the tile.
        """
        return any(item.type == thing_type for item in self.on_tile)

    def remove_from(self, thing):
        """Remove the specified object from the Tile.

        Parameters:
        -----------
        thing: object
            The object to remove.

        Returns:
        --------
        None
        """
        if self.has(thing):
            self.on_tile.remove(thing)

    def remove_a_from(self, thing_type):
        """Remove a type of object from the Tile.

        Parameters:
        -----------
        thing_type: string
            The type of the object to remove.

        Returns:
        --------
        None
        """
        if self.has_a(thing_type):
            for item in self.on_tile:
                if item.type == thing_type:
                    self.on_tile.remove(item)
                    return


class Grid(object):
    """The representation of the artificial environment.

    Parameters:
    -----------
    size: int
        The size of the artificial environment.

    typer: callable
        A function with one parameter (arguments - the position as a list)
        to determine the type of the tile

    Returns:
    --------
    None
    """

    def __init__(self, size, typer):
        # (y, x)
        self.size = size
        self.typer = typer
        self.grid = self.create()
        self.zero = Tile('null', 'null')

    def create(self):
        """Generate the grid.

        Returns:
        --------
        grid: list of Tile objects
            The generated grid.
        """
        return [Tile((i, j), self.typer((i, j)))
                for j in xrange(self.size)
                for i in xrange(self.size)]

    def where_is(self, thing):
        """Returns the position of the specified object.

        Parameters:
        -----------
        thing: object
            The object to search.

        Returns:
        --------
        pos: tuple of ints
            The location of the object. ('null', 'null') if not found.
        """
        for tile in self.grid:
            if tile.has(thing):
                return tile.pos
        return ('null', 'null')

    def on_which_tile(self, thing):
        """Returns the tile object which contains the specified object.

        Parameters:
        -----------
        thing: object
            The object to search.

        Returns:
        --------
        tile: Tile object
            The tile where the searched object reside. The zero tile returned
            if the object is not found.
        """
        for tile in self.grid:
            if tile.has(thing):
                return tile
        return self.zero

    def move_pos(self, thing, start, end):
        """Move an object from a starting position to a destination position.

        Parameters:
        -----------
        thing: object
            The object to move.

        start: tuple of ints
            The starting position.

        end: tuple of ints
            The destination position.

        Returns:
        --------
        end: tuple of ints
            The destination position.
        """
        if start != end:
            for tile in self.grid:
                if tile.pos == start:
                    tile.remove_from(thing)
                if tile.pos == end:
                    tile.put_to(thing)
        return end

    def move_num(self, thing, start, end):
        """Move an object from a starting position to an end position based on
        the Tile indeces.

        Parameters:
        -----------
        thing: object
            The object to move.

        start: int
            The starting Tile's index.

        end: int
            The destination Tile's index.

        Returns:
        --------
        end: int
            The destination Tile's index.
        """
        if start != end:
            self.grid[start].remove_from(thing)
            self.grid[end].put_to(thing)
        return end

    def move_to_dir(self, thing, start, dir):
        """Move an object from a starting position to a direction.

        Parameters:
        -----------
        thing: object
            The object to move.

        start: tuple of ints
            The starting position.

        dir: {0, 1, 2, 3}
            Direction:
                0 - up
                1 - down
                2 - right
                3 - left

        Returns:
        --------
        end: int
            The destination's position.
        """
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

    def remove_from_pos(self, thing, pos):
        """Remove an object from a Tile by Tile position.

        Parameters:
        -----------
        thing: object
            The object to remove.

        pos: tuple of ints
            The target Tile's position.

        Returns:
        --------
        None
        """
        for tile in self.grid:
            if tile.pos == pos and tile.has(thing) > 0:
                tile.remove_from(thing)
                break

    def remove_from_num(self, thing, num):
        """Remove an object from a Tile by Tile index.

        Parameters:
        -----------
        thing: object
            The object to remove.

        num: int
            The target Tile's index.

        Returns:
        --------
        None
        """
        if self.grid[num].has(thing) > 0:
            self.grid[num].remove_from(thing)

    def remove_a_from_pos(self, thing_type, pos):
        """Remove one object of given type from a Tile by Tile position.

        Parameters:
        -----------
        thing_type: string
            The type of the object to remove.

        pos: tuple of ints
            The target Tile's position.

        Returns:
        --------
        None
        """
        for tile in self.grid:
            if tile.pos == pos and tile.has_a(thing_type) > 0:
                tile.remove_a_from(thing_type)
                break

    def remove_a_from_num(self, thing_type, num):
        """Remove one object of given type from a Tile by Tile index.

        Parameters:
        -----------
        thing_type: string
            The type of the object to remove.

        num: int
            The target Tile's index.

        Returns:
        --------
        None
        """
        if self.grid[num].has_a(thing_type) > 0:
            self.grid[num].remove_a_from(thing_type)

    def put_to_pos(self, thing, pos):
        """Insert an object to a Tile of given position.

        Parameters:
        -----------
        thing: object
            The object to insert.

        pos: tuple of ints
            The target Tile's position.

        Returns:
        --------
        None
        """
        for tile in self.grid:
            if tile.pos == pos:
                tile.put_to(thing)
                break

    def put_to_num(self, thing, num):
        """Insert an object to a Tile of given index.

        Parameters:
        -----------
        thing: object
            The object to insert.

        pos: int
            The target Tile's index.

        Returns:
        --------
        None
        """
        self.grid[num].put_to(thing)

    def show(self):
        """Print the grid.

        Returns:
        --------
        None
        """
        print 'the grid:'
        for tile in self.grid:
            print tile.pos, tile.type, tile.on_tile
