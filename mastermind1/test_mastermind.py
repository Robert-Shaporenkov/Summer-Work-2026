import unittest
from unittest.mock import patch, call
import mastermind1_game


class TestInputValidation(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input", return_value="1000")
    def test_valid_input_first_try(self, mock_input, mock_print):
        """Test passing a valid number (1000) first"""
        result = mastermind1_game.prompt_validate_input(1)

        self.assertEqual(result, "1000")
        mock_input.assert_called_once()

    @patch("builtins.print")
    def test_empty_then_valid_input(self, mock_print):
        """Test handling when user presses Enter, then a valid input"""
        with patch("builtins.input", side_effect=["", "2000"]):
            result = mastermind1_game.prompt_validate_input(1)

        self.assertEqual(result, "2000")
        mock_print.assert_any_call("Error: input cannot be empty.", end="\n\n")

    @patch("builtins.print")
    def test_not_number_then_valid_input(self, mock_print):
        """Test handling when user enters words before entering a valid number"""
        with patch("builtins.input", side_effect=["hello", "3000"]):
            result = mastermind1_game.prompt_validate_input(1)

        self.assertEqual(result, "3000")
        mock_print.assert_any_call("Error: enter a valid number.", end="\n\n")

    @patch("builtins.print")
    def test_out_of_range_then_valid_input(self, mock_print):
        """Test handling when user types numbers outside 1000-9999 range"""
        with patch("builtins.input", side_effect=["999", "10000", "4000"]):
            result = mastermind1_game.prompt_validate_input(1)

        self.assertEqual(result, "4000")
        mock_print.assert_any_call("Error: number must be between 1000 and 9999.", end="\n\n")

    @patch("builtins.print")
    @patch("builtins.input", return_value="5000")
    def test_num_of_turns_param(self, mock_input, mock_print):
        """Test passing a different number of turns to check that input message changes"""
        mastermind1_game.prompt_validate_input(4)

        mock_input.assert_any_call("Turn 4: Enter a 4-digit number (1000-9999): ")

class TestMainLoop(unittest.TestCase):

    @patch("mastermind1_game.prompt_validate_input")
    @patch("builtins.print")
    @patch("mastermind1_game.code", "1234")
    def test_correct_on_second_try(self, mock_print, mock_prompt):
        """Test when user wins on the second guess"""

        # first guess has 2 correct digits (12), second guess is fully correct
        mock_prompt.side_effect = ["1200", "1234"]

        # call function with initial incorrect guess (5678 != 1234) in order to actually enter the loop
        mastermind1_game.main_loop(user_guess="5678", num_of_turns=1) # 5678 -> 1200 -> 1234 = 1234
        

        # checks that loop ran the expected number of times
        self.assertEqual(mock_prompt.call_count, 2)

        # checks that prompt_validate_input was called with incrementing num_of_turns
        mock_prompt.assert_has_calls([call(1), call(2)])

        # checks that correct print outputs were sent
        expected_prints = [
            call("You got 2 digits right!", end="\n\n"), # printed for "1200"
            call("Well done! The mystery number was 1234. You got it in 2 tries.")
        ]
        mock_print.assert_has_calls(expected_prints)


    @patch("mastermind1_game.prompt_validate_input")
    @patch("builtins.print")
    @patch("mastermind1_game.code", "7788")
    def test_duplicate_digits(self, mock_print, mock_prompt):
        """Test how Counter intersection handles duplicate digits"""

        mock_prompt.side_effect = ["7777", "7877", "7788"]

        mastermind1_game.main_loop(user_guess="7123", num_of_turns=1)

        expected_prints = [
            call("You got 2 digits right!", end="\n\n"),
            call("You got 3 digits right!", end="\n\n"),
            call("Well done! The mystery number was 7788. You got it in 3 tries.")
        ]

        mock_print.assert_has_calls(expected_prints)

if __name__ == "__main__":
    unittest.main()       