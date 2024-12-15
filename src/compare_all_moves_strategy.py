from itertools import permutations
import time
from src.strategies import Strategy
from src.piece import Piece


class CompareAllMoves(Strategy):

    @staticmethod
    def get_difficulty():
        return "Hard"

    def assess_board(self, colour, myboard):
        pieces = myboard.get_pieces(colour)
        pieces_on_board = len(pieces)
        sum_distances = 0
        number_of_singles = 0
        number_occupied_spaces = 0
        sum_single_distance_away_from_home = 0
        sum_distances_to_endzone = 0
        for piece in pieces:
            sum_distances = sum_distances + piece.spaces_to_home()
            if piece.spaces_to_home() > 6:
                sum_distances_to_endzone += piece.spaces_to_home() - 6
        for location in range(1, 25):
            pieces = myboard.pieces_at(location)
            if len(pieces) != 0 and pieces[0].colour == colour:
                if len(pieces) == 1:
                    number_of_singles = number_of_singles + 1
                    sum_single_distance_away_from_home += 25 - pieces[0].spaces_to_home()
                elif len(pieces) > 1:
                    number_occupied_spaces = number_occupied_spaces + 1
        opponents_taken_pieces = len(myboard.get_taken_pieces(colour.other()))
        opponent_pieces = myboard.get_pieces(colour.other())
        sum_distances_opponent = 0
        for piece in opponent_pieces:
            sum_distances_opponent = sum_distances_opponent + piece.spaces_to_home()
        return {
            'number_occupied_spaces': number_occupied_spaces,
            'opponents_taken_pieces': opponents_taken_pieces,
            'sum_distances': sum_distances,
            'sum_distances_opponent': sum_distances_opponent,
            'number_of_singles': number_of_singles,
            'sum_single_distance_away_from_home': sum_single_distance_away_from_home,
            'pieces_on_board': pieces_on_board,
            'sum_distances_to_endzone': sum_distances_to_endzone,
        }

    def move(self, board, colour, dice_roll, make_move, opponents_activity):

        result = self.move_recursively(board, colour, dice_roll)
        not_a_double = len(dice_roll) == 2
        if not_a_double:
            new_dice_roll = dice_roll.copy()
            new_dice_roll.reverse()
            result_swapped = self.move_recursively(board, colour,
                                                   dice_rolls=new_dice_roll)
            if result_swapped['best_value'] < result['best_value'] and \
                    len(result_swapped['best_moves']) >= len(result['best_moves']):
                result = result_swapped

        if len(result['best_moves']) != 0:
            for move in result['best_moves']:
                make_move(move['piece_at'], move['die_roll'])

    def move_recursively(self, board, colour, dice_rolls):
        best_board_value = float('inf')
        best_pieces_to_move = []

        pieces_to_try = [x.location for x in board.get_pieces(colour)]
        pieces_to_try = list(set(pieces_to_try))

        valid_pieces = []
        for piece_location in pieces_to_try:
            valid_pieces.append(board.get_piece_at(piece_location))
        valid_pieces.sort(key=Piece.spaces_to_home, reverse=True)

        dice_rolls_left = dice_rolls.copy()
        die_roll = dice_rolls_left.pop(0)

        for piece in valid_pieces:
            if board.is_move_possible(piece, die_roll):
                board_copy = board.create_copy()
                new_piece = board_copy.get_piece_at(piece.location)
                board_copy.move_piece(new_piece, die_roll)
                if len(dice_rolls_left) > 0:
                    result = self.move_recursively(board_copy, colour, dice_rolls_left)
                    if len(result['best_moves']) == 0:
                        # we have done the best we can do
                        board_value = self.evaluate_board(board_copy, colour)
                        if board_value < best_board_value and len(best_pieces_to_move) < 2:
                            best_board_value = board_value
                            best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]
                    elif result['best_value'] < best_board_value:
                        new_best_moves_length = len(result['best_moves']) + 1
                        if new_best_moves_length >= len(best_pieces_to_move):
                            best_board_value = result['best_value']
                            move = {'die_roll': die_roll, 'piece_at': piece.location}
                            best_pieces_to_move = [move] + result['best_moves']
                else:
                    board_value = self.evaluate_board(board_copy, colour)
                    if board_value < best_board_value and len(best_pieces_to_move) < 2:
                        best_board_value = board_value
                        best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]

        return {'best_value': best_board_value,
                'best_moves': best_pieces_to_move}


class CompareAllMovesSimple(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


class CompareAllMovesWeightingDistance(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent'])/3 + \
                      2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


class CompareAllMovesWeightingDistanceAndSingles(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent'])/3 + \
                      float(board_stats['sum_single_distance_away_from_home'])/6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


class CompareAllMovesWeightingDistanceAndSinglesWithEndGame(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board']

        return board_value


class CompareAllMovesWeightingDistanceAndSinglesWithEndGame2(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board'] + float(board_stats['sum_distances_to_endzone']) / 6

        return board_value

class CompareAllMovesMinMax(Strategy):

    @staticmethod
    def get_difficulty():
        return "MinMax"

    def __init__(self, depth=3, time_limit=5):
        super().__init__()
        self.MAX_DEPTH = depth
        self.time_limit = time_limit - 0.5
        self.weights = {
            'sum_distances': -0.5,
            'number_of_singles': -3.0,
            'number_of_safe_zones': 2.0,
            'opponents_taken_pieces': 5.0,
            'sum_distances_opponent': 0.5,
        }

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)
        return sum(board_stats[key] * self.weights.get(key, 0) for key in board_stats)

    def assess_board(self, colour, myboard):
        pieces = myboard.get_pieces(colour)
        sum_distances = sum(piece.spaces_to_home() for piece in pieces)
        number_of_singles = sum(1 for loc in range(1, 25) if len(myboard.pieces_at(loc)) == 1)
        number_of_safe_zones = sum(1 for loc in range(1, 25) if len(myboard.pieces_at(loc)) > 1)
        opponents_taken_pieces = len(myboard.get_taken_pieces(colour.other()))
        sum_distances_opponent = sum(piece.spaces_to_home() for piece in myboard.get_pieces(colour.other()))
        return {
            'sum_distances': sum_distances,
            'number_of_singles': number_of_singles,
            'number_of_safe_zones': number_of_safe_zones,
            'opponents_taken_pieces': opponents_taken_pieces,
            'sum_distances_opponent': sum_distances_opponent,
        }

    def move(self, board, colour, dice_rolls, make_move, opponents_activity):
        if board.has_game_ended():
            return

        print(f"AI turn: Colour={colour}, Dice Rolls={dice_rolls}")

        best_score = float('-inf')
        optimal_move = []

        possible_boards_with_moves = self.generate_boards(board, colour, dice_rolls)

        if not possible_boards_with_moves:
            print("No valid moves.")
            return

        start_time = time.time()

        for b, moves in possible_boards_with_moves.items():
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.time_limit:
                print(f"Time limit reached. Using best move so far: {optimal_move}")
                break

            score_for_board_state = self.expectiminimax(b, colour, self.MAX_DEPTH, True, start_time)

            print(f"Evaluated Board Score: {score_for_board_state} for Moves: {moves}")

            if score_for_board_state > best_score:
                best_score = score_for_board_state
                optimal_move = moves

        print(f"AI move: Best Score={best_score}, Moves={optimal_move}")

        if optimal_move:
            for move in optimal_move:
                make_move(move['piece_at'], move['die_roll'])
        else:
            print("No optimal move found.")

    def generate_boards(self, board, colour, dice_rolls):
        if not dice_rolls:
            return {board: []}

        location_of_pieces = list(set(x.location for x in board.get_pieces(colour)))
        player_pieces = [board.get_piece_at(loc) for loc in location_of_pieces]

        resulting_boards = {}

        for dice_order in permutations(dice_rolls):
            die_roll = dice_order[0]
            remaining_die_rolls = dice_order[1:]

            for piece in player_pieces:
                if board.is_move_possible(piece, die_roll):
                    board_copy = board.create_copy()
                    new_piece = board_copy.get_piece_at(piece.location)
                    board_copy.move_piece(new_piece, die_roll)

                    subsequent_boards = self.generate_boards(board_copy, colour, remaining_die_rolls)
                    for new_board, moves in subsequent_boards.items():
                        resulting_boards[new_board] = [{'piece_at': piece.location, 'die_roll': die_roll}] + moves

        return resulting_boards

    def generate_dice_rolls(self):
        dice_rolls = []

        for d1 in range(1, 7):
            for d2 in range(d1, 7):
                probability = 1 / 36 if d1 == d2 else 1 / 18
                dice_rolls.append(((d1, d2), probability))

        return dice_rolls

    def expectiminimax(self, board, colour, depth, is_maximizing_player, start_time):
        elapsed_time = time.time() - start_time
        remaining_time = self.time_limit - elapsed_time

        if remaining_time <= 0 or depth == 0:
            return self.evaluate_board(board, colour)

        all_combinations = self.generate_dice_rolls()
        best_score = float('-inf') if is_maximizing_player else float('inf')

        for (d1, d2), prob in all_combinations:
            possible_boards = self.generate_boards(
                board, colour if is_maximizing_player else colour.other(), [d1, d2]
            )

            for b, _ in possible_boards.items():
                elapsed_time = time.time() - start_time
                if elapsed_time >= self.time_limit:
                    return best_score  # Return the best score computed so far

                score = self.expectiminimax(
                    b, colour, depth - 1, not is_maximizing_player, start_time
                )
                weighted_score = prob * score

                if is_maximizing_player:
                    best_score = max(best_score, weighted_score)
                else:
                    best_score = min(best_score, weighted_score)

        return best_score
