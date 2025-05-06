from backtracking import GridSudoku
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <chemin_du_fichier_sudoku>")
        return
    
    filename = sys.argv[1]

    sudoku = GridSudoku(filename)

    print("Initial Grid :")
    sudoku.display()

    if sudoku.solve():
        print("\nSolved Grid :")
        sudoku.display()
    else:
        print("No solution.")

if __name__ == "__main__":
    main()