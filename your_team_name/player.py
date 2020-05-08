from your_team_name.action import Action
import random

MAX_DEPTH = 1
MOVE_DIRECTIONS = [(0,+1), (+1,0),  (-1,0), (0,-1)]

class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.
        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        self.state = {"black": [[1,0,7], [1,1,7], [1,3,7], [1,4,7], [1,6,7], [1,7,7],
                                [1,0,6], [1,1,6], [1,3,6], [1,4,6], [1,6,6], [1,7,6]],
                      "white": [[1,0,1], [1,1,1], [1,3,1], [1,4,1], [1,6,1], [1,7,1],
                                [1,0,0], [1,1,0], [1,3,0], [1,4,0], [1,6,0], [1,7,0]]}
        #self.state = {"black": [[1,0,6], [1,1,6], [1,3,6], [1,4,6], [1,6,6], [1,7,6]],
        #              "white": [[1,0,1], [1,1,1], [1,3,1], [1,4,1], [1,6,1], [1,7,1]]}
        self.colour = colour
        self.prev_action = None

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        all_actions = all_possible_actions(self.state, self.colour)
        for action in all_actions:
            if action == self.prev_action:
                all_actions.remove(action)
                break

        a = heuristic(self.state)
        print(a)
        #random.shuffle(all_actions)
        #for a in all_actions:
        #    print(a.return_action())
        best_action = None
        if self.colour == "white": #white maximizer
            best_eval = -1000
            for action in all_actions:
                eval_child = alphabeta(action, self.state, 0, "black", -1000, 1000)
                #eval_child = minimax(action, self.state, 0, "black")
                #print(eval_child, " ", action_child.return_action())
                if eval_child > best_eval:
                    best_eval = eval_child
                    best_action = action
            print("\n------BEST EVAL:", best_eval)
            self.prev_action = best_action
            return best_action.return_action()
        else:
            best_eval = 1000
            for action in all_actions:
                eval_child = alphabeta(action, self.state, 0, "white", -1000, 1000)
                #eval_child = minimax(action, self.state, 0, "white")
                #print(eval_child, " ", action_child.return_action())
                if eval_child < best_eval:
                    best_eval = eval_child
                    best_action = action
            self.prev_action = best_action
            print("\n------BEST EVAL:", best_eval)
            return best_action.return_action()



    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.
        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.
        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.
        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
        #self.colour = colour
        action_object = Action.from_tuple(action, colour)
        self.state = action_object.apply_to(self.state)
        return self.state
def heuristic(state):
    dict_black_coord = {(x, y) for _, x, y in state['black']}
    h = 0
    for group in find_explosion_groups(dict_black_coord):
        matrics = distance_grid(group)
        dict_white_coord = {(x, y) for _, x, y in state['white']}
        h += min(matrics[white_coord] for white_coord in dict_white_coord)
    return h

def distance_grid(group):
    """
    Precompute a Manhattan distance landscape for a particular group of
    squares---a dictionary of #steps until within explosive zone.
    """
    radius = around_group(group)
    grid = {}
    for xy in BOARD_SQUARES:
        grid[xy] = min(manhattan_distance(xy, square) for square in radius)
    return grid

def manhattan_distance(xy_a, xy_b):
    """
    Number of steps between two squares allowing only
    up, down, left and right steps.
    """
    x_a, y_a = xy_a
    x_b, y_b = xy_b
    return abs(x_a-x_b) + abs(y_a-y_b)
BOARD_SQUARES = {(x,y) for x in range(8) for y in range(8)}

BOOM_RADIUS = [(-1,+1), (+0,+1), (+1,+1),
               (-1,+0),          (+1,+0),
               (-1,-1), (+0,-1), (+1,-1)]
def around_square(xy):
    """
    Generate the list of squares surrounding a square
    (those affected by a boom action).
    """
    x, y = xy
    for dx, dy in BOOM_RADIUS:
        square = x+dx, y+dy
        if square in BOARD_SQUARES:
            yield square

def around_group(group):
    """The set of squares in explosive range of a set of squares."""
    return set.union(set(group), *[around_square(sq) for sq in group])

def find_explosion_groups(targets):
    """
    Partition a set of targets into groups that will 'boom' together.
    'targets' is a set of coordinate pairs. Return a set of frozensets
    representing the partition.
    """
    # 'up' is a union-find tree-based data structure
    up = {t: t for t in targets}
    # find performs a root lookup with path compression in 'up'
    def find(t):
        if up[t] == t:
            return t
        top = find(up[t])
        up[t] = top
        return top
    # run disjoint set formation algorithm to identify groups
    for t in targets:
        ttop = find(t)
        for u in around_square(t):
            if u in targets:
                utop = find(u)
                if ttop != utop:
                    up[utop] = ttop
    # convert disjoint set trees into Python sets
    groups = {}
    for t in targets:
        top = find(t)
        if top in groups:
            groups[top].add(t)
        else:
            groups[top] = {t}
    # return the partition
    return {frozenset(group) for group in groups.values()}
#def heuristic()

def alphabeta(action, state, current_depth, turn, alpha, beta):
    state = action.apply_to(state)
    if current_depth == MAX_DEPTH or winner(state) != "none":
        return evaluation(state)

    all_actions = all_possible_actions(state, turn)
    #random.shuffle(all_actions)
    if turn == "white":
        for action in all_actions:
            alpha = max(alpha, alphabeta(action, state, current_depth+1, "black", alpha, beta))
            if alpha >= beta:
                break
        return alpha

    else:
        for action in all_actions:
            beta = min(beta, alphabeta(action, state, current_depth+1, "white", alpha, beta))
            if alpha >= beta:
                break
        return beta

def minimax(action, state, current_depth, turn):
    #best_action = None
    state = action.apply_to(state)
    if current_depth == MAX_DEPTH or winner(state) != "none":
        return evaluation(state)
    all_actions = all_possible_actions(state, turn)
    random.shuffle(all_actions)
    if turn == "white": #white maximizer
        best_eval = -1000
        for possible_action in all_actions:
            eval_child = minimax(possible_action, state, current_depth+1, "black")

            if eval_child > best_eval:
                best_eval = eval_child
                #best_action = action
        return best_eval
        #return (best_eval, best_action)

    else: #black minimizer
        best_eval = 1000
        for possible_action in all_actions:
            eval_child = minimax(possible_action, state, current_depth+1, "white")

            if eval_child < best_eval:
                best_eval = eval_child
                #best_action = action
        return best_eval
        #return (best_eval, best_action)

def winner(state):
    if len(state["black"]) == 0 and len(state["white"]) == 0:
        return "both"
    elif len(state["black"]) == 0:
        return "white"
    elif len(state["white"]) == 0:
        return "black"
    else:
        return "none"

def count_members(team):
    count = 0
    for member in team:
        count += member[0]
    return count

def evaluation(state):
    if winner(state) == "white":
        return 100
    if winner(state) == "black":
        return -100
    result = count_members(state["white"]) - count_members(state["black"])
    #for member in state["white"]:
    #    if member[0] > 2:
    #        result = result - 5

    return result - heuristic(state)

def all_possible_actions(state, colour):
    all_actions = []
    all_directions = []
    all_move_actions = []
    factor = 1 if colour == "white" else -1
    for member in state[colour]:
        coord = tuple(member[1:3])
        boom_action = Action("BOOM", None, coord, None, colour)
        if evaluation(boom_action.apply_to(state))*factor > 0:
            all_actions.append(boom_action)

        for n in range(1, 2):
            for step in range(1, member[0]+1):
                for direction in MOVE_DIRECTIONS:
                    move_action = Action.move_from_attributes(n, coord, step, direction, colour)
                    if move_action.is_valid(state):
                        all_move_actions.append(move_action)

    #random.shuffle(all_move_actions)
    all_actions.extend(all_move_actions)
    return all_actions