import random
import itertools


class Actor(object):
    def __init__(self):
        # Mark to avoid moving an actor more than once after tile is processed.
        self.moved_or_created_in_turn = False
        # To not overwrite id.
        self.id_ = None

    def pretty_repr(self):
        return "{}{}".format(self.__class__.__name__.lower(), self.id_)

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__.lower()[0], self.id_)


# Defining these because it's nice to show a representation on the grid that
# uniquely numbers each actor per type.
# One might also argue that a bunch of methods on grid could belong on different
# types of actors. See more about it in the comments in the Grid class.
class Human(Actor):
    # http://stackoverflow.com/questions/1045344/how-do-you-create-an-incremental-id-in-a-python-class
    # Nicer not to expose this to someone using the class.
    _id = itertools.count().next

    def __init__(self):
        super(Human, self).__init__()
        self.human_id = self.id_ = self._id()

# See comments aout Human.
class Zombie(Actor):
    # See comments on _id for Human.
    _id = itertools.count().next

    def __init__(self):
        super(Zombie, self).__init__()
        self.zombie_id = self.id_ = self._id()


class Grid(object):
    def __init__(self, x_tiles, y_tiles):
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles
        # Internal representation of the grid. We should use internal and external
        # representations so that we can still keep track of multiple actors
        # on the same tile internally while not showing individual
        # occupants if two or more are on a the same tile.
        # Otherwise a row would potentially expand on the x-axis far beyond
        # the boundaries of other rows if suddenly a bunch of actors coming
        # from the north or south landed on the same tile. I.e. we would
        # end up with an unclear unaligned grid where rows suddenly expand and
        # contract for some steps.
        self.grid = [[[] for x in range(self.x_tiles)] for x in range(self.y_tiles)]
        self.directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


    def place_actors(self, actor_class):
        # implement specified placements algorithms per actor here.
        pass


    # !! Delete this after implementing place_actors; scaffolding code !!
    def dummy_place(self):
        # Quickly writing a test case
        h0 = Human()
        h1 = Human()
        h2 = Human()
        z0 = Zombie()
        z1 = Zombie()
        self.grid = [[[h0], [h1, h2], []],
                     [[], [], []],
                     [[z0], [], [z1]]]
        return 3, 2

    def _move_to_adjacent_tile(self, direction, actor, cur_x, cur_y):
        if direction == "N":
            if cur_y > 0:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y - 1][cur_x].append(actor)
                print "{} moved North.".format(actor)
                return cur_x, cur_y - 1
            else:
                print "{} tried to move North but bumped into a wall.".format(actor)

        elif direction == "NE":
            if cur_y > 0 and cur_x < len(self.grid[cur_y]) - 1:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y - 1][cur_x + 1].append(actor)
                print "{} moved North-East.".format(actor)
                return cur_x + 1, cur_y - 1
            else:
                print "{} tried to move North-West but bumped into a wall.".format(actor)

        elif direction == "E":
            if cur_x < len(self.grid[cur_y]) - 1:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y][cur_x + 1].append(actor)
                print "{} moved East.".format(actor)
                return cur_x + 1, cur_y
            else:
                print "{} tried to move East bumped into a wall.".format(actor)

        elif direction == "SE":
            if cur_x < len(self.grid[cur_y]) - 1 and cur_y < len(self.grid) - 1:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y + 1][cur_x + 1].append(actor)
                print "{} moved South-East.".format(actor)
                return cur_x + 1, cur_y + 1
            else:
                print "{} tried to move South-East but bumped into a wall.".format(actor)

        elif direction == "S":
            if cur_y < len(self.grid) - 1:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y + 1][cur_x].append(actor)
                print "{} moved South.".format(actor)
                return cur_x, cur_y + 1
            else:
                print "{} tried to move South but bumped into a wall.".format(actor)

        elif direction == "SW":
            if cur_y < len(self.grid) - 1 and cur_x > 0:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y + 1][cur_x - 1].append(actor)
                print "{} moved South-West.".format(actor)
                return cur_x - 1, cur_y + 1
            else:
                print "{} tried to move South-West but bumped into a wall.".format(actor)

        elif direction == "W":
            if cur_x > 0:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y][cur_x - 1].append(actor)
                print "{} moved West.".format(actor)
                return cur_x - 1, cur_y
            else:
                print "{} tried to move West but bumped into a wall.".format(actor)

        elif direction == "NW":
            if cur_y > 0 and cur_x > 0:
                self.grid[cur_y][cur_x].remove(actor)
                self.grid[cur_y - 1][cur_x - 1].append(actor)
                print "{} moved North-West.".format(actor)
                return cur_x - 1, cur_y - 1
            else:
                print "{} tried to move North-West but bumped into a wall.".format(actor)

        if actor.__class__ == Zombie:
            self._let_zombie_bite_non_zombies_on_tile(actor, cur_x, cur_y)

        return cur_x, cur_y


    # One might argue to move this method to a Zombie class as the zombie is
    # the actor. However, this method also alters humans on the grid.
    # Wouldn't be a drama to put in the Zombie class.
    def _let_zombie_bite_non_zombies_on_tile(self, zombie, cur_x, cur_y):
        tile = self.grid[cur_y][cur_x]
        for actor in tile:
            if actor.__class__ != Zombie:
                tile.remove(actor)
                new_zombie = Zombie()
                tile.append(new_zombie)
                print ("{0} was bitten by {1} and turned into {2}, "
                    "yikes!").format(actor, zombie, new_zombie)
                # To prevent new zombies from moving on the turn they
                # were created.
                actor.moved_or_created_in_turn = False



    # This function works by handling subsequently tile per tile, actor per actor and
    # lastly pace per pace based on the initial positions of the actors
    # for each turn.
    #
    # It is arguably the most complex one and should be prioritised to write
    # tests for as to increase trust that it works correctly for different cases
    # as well as it might reveal opportunity for refactoring as to make it
    # easier to digest.
    def move_actors(self, actor_class, paces):
        """
        Move all actors of a particular class for some number of paces.

        Returns a count of number of actors moved.

        The way it's set up assumes a zombie will continue to walk if he still
        has a number of paces left after killing all humans on the grid he passes.
        """
        for yi, outer in enumerate(self.grid):
            for xi, inner in enumerate(outer):
                #print "xi: {}, yi: {}".format(xi, yi)

                i = 0
                actors_in_tile_to_process = True
                # This processess all actors to move by their initial position
                # on a tile per turn.
                while actors_in_tile_to_process:
                    # To prevent index calls when a tile is empty.
                    tile = self.grid[yi][xi]
                    if len(tile) == 0:
                        # Essentially same as break:
                        actors_in_tile_to_process = False
                        continue

                    actor = tile[i]

                    if actor.__class__ == actor_class:
                        if not actor.moved_or_created_in_turn:
                            # Remember position before actor did any paces.
                            xi_init = xi
                            yi_init = yi
                            for pace in range(paces):
                                # This is a human movement implementation,
                                # need to handle zombie movement properly!!!
                                direction = random.choice(self.directions)
                                xi, yi = self._move_to_adjacent_tile(direction, actor, xi, yi)
                                print self.grid
                                print ""

                            # Mark actor so that in case he moved to a tile
                            # that we still need to process we don't move them
                            # subsequently again.
                            actor.moved_or_created_in_turn = True
                            # Continue processing next actor based on initial
                            # position.
                            xi = xi_init
                            yi = yi_init

                    tile = self.grid[yi][xi]
                    if i < len(tile) - 1:
                        i += 1
                    else:
                        actors_in_tile_to_process = False

        actors = 0
        # Reset marks for all actors of the given actor_class.
        for yi, outer in enumerate(self.grid):
            for xi, inner in enumerate(outer):
                for actor in inner:
                    if actor.__class__ == actor_class:
                        # This thus also includes newly created zombies if the
                        # actor is a zombie
                        actors += 1
                        actor.moved_or_created_in_turn = False

        return actors


    # Temporary external representation of the grid.
    # Should be implemented such that multiple actors on same tile are
    # represented by a single symbol. E.g. could use a symbol that represents
    # one or more zombies biting humans on tile if at least one zombie and human
    # are on the same tile.
    # Why limit representation to a single symbol? See comment where grid is
    # created (__init__ method).
    def __repr__(self):
        st = ""
        for row in self.grid:
            st += str(row) + "\n"
        return st


class Game(object):
    def __init__(self):
        # Currently overwritten by dummy_place!!
        self.grid = Grid(40, 20)

    def run(self):
        # Use place_actors once implemented instead to get humans and zombies.
        humans, zombies = self.grid.dummy_place()
        # Commented out because we haven't properly defined 'place_actors'.
        # H = 60, in problem descr.
        #humans = self.grid.place_actors(Human, 60)
        # Z = 3, in problem descr.
        #zombies = self.grid.place_actors(Zombie, 3)

        turns = 0
        while humans:
            # Turns start counting turns from 1.
            turns += 1
            humans = self.grid.move_actors(Human, 3)
            zombies = self.grid.move_actors(Zombie, 3)
        print "Game over! No humans left on turn {}!".format(turns)


if __name__ == "__main__":
    game = Game()
    game.run()
