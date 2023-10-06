import random

from exceptions import CreateGamePoleException


class Cell:
    """
    Cell model of the playing field.

    Args:
        - **around_mines** - number of mines around current cell;
        - **mine** - boolean value - cell is mine or not.
    """

    is_open: bool

    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        self.around_mines = around_mines
        self.mine = mine
        self.is_open = False


class GamePole:
    """
    Playing field model.

    Args:
        - **field_size** - size of one side of a square playing field;
        - **total_mines** - total number of mines.
    """

    pole: list[list[Cell]]

    def __init__(self, field_size: int, total_mines: int) -> None:
        if field_size < 0 or total_mines < 0:
            raise CreateGamePoleException(
                'the size of tje playing field '
                'or the number of mines can\'t be negative'
            )

        if field_size*field_size <= total_mines:
            raise CreateGamePoleException(
                'the number of mines must be less than '
                'the total number of game cells'
            )

        self.field_size = field_size
        self.total_mines = total_mines
        self.pole = self._create_game_field()

        self._set_mines()
        self._count_mines()

    def _create_game_field(self) -> list[list[Cell]]:
        """Returns a two-demensional list of Cell objects."""
        return [
            [Cell() for _ in range(self.field_size)]
            for _ in range(self.field_size)
        ]

    def _set_mines(self) -> None:
        """Randomly sets the required number of mines."""
        count: int = 0
        n: int = self.field_size - 1
        used: set = set()

        while count < self.total_mines:
            row: int = random.randint(0, n)
            col: int = random.randint(0, n)
            cell = self.pole[row][col]

            if (row, col) not in used:
                used.add((row, col))
                cell.mine = True
                count += 1

    def _count_mines(self) -> None:
        """Counts the number of mines surrounding a cell."""
        n: int = len(self.pole)

        for row in range(n):
            for col in range(n):
                if self.pole[row][col].mine:
                    continue

                self.pole[row][col].around_mines = (
                    self._check_neighbors_mines(row, col)
                )

    def _check_neighbors_mines(self, row: int, col: int) -> int:
        """Check neighboring cells and count the number of mines."""
        mines_counter: int = 0
        n: int = self.field_size - 1

        for r in range(max(0, row - 1), min(n, row + 1) + 1):
            for c in range(max(0, col - 1), min(n, col + 1) + 1):
                if r == row and c == col:
                    continue

                if self.pole[r][c].mine:
                    mines_counter += 1

        return mines_counter

    def show(self) -> None:
        """Show the mineswepper playing field."""
        field: list[str] = []

        for row in self.pole:
            row_str: list[str] = []

            for cell in row:
                if not cell.is_open:
                    row_str.append('#')

                elif cell.is_open and not cell.mine:
                    row_str.append(str(cell.around_mines))

                else:
                    row_str.append('*')

            field.append(' '.join(row_str))

        print('\n'.join(field))
