from chess import pgn, Move, Square, square_name
from io import StringIO
from enum import Enum
from datetime import time
import re

def parse_pgn(pgn_string: str, fen_string: str = "") -> list[Move]:
    pgn_io = StringIO(pgn_string)
    game = pgn.read_game(pgn_io)
    
    if game is None:
        return []

    if fen_string:
        game.setup(fen_string)

    return [move for move in game.mainline_moves()]

def list_moves(moves: list[Move]) -> list[str]:
    def concat_squares(from_square: Square, to_square: Square) -> str:
        return square_name(from_square) + "-" + square_name(to_square)
    
    return [
        concat_squares(move.from_square, move.to_square)
        for move in moves
    ]

def replay_game(moves: list[Move], fen: str = ""):
    ...

#====================

class Figure(Enum):
    King    = "K"
    Queen   = "Q"
    Rook    = "R"
    Bishop  = "B"
    Knight  = "N"
    Pawn    = "P"

class Position:
    position: tuple[str, int]

class GameMove:
    index: int
    white: tuple[Figure, Position]
    black: tuple[Figure, Position]
    white_clock: time
    black_clock: time

    def __init__(self, move: str) -> None:
        pattern = r"(\d)\. (\w+\d) ({\[%clk .*\]}) \d\.\.\. (\w+\d) ({\[%clk .*\]})"
        match = re.search(move, pattern)
        if match is None:
            raise ValueError
        
        self.index = int(match.group(1))
        ...

def parse_moves():
    pattern = r"(\d)\. (\w+\d) ({\[%clk .*\]}) \d\.\.\. (\w+\d) ({\[%clk .*\]})"
    
    
    text: str = "aaaaa aaaa"
    text.split()

pieces_positions: dict[Figure, Position] = {}

