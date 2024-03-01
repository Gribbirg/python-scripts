import os


class SudokuSolver:
    def __init__(self, data_file_path: str = None, size: int = 9, square_size: int = 3):
        self.size = size
        self.square_size = square_size
        if data_file_path is None:
            self.matrix = [[0] * size] * size
            self.candidates_matrix = [[[] for _ in range(size)] for _ in range(size)]
        elif os.path.isfile(data_file_path):
            self.read_from_file(data_file_path)
        else:
            raise FileNotFoundError("File not found")

    def input(self):
        pass

    def read_from_file(self, path):
        self.matrix = []
        self.candidates_matrix = [[[] for _ in range(self.size)] for _ in range(self.size)]
        with open(path, 'r') as file:
            for line in [line.replace("\n", "") for line in file.readlines()]:
                if line != "":
                    self.matrix.append([])
                    for char in line.split(" "):
                        if char.isnumeric():
                            self.matrix[-1].append(int(char))

    def print(self):
        for i in range(self.size):
            if i != 0 and i % self.square_size == 0:
                print()
            for j in range(self.size):
                if j != 0 and j % self.square_size == 0:
                    print(" ", end=" ")
                print(self.matrix[i][j], end="")
                if j != self.size - 1:
                    print(" ", end="")
            print()

    def solve(self):
        self.get_candidates_matrix()
        # for _ in range(100):
        while any([any([element == 0 for element in line]) for line in self.matrix]):
            if self.only_candidate_solve():
                continue
            elif self.place_find_solve():
                continue
            elif self.select_something_solve():
                continue
            else:
                raise Exception("No solution found")

    def get_candidates_matrix(self):
        self.candidates_matrix = [[[] for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 0:
                    candidates = set(k for k in range(1, self.size + 1))
                    impossibles = set()
                    [impossibles.add(x) for x in self.matrix[i] if x != 0]
                    [impossibles.add(self.matrix[x][j]) for x in range(self.size) if self.matrix[x][j] != 0]
                    [impossibles.add(self.matrix[x][y]) for x in
                     range(i - i % self.square_size, i - i % self.square_size + self.square_size) for y in
                     range(j - j % self.square_size, j - j % self.square_size + self.square_size)]
                    candidates = candidates.difference(impossibles)
                    self.candidates_matrix[i][j] = list(candidates)

    def remove_candidates(self, i, j, candidate):
        self.candidates_matrix[i][j] = []
        for x in range(self.size):
            self.candidates_matrix[i][x] = [k for k in self.candidates_matrix[i][x] if k != candidate]
            self.candidates_matrix[x][j] = [k for k in self.candidates_matrix[x][j] if k != candidate]
        for x in range(i - i % self.square_size, i - i % self.square_size + self.square_size):
            for y in range(j - j % self.square_size, j - j % self.square_size + self.square_size):
                self.candidates_matrix[x][y] = [k for k in self.candidates_matrix[x][y] if k != candidate]

    def only_candidate_solve(self):
        for i in range(self.size):
            for j in range(self.size):
                if len(self.candidates_matrix[i][j]) == 1:
                    self.matrix[i][j] = self.candidates_matrix[i][j][0]
                    self.remove_candidates(i, j, self.matrix[i][j])
                    return True
        return False

    def place_find_solve(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                for k in self.candidates_matrix[i][j]:
                    if not any([k in self.candidates_matrix[i][x] for x in range(self.size) if x != j]) or not any(
                            [k in self.candidates_matrix[x][j] for x in range(self.size) if x != i]) or not any(
                        [k in self.candidates_matrix[x][y] for x in
                         range(i - i % self.square_size, i - i % self.square_size + self.square_size) for y in
                         range(j - j % self.square_size, j - j % self.square_size + self.square_size) if
                         x != i or y != j]):
                        self.matrix[i][j] = k
                        self.remove_candidates(i, j, k)
                        return True
        return False

    def select_something_solve(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 0 and len(self.candidates_matrix[i][j]) != 0:
                    self.matrix[i][j] = sorted(self.candidates_matrix[i][j])[0]
                    self.remove_candidates(i, j, self.matrix[i][j])
                    return True
        return False


if __name__ == "__main__":
    sudoku_solver = SudokuSolver("C:\\Users\\gribk\\PycharmProjects\\SudokySolver\\problems\\hard.txt")
    sudoku_solver.print()
    sudoku_solver.solve()
    print("-" * 28)
    sudoku_solver.print()
