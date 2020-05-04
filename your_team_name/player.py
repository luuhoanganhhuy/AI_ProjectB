
from your_team_name.action import Action

MAX_DEPTH = 16
MOVE_DIRECTIONS = [(+1,0), (0,+1), (-1,0), (0,-1)]

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
        self.state = {"white": [], "black": []}
        self.colour = colour

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        all_moves = all_moves(state)
        for move in all_moves:
            (best_value, best_action) = minimax(move)
        return return_action(best_action)


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

        return self.state

def minimax(self, action, state, current_depth, is_white):
    current_colour = "white" if is_white else "black"
    if current_depth == MAX_DEPTH || winner(state) != "none":
        return (evaluation(state), state)
    state = action.apply_to(state)
    #white: max
    best_value = -100 if is_white else 100
    best_action = None
    for possible_action in all_possible_actions(state, current_colour):
        (eval_child, action_child) = minimax(possible_action, state, current_depth+1, not is_white)

    if is_colour and best_value < eval_child:
            best_value = eval_child
            best_action = possible_action

        elif (not is_white) and best_value > eval_child:
            best_value = eval_child
            best_action = possible_action
    return (best_value, best_action)

def winner(self, state):
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
        return count_members(state["white"]) - count_members(state["black"])

def all_possible_actions(state, colour):
    all_actions = []
    all_directions = []
    for member in state[colour]:
        coord = tuple(member[1:3])
        for n in range(1, member[0]+1):
            for step in range(1, member[0]+1):
                for direction in MOVE_DIRECTIONS:
                    move_action = Action.move_from_attributes(n, coord, step, direction, colour)
                    if move_action.is_valid():
                        all_actions.append(move_action)
        all_actions.append(Action("BOOM", 1, coord, coord)
