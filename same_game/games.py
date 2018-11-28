"""Games, or Adversarial Search (Chapter 5)"""

from collections import namedtuple
import random

from same_game.utils import argmax
# from canvas import Canvas

infinity = float('inf')
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

# ______________________________________________________________________________
# Minimax Search


def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minimax_decision:
    return argmax(game.actions(state),
                  key=lambda a: min_value(game.result(state, a)))

# ______________________________________________________________________________


def alphabeta_full_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    evL = lambda state, depth: depth > d
    cutoff_test = (cutoff_test or
                   # (lambda state, depth: depth > d or
                   (evL or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alphabeta_singleplayer_search(state, game):
    """Alpha Beta Search for a single player game, or a two player game where each player
    has their own game board and tries to outscore the other player"""

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alphabeta_singleplayer_depthsearch(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Alpha Beta search adapted for a single player game, or otherwise thought of as
    a two player game where each player has their own game board and tries to outscore the other player.
    This version allows the depth to be specified to set AI difficulty"""

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    evL = lambda state, depth: depth > d
    cutoff_test = (cutoff_test or
                   # (lambda state, depth: depth > d or
                   (evL or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v >= best_score:
            best_score = v
            best_action = a
    return best_action


def maximizing_singleplayer_search(state, game):
    """Adopted from Alpha Beta search for a single player game, or a two player game where each player
    has their own game board and tries to outscore the other player. Searches from root to leaves"""

    # Functions used by alphabeta
    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, max_value(game.result(state, a)))
        return v

    # Body of maximizing search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = max_value(game.result(state, a))
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def maximizing_score_depth_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search adopted from Alpha Beta search. Works for an agent trying to maximize their score in a single player game,
    or a game where the agent is competing against an opponent, but plays on their own game board"""

    # Maximizing function
    def max_value(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, max_value(game.result(state, a), depth + 1))
        return v

    # Body of search:
    evL = lambda state, depth: depth > d
    cutoff_test = (cutoff_test or
                   (evL or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state))
    best_score = -infinity
    best_action = None
    for a in game.actions(state):
        v = max_value(game.result(state, a), 1)
        if v >= best_score:
            best_score = v
            best_action = a
    return best_action


def minimizing_singleplayer_depth_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search adopted from Alpha Beta search. Works for an agent trying to minimize their score in a single player game,
    or a game where the agent is competing against an opponent, but plays on their own game board. Great for
    'easy' level AI opponents."""

    def min_value(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, min_value(game.result(state, a), depth + 1))
        return v

    # Body of minimizing search starts here:
    # The default test cuts off at depth d or at a terminal state
    evL = lambda state, depth: depth > d
    cutoff_test = (cutoff_test or
                   # (lambda state, depth: depth > d or
                   (evL or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state))
    worst_score = infinity
    worst_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), 1)
        if v <= worst_score:
            worst_score = v
            worst_action = a
    return worst_action

# ______________________________________________________________________________
# Players for Games


def query_player(game, state):
    "Make a move by querying standard input."
    move_string = input('Your move? ')
    try:
        move = eval(move_string)
    except NameError:
        move = move_string
    return move


def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.actions(state))


def alphabeta_player(game, state):
    return alphabeta_full_search(state, game)


def alphabeta_singleplayer(game, state):
    return alphabeta_singleplayer_search(state, game)


def alphabeta_singleplayer_depthlimit(game, state, depth):
    return alphabeta_singleplayer_depthsearch(state, game, depth)


def maximizing_singleplayer(game, state):
    return maximizing_singleplayer_search(state, game)


def maximizing_singleplayer_depthlimit(game, state, depth):
    return maximizing_score_depth_search(state, game, depth)


def minimizing_singleplayer_depthlimit(game, state, depth):
    return minimizing_singleplayer_depth_search(state, game, depth)


def play_game(game, *players):
    """Play an n-person, move-alternating game."""

    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.result(state, move)
            if game.terminal_test(state):
                game.display(state)
                return game.utility(state, game.to_move(game.initial))

# ______________________________________________________________________________
# Some Sample Games


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        raise NotImplementedError

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        raise NotImplementedError

    def utility(self, state, player):
        "Return the value of this final state to player."
        raise NotImplementedError

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
