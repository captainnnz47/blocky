
"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.

    """

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initailize the blob goal """
        Goal.__init__(self, target_colour)

    def score(self, board: Block) -> int:
        """Return the current score for blob goal on the given board.

        The score is always greater than or equal to 0.
        """
        scores = []

        flattened = board.flatten()

        for i in range(len(flattened)):
            for j in range(len(flattened)):
                visited = _make_unvisited(len(flattened))

                scores.append(self._undiscovered_blob_size((i, j), flattened,
                                                           visited))

        return max(scores)

    def description(self) -> str:
        """Return a description of this goal.
        """
        colour = ""
        if self.colour == (1, 128, 181):
            colour = "Pacific Point"
        elif self.colour == (138, 151, 71):
            colour = "Old Olive"
        elif self.colour == (199, 44, 58):
            colour = "Real Red"
        elif self.colour == (255, 211, 92):
            colour = "Daffodil Delight"

        return "create the biggest " + colour + " blob"

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """
        Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        x = pos[0]
        y = pos[1]
        if (x >= len(board)) or (y >= len(board)) or (x < 0) or (y < 0):
            return 0
        elif board[x][y] != self.colour:
            visited[x][y] = 0
            return 0
        else:
            if visited[x][y] == -1:

                if board[x][y] != self.colour:
                    visited[x][y] = 0
                    return 0
                else:
                    size = 0
                    visited[x][y] = 1

                    size += 1
                    size += self._undiscovered_blob_size((x + 1, y), board,
                                                         visited)
                    size += self._undiscovered_blob_size((x - 1, y), board,
                                                         visited)
                    size += self._undiscovered_blob_size((x, y + 1), board,
                                                         visited)
                    size += self._undiscovered_blob_size((x, y - 1), board,
                                                         visited)
                    return size
            else:
                return 0


class PerimeterGoal(Goal):
    """A goal to put the most possible units of the target color on the outer
    perimeter of the board.

    """

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initailize the perimeter goal """
        Goal.__init__(self, target_colour)

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        score = 0
        new_board = board.flatten()
        for j in range(len(new_board)):
            if new_board[j][0] == self.colour:
                score += 1
            if new_board[j][len(new_board) - 1] == self.colour:
                score += 1
            if new_board[0][j] == self.colour:
                score += 1
            if new_board[len(new_board) - 1][j] == self.colour:
                score += 1
        return score

    def description(self) -> str:
        """Return a description of this goal.
        """
        colour = ""
        if self.colour == (1, 128, 181):
            colour = "Pacific Point"
        elif self.colour == (138, 151, 71):
            colour = "Old Olive"
        elif self.colour == (199, 44, 58):
            colour = "Real Red"
        elif self.colour == (255, 211, 92):
            colour = "Daffodil Delight"

        return "create the longest " + colour + "on the outer perimeter on" \
                                                "the board."


def _make_unvisited(size: int) -> List[List[int]]:
    """
    Return a list of lists to indicate all cells haven't been visited yet
    """
    visited = []

    for _ in range(size):
        col = []
        for _ in range(size):
            col.append(-1)
        visited.append(col)
    return visited


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
