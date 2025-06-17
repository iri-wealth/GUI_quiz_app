import tkinter as tk
from tkinter import messagebox
import json


class QuizApp:
    """
    A class to create a GUI-based quiz application using tkinter.
    """

    def __init__(self, root):
        """
        Initializes the Quiz application.

        Args:
            root (tk.Tk): The root window of the tkinter application.
        """
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x500")
        self.root.config(bg="#F2F2F2")

        # Load quiz data from JSON file
        try:
            with open('quiz_questions.json', 'r') as file:
                self.quiz_questions = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "quiz_questions.json not found!")
            self.root.destroy()
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid format in quiz_questions.json!")
            self.root.destroy()
            return

        # Initialize state variables
        self.score = 0
        self.total_questions = len(self.quiz_questions)
        self.current_question_index = 0

        # Create and configure GUI widgets
        self.setup_widgets()

        # Load the first question
        self.load_question()

    def setup_widgets(self):
        """
        Sets up the main widgets for the quiz interface.
        """
        # Question Label
        self.question_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 16, "bold"),
            wraplength=550,
            justify="center",
            pady=20,
            bg="#F2F2F2",
            fg="#333333"
        )
        self.question_label.pack()

        # Frame for answer buttons
        self.alternatives_frame = tk.Frame(self.root, pady=10, bg="#F2F2F2")
        self.alternatives_frame.pack()

        self.alternative_buttons = []
        for i in range(3):  # Assuming 3 alternatives per question
            button = tk.Button(
                self.alternatives_frame,
                text="",
                font=("Arial", 12),
                width=40,
                pady=10,
                bg="#4CAF50",
                fg="white",
                relief="flat",
                command=lambda i=i: self.check_answer(i)
            )
            button.pack(pady=5)
            self.alternative_buttons.append(button)

        # Feedback Label
        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12, "italic"),
            pady=10,
            bg="#F2F2F2"
        )
        self.feedback_label.pack()

        # Score Label
        self.score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            pady=10,
            bg="#F2F2F2",
            fg="#333333"
        )
        self.score_label.pack()

        # Next Question Button
        self.next_button = tk.Button(
            self.root,
            text="Next",
            font=("Arial", 12, "bold"),
            command=self.next_question,
            state="disabled",
            bg="#008CBA",
            fg="white",
            relief="flat",
            padx=20,
            pady=5
        )
        self.next_button.pack(pady=20)

    def load_question(self):
        """
        Loads and displays the current question and its alternatives.
        """
        # Reset feedback and re-enable buttons
        self.feedback_label.config(text="")
        self.next_button.config(state="disabled")
        for btn in self.alternative_buttons:
            btn.config(state="normal", bg="#4CAF50")

        # Load question data
        question_data = self.quiz_questions[self.current_question_index]
        self.question_label.config(text=question_data["question"])

        alternatives = question_data["alternatives"]
        for i, alternative in enumerate(alternatives):
            self.alternative_buttons[i].config(text=alternative)

    def check_answer(self, user_answer):
        """
        Checks if the user's selected answer is correct and updates the score.

        Args:
            user_answer (int): The index of the answer selected by the user.
        """
        # Disable all alternative buttons after an answer is chosen
        for btn in self.alternative_buttons:
            btn.config(state="disabled")

        question_data = self.quiz_questions[self.current_question_index]
        correct_answer_index = question_data["correct_answer"]

        if user_answer == correct_answer_index:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="green")
            self.alternative_buttons[user_answer].config(bg="green")
        else:
            self.score -= 1
            correct_answer_text = question_data["alternatives"][correct_answer_index]
            self.feedback_label.config(text=f"Incorrect! The correct answer was: {correct_answer_text}", fg="red")
            self.alternative_buttons[user_answer].config(bg="red")
            self.alternative_buttons[correct_answer_index].config(bg="lightgreen")  # Highlight correct answer

        # Update score and enable the next button
        self.score_label.config(text=f"Score: {self.score}")
        self.next_button.config(state="normal")

    def next_question(self):
        """
        Moves to the next question or ends the quiz if all questions are answered.
        """
        self.current_question_index += 1
        if self.current_question_index < self.total_questions:
            self.load_question()
        else:
            self.show_final_results()

    def show_final_results(self):
        """
        Displays the final score and a concluding message.
        """
        # Determine the final message
        if self.score == self.total_questions:
            result_message = "Congratulations! You've passed the quiz with a perfect score."
        elif self.score >= self.total_questions // 2:
            result_message = "You've achieved a good score."
        else:
            result_message = "You've failed the quiz. Better luck next time!"

        final_text = f"Quiz Completed!\n\nYour final score is {self.score} out of {self.total_questions}.\n\n{result_message}"

        messagebox.showinfo("Quiz Over", final_text)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
