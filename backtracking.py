import time

class GridSudoku:
    def __init__(self, filename):
        self.fullList = list(range(1,10))
        self.grid = self.load_from_file(filename)
        self.grid_initial = self.load_from_file(filename)
    
    def load_from_file(self, filename):
        grid = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    row = [int(ch) if ch.isdigit() else 0 for ch in line]
                    grid.append(row)
        return grid
    

    ######################## validation ##########################

    def _no_duplicates(self, seq):
        vals = [n for n in seq if n != 0]
        return len(vals) == len(set(vals))

    def _is_all_column_valid(self):
        for column in zip(*self.grid):
            if not self._no_duplicates(column):
                return False
        return True 

    def _is_all_line_valid(self):
        for line in self.grid:
            if not self._no_duplicates(line):
                return False
        return True

    def _is_all_square_valid(self):
        for line in [0,3,6]:
            for col in [0,3,6]:
                square = self.grid[line][col:col+3]+self.grid[line+1][col:col+3]+self.grid[line+2][col:col+3]
                if not self._no_duplicates(square):
                    return False
        return True

    def _is_valid_so_far(self):
        return (self._is_all_line_valid() and 
        self._is_all_column_valid() and 
        self._is_all_square_valid())

    ######################## end validation ########################

    ######################### getting lists ########################

    def _get_line_value(self, line):
        return [cell for cell in self.grid[line] if cell != 0]

    def _get_col_value(self, col):
        revertGrid = list(zip(*self.grid))
        return [cell for cell in revertGrid[col] if cell != 0]

    def _get_square_value(self, line, col):
        sLine = (line//3) *3
        sCol = (col//3) *3
        return (self.grid[sLine][sCol:sCol+3] + self.grid[sLine+1][sCol:sCol+3] + self.grid[sLine+2][sCol:sCol+3])

    def _get_candidates(self):

        def sort_by_remaining_values(cell):
            return len(cell["possible_values"])
        
        listCellWithCandidats = []
        for line in range(9):
            for col in range(9):
                if self.grid[line][col] != 0:
                    continue
                listLine = self._get_line_value(line)
                listCol = self._get_col_value(col)
                listSquare = self._get_square_value(line,col)
                result = [x for x in self.fullList if x not in listCol and x not in listLine and x not in listSquare]
                listCellWithCandidats.append({
                    "candidate": [line,col],
                    "possible_values": result
                    })
        listCellWithCandidats.sort(key=sort_by_remaining_values)
        return listCellWithCandidats

    ####################### end getting lists ######################

    def _is_complete(self):
        for line in self.grid:
            for cell in line:
                if cell == 0:
                    return False
        return True

    def diddsplay(self):
        for row in self.grid:
            print(' '.join(str(num) for num in row))

    def display(self):
        gridDisplayed = []
        for line in range(1,9):
            for col in range(1,9):
                value = str(self.grid[line][col])
                if self.grid[line][col] != self.grid_initial[line][col]:
                    value = f"\033[1m\033[31m{value}\033[0m"
                gridDisplayed.append(value)
            gridDisplayed.append("\n")
        print(' '+' '.join(gridDisplayed))

    def solve(self):

        if not self._is_valid_so_far():
            return False

        if self._is_complete():
            return True

        candidates = self._get_candidates()
        if not candidates:
            return False
        
        line, col = candidates[0]["candidate"]
        possible_values = candidates[0]["possible_values"]


        for value in possible_values:

            self.grid[line][col] = value
            print(f"Assignation: cell ({line}, {col}) with {value}")

            if self.solve():
                return True
                
            print(f"Backtracking on: cell ({line}, {col}) (cancelation of {value})")
            self.grid[line][col] = 0
        
        return False
