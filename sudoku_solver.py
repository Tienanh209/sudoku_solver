import tkinter as tk
from tkinter import messagebox
import random


class SudokuSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.config(bg="lightgrey")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.create_widgets()

    def create_widgets(self):
        # Create the grid of entry boxes with a thicker border around each 3x3 box
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.master, width=2, font=(
                    'Arial', 18), justify='center', borderwidth=2, relief="solid")
                entry.grid(row=i, column=j, padx=(1, 1 if (j + 1) % 3 != 0 else 5),
                           pady=(1, 1 if (i + 1) % 3 != 0 else 5))
                self.entries[i][j] = entry

        # Create Solve button
        solve_button = tk.Button(self.master, text="Solve", command=self.solve_sudoku, font=(
            'Arial', 14), bg="lightblue", fg="black", relief="raised", borderwidth=2)
        solve_button.grid(row=10, column=1, columnspan=3, pady=10)

        # Create Clear button
        clear_button = tk.Button(self.master, text="Clear", command=self.clear_board, font=(
            'Arial', 14), bg="lightcoral", fg="black", relief="raised", borderwidth=2)
        clear_button.grid(row=10, column=5, columnspan=3, pady=10)

        # Create Hint button
        hint_button = tk.Button(self.master, text="Hint", command=self.give_hint, font=(
            'Arial', 14), bg="lightgreen", fg="black", relief="raised", borderwidth=2)
        hint_button.grid(row=11, column=1, columnspan=7, pady=10)

    def solve_sudoku(self):
        # Get values from the entry boxes and fill the grid
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    self.grid[i][j] = int(value)
                else:
                    self.grid[i][j] = 0  # Empty cell

        if self.solve():
            self.update_board()
            messagebox.showinfo("Success", "Sudoku solved successfully!")
        else:
            messagebox.showerror("Error", "No solution exists.")

    def solve(self):
        empty_cell = self.find_empty_location()

        if not empty_cell:
            return True  # Solved

        row, col = empty_cell

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num

                if self.solve():
                    return True

                self.grid[row][col] = 0  # Backtrack

        return False

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row, col, num):
        # Check row and column
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False

        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False

        return True

    def update_board(self):
        """Update the GUI with the solved Sudoku board."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)  # Clear previous value
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(tk.END, str(self.grid[i][j]))
                    # Display solution in blue color
                    self.entries[i][j].config(fg="blue")

    def clear_board(self):
        """Clear the Sudoku board."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(fg="black")  # Reset to default color
                self.grid[i][j] = 0

    def give_hint(self):
        """Provide a hint by filling one empty cell with a correct number."""
        # Save the current grid state
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    self.grid[i][j] = int(value)
                else:
                    self.grid[i][j] = 0  # Empty cell

        # Use solve() to get a solution
        temp_grid = [row[:] for row in self.grid]
        if self.solve():
            empty_cells = [(i, j) for i in range(9)
                           for j in range(9) if self.entries[i][j].get() == '']
            if empty_cells:
                i, j = random.choice(empty_cells)  # Pick a random empty cell
                hint_value = self.grid[i][j]
                self.entries[i][j].insert(0, str(hint_value))
                self.entries[i][j].config(fg="green")  # Hint in green color

            # Restore the original grid state
            self.grid = temp_grid
        else:
            messagebox.showerror("Error", "No solution exists.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
