import tkinter as tk
from tkinter import ttk


class PuzzleGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("15 Puzzle with Functions")

        # Initialize puzzle states
        self.initial_board = [
            [7, 11, 8, 15],
            [9, 10, 6, 0],
            [2, 5, 4, 12],
            [13, 3, 1, 14]
        ]

        self.goal_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]

        # Initialize current state
        self.puzzle_array = [row[:] for row in self.initial_board]
        self.current_number = 1

        # Initialize position dictionaries
        self.number_positions = self.get_number_positions()
        self.goal_positions = {
            1: (0, 0), 2: (0, 1), 5: (1, 0),
            6: (1, 1), 9: (2, 0), 13: (3, 0)
        }

    # Create main frame and continue with GUI setup...
        self.button_dict = {}  # Will store 'btnRxCy': button_object pairs

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create puzzle frame (4x4 grid)
        self.puzzle_frame = ttk.Frame(self.main_frame)
        self.puzzle_frame.grid(row=0, column=0, rowspan=1, padx=(0, 10))

        # Create puzzle buttons (4x4 grid) with numbers
        self.puzzle_buttons = []
        for i in range(4):
            for j in range(4):
                value = self.puzzle_array[i][j]
                text = str(value) if value != 0 else ""
                button = tk.Button(self.puzzle_frame, text=text, width=4, height=2,
                                   font=('Arial', 36),
                                   command=lambda r=i, c=j: self.puzzle_button_click(r, c))
                button.grid(row=i, column=j, padx=1, pady=1)
                button.configure(width=4, height=2)

                # Store all buttons with RxCy format, even the space
                btn_name = f"btn_R{i}C{j}"
                self.button_dict[btn_name] = button
                self.puzzle_buttons.append(button)

        # Create text box below puzzle
        self.info_text = tk.Text(self.main_frame, height=10, width=16,
                                 wrap=tk.WORD, font=('Arial', 10))
        self.info_text.grid(row=1, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=10)

        # Add scrollbar to text box
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL,
                                  command=self.info_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), pady=10)
        self.info_text['yscrollcommand'] = scrollbar.set

        # Create function buttons frame
        self.function_frame = ttk.Frame(self.main_frame)
        self.function_frame.grid(row=0, column=1, sticky=tk.N)

        # Create paired button frames
        self.create_paired_buttons()

        # Create remaining function buttons
        self.create_function_buttons()

    def create_paired_buttons(self):
        # Frame for New Puzzle and Propose Move
        pair1_frame = ttk.Frame(self.function_frame)
        pair1_frame.grid(row=0, column=0, pady=1)

        tk.Button(pair1_frame, text="New puzzle", font=('Arial', 12),
                  width=16, height=1, command=self.new_puzzle).grid(row=0, column=0, padx=1)
        tk.Button(pair1_frame, text="Propose move", font=('Arial', 12),
                  width=16, height=1, command=self.propose_move).grid(row=0, column=1, padx=1)

        # Frame for Accept Move and Reject Move
        pair2_frame = ttk.Frame(self.function_frame)
        pair2_frame.grid(row=1, column=0, pady=1)

        tk.Button(pair2_frame, text="Accept move", font=('Arial', 12),
                  width=16, height=1, command=self.accept_move).grid(row=0, column=0, padx=1)
        tk.Button(pair2_frame, text="Reject move", font=('Arial', 12),
                  width=16, height=1, command=self.reject_move).grid(row=0, column=1, padx=1)

        pair3_frame = ttk.Frame(self.function_frame)
        pair3_frame.grid(row=9, column=0, pady=1)

        tk.Button(pair3_frame, text="Move space", font=('Arial', 12),
                  width=16, height=1, command=self.move_space).grid(row=0, column=0, padx=1)
        tk.Button(pair3_frame, text="Reject move", font=('Arial', 12),
                  width=16, height=1, command=self.reject_move).grid(row=0, column=1, padx=1)

    def create_function_buttons(self):
        # Single wide buttons
        functions = [
            ("Select number", self.select_number),
            ("Set number goal location", self.set_number_goal),
            ("Set number target location", self.set_number_target),
            ("Set space target location", self.set_space_target),
            ("Set number move direction", self.set_number_direction),
            ("Set space move direction", self.set_space_direction)
        ]

        for idx, (text, command) in enumerate(functions):
            button = tk.Button(self.function_frame, text=text,
                               font=('Arial', 12), width=32, height=1,
                               command=command)
            button.grid(row=idx+2, column=0, pady=1)

    def move_space(self):
        self.move_space_active = True
        self.info_text.insert(
            tk.END, "Move Space mode activated - click a number adjacent to space\n")
        self.info_text.see(tk.END)

    # def puzzle_button_click(self, row, col):
    #     msg = f"118 Clicked button in , {row}, {col}\n"
        # self.info_text.insert(tk.END, msg)

    def puzzle_button_click(self, row, col):
        msg = f"118 Clicked button in , {row}, {col}\n"
        self.info_text.insert(tk.END, msg)
        if hasattr(self, 'move_space_active') and self.move_space_active:
            # Find current space position
            space_row, space_col = None, None
            for i in range(4):
                for j in range(4):
                    if self.puzzle_array[i][j] == 0:
                        space_row, space_col = i, j
                        break

            # Check if clicked button is adjacent to space
            is_adjacent = (
                (abs(row - space_row) == 1 and col == space_col) or
                (abs(col - space_col) == 1 and row == space_row)
            )

            if is_adjacent:
                # Get the number being moved
                number = self.puzzle_array[row][col]
                # print("141 number", number, row, col)

                # Swap values in puzzle array
                self.puzzle_array[space_row][space_col] = number
                self.puzzle_array[row][col] = 0

                # Update button texts using correct button IDs
                clicked_button_id = f"btn_R{row}C{col}"
                space_button_id = f"btn_R{space_row}C{space_col}"

                # Move number to where space was
                self.button_dict[space_button_id].config(text=str(number))
                # Clear the clicked button (new space location)
                self.button_dict[clicked_button_id].config(text="")

                # Print message
                self.info_text.insert(tk.END,
                                      f"Space moved from ({space_row}, {space_col}) to ({row}, {col})\n")
                self.info_text.see(tk.END)
            else:
                self.info_text.insert(tk.END,
                                      "Invalid move: Selected number must be adjacent to space\n")
                self.info_text.see(tk.END)

            # Reset move_space_active
            self.move_space_active = False

        else:
            # Original button click behavior
            if self.puzzle_array[row][col] != 0:
                button_id = f"btn_R{row}C{col}"
            else:
                button_id = "btn_Space"
            self.info_text.insert(tk.END, f"Clicked {button_id}\n")
            self.info_text.see(tk.END)

    # Dummy functions for control buttons

    def get_number_positions(self):
        """Create dictionary of current number positions"""
        positions = {}
        for i in range(4):
            for j in range(4):
                num = self.puzzle_array[i][j]
                positions[num] = (i, j)
        return positions

    def initialize_board(self):
        """Reset the board to initial state and update GUI"""
        # Reset puzzle array to initial board
        self.puzzle_array = [row[:] for row in self.initial_board]

        # Reset current number
        self.current_number = 1

        # Update number positions
        self.number_positions = self.get_number_positions()

        # Update GUI buttons
        for i in range(4):
            for j in range(4):
                value = self.puzzle_array[i][j]
                button_id = f"btn_R{i}C{j}"
                if value != 0:
                    self.button_dict[button_id].config(text=str(value))
                else:
                    self.button_dict[button_id].config(text="")

        # Log initialization
        self.info_text.insert(
            tk.END, "Board initialized to starting position\n")
        self.info_text.see(tk.END)

    def find_position(self, board, number):
        """Find position of a number in given board"""
        for i in range(4):
            for j in range(4):
                if board[i][j] == number:
                    return (i, j)
        return None

# Modify the New Puzzle button command to use initialize_board

    def create_paired_buttons(self):
        # Frame for New Puzzle and Propose Move
        pair1_frame = ttk.Frame(self.function_frame)
        pair1_frame.grid(row=0, column=0, pady=1)

        tk.Button(pair1_frame, text="New puzzle", font=('Arial', 12),
                  width=16, height=1, command=self.initialize_board).grid(row=0, column=0, padx=1)
        tk.Button(pair1_frame, text="Propose move", font=('Arial', 12),
                  width=16, height=1, command=self.propose_move).grid(row=0, column=1, padx=1)

        # Frame for Accept Move and Reject Move
        pair2_frame = ttk.Frame(self.function_frame)
        pair2_frame.grid(row=1, column=0, pady=1)

        tk.Button(pair2_frame, text="Accept move", font=('Arial', 12),
                  width=16, height=1, command=self.accept_move).grid(row=0, column=0, padx=1)
        tk.Button(pair2_frame, text="Reject move", font=('Arial', 12),
                  width=16, height=1, command=self.reject_move).grid(row=0, column=1, padx=1)

        pair3_frame = ttk.Frame(self.function_frame)
        pair3_frame.grid(row=9, column=0, pady=1)

        tk.Button(pair3_frame, text="Move space", font=('Arial', 12),
                  width=16, height=1, command=self.move_space).grid(row=0, column=0, padx=1)
        tk.Button(pair3_frame, text="Reject move", font=('Arial', 12),
                  width=16, height=1, command=self.reject_move).grid(row=0, column=1, padx=1)

    def new_puzzle(self):
        self.info_text.insert(tk.END, "New Puzzle requested\n")
        self.info_text.see(tk.END)

    def propose_move(self):
        self.info_text.insert(tk.END, "Move proposed\n")
        self.info_text.see(tk.END)

    def accept_move(self):
        self.info_text.insert(tk.END, "Move accepted\n")
        self.info_text.see(tk.END)

    def reject_move(self):
        self.info_text.insert(tk.END, "Move rejected\n")
        self.info_text.see(tk.END)

    def select_number(self):
        self.info_text.insert(tk.END, "Number selection mode\n")
        self.info_text.see(tk.END)

    def set_number_goal(self):
        self.info_text.insert(tk.END, "Setting number goal location\n")
        self.info_text.see(tk.END)

    def set_number_target(self):
        self.info_text.insert(tk.END, "Setting number target location\n")
        self.info_text.see(tk.END)

    def set_space_target(self):
        self.info_text.insert(tk.END, "Setting space target location\n")
        self.info_text.see(tk.END)

    def set_number_direction(self):
        self.info_text.insert(tk.END, "Setting number move direction\n")
        self.info_text.see(tk.END)

    def set_space_direction(self):
        self.info_text.insert(tk.END, "Setting space move direction\n")
        self.info_text.see(tk.END)


def main():
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
