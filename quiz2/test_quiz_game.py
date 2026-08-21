import unittest
from unittest.mock import patch, mock_open
import quiz_game


class TestInputValidation(unittest.TestCase):

    @patch("builtins.print") # hides print text from testing window
    @patch("builtins.input", return_value="10")
    def test_valid_input_first_try(self, mock_input, mock_print):
        """Test passing a valid number (10) first"""
        result = quiz_game.prompt_validate_input()

        self.assertEqual(result, 10)
        mock_input.assert_called_once() # checks that function only asked for one input (function only called once)

    @patch("builtins.print")
    def test_empty_then_valid_input(self, mock_print): 
        """Test handling when user presses Enter (empty) before entering a valid number"""
        with patch("builtins.input", side_effect=["", "7"]):
            result = quiz_game.prompt_validate_input()

        self.assertEqual(result, 7)
        # check that presence error message is printed
        mock_print.assert_any_call("Error: input cannot be empty.", end="\n\n")

    @patch("builtins.print")
    def test_not_number_then_valid_input(self, mock_print):
        """Test handling when user enters words before entering a valid number"""
        with patch("builtins.input", side_effect=["hello", "15"]):
            result = quiz_game.prompt_validate_input()

        self.assertEqual(result, 15)
        # check that type error message is printed
        mock_print.assert_any_call("Error: input must be a number.", end="\n\n")

    @patch("builtins.print")
    def test_out_of_range_then_valid_input(self, mock_print):
        """Test handling when user types numbers outside 5-20 range"""
        with patch("builtins.input", side_effect=["4", "21", "12"]):
            result = quiz_game.prompt_validate_input()

        self.assertEqual(result, 12)
        # check that range error message is printed
        mock_print.assert_any_call("Error: input must be between 5 and 20.", end="\n\n")

class TestMoreAdvancedFeatures(unittest.TestCase):

    # mocks file reading (get_rows())
    @patch("builtins.open", new_callable=mock_open, read_data="Q1?A1\nQ2?A2\nQ3?A3\nQ4?A4\nQ5?A5\n")
    @patch("random.sample")
    def test_get_rows(self, mock_sample, mock_file):
        """Checks that get_rows opens quiz.txt, strips empty chars, returns sample"""

        # forces random.sample() to return this list
        mock_sample.return_value = ["Q2?A2", "Q5?A5"]

        result = quiz_game.get_rows(2)

        mock_file.assert_called_once_with("quiz.txt", "r", encoding="utf-8")
        mock_sample.assert_called_once_with(["Q1?A1", "Q2?A2", "Q3?A3", "Q4?A4", "Q5?A5"], 2)
        self.assertEqual(result, ["Q2?A2", "Q5?A5"])

    @patch("builtins.print")
    @patch("time.sleep") # so that tests run without the wait
    @patch("quiz_game.get_rows")
    def test_game_loop_and_maths(self, mock_get_rows, mock_sleep, mock_print):
        """Simulates a whole game loop to check score and % accuracy"""

        # Mock data for 5 questions
        mock_get_rows.return_value = [
            "What is the capital of France?Paris",
            "What is the square root of 64?8",
            "Who wrote 'Romeo and Juliet'?William Shakespeare,Shakespeare",
            "What colour are emeralds?Green",
            "What is the currency of Japan?Yen"
        ]

        simulated_inputs = [
            "5", # choice of question count so first input
            "paris", # q1: correct + case check
            "9", # q2: incorrect
            "shakespeare", # q3: correct + non-primary answer check
            "red", # q4: incorrect
            "yen" # q5: correct
        ]

        with patch("builtins.input", side_effect=simulated_inputs):
            quiz_game.main()

        # check the structure of prints
        mock_print.assert_any_call("--- Welcome to the Quiz! (5 questions) ---\n")
        mock_print.assert_any_call("Correct!\n")
        mock_print.assert_any_call("Incorrect. The right answer was 8.\n")

        # checks maths
        mock_print.assert_any_call("Your score is 3/5!")
        mock_print.assert_any_call("Your accuracy is 60.0%!\n")

    


if __name__ == "__main__":
    unittest.main()