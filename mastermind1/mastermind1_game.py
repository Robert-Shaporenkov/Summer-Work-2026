from random import randint


code = str(randint(1000, 9999))
user_guess = "-1"
num_of_turns = 1

def prompt_validate_input(num_of_turns):
    while True:
        user_input_str = input(f"Turn {num_of_turns}: Enter a 4-digit number (1000-9999): ").strip()

        # presence check
        if not user_input_str:
            print("Error: input cannot be empty.", end="\n\n")
            continue

        # type check
        try:
            user_input_int = int(user_input_str)

            # range check
            if 1000 <= user_input_int <= 9999:
                return user_input_str # return the string to create a Counter
            print("Error: number must be between 1000 and 9999.", end="\n\n")

        except ValueError:
            print("Error: enter a valid number.", end="\n\n")

def main_loop(user_guess, num_of_turns):

    while True:
        user_guess = prompt_validate_input(num_of_turns)

        if user_guess == code:
            break

        code_list = list(code)
        shared_digits_count = 0
        for digit in user_guess:
            if digit in code_list:
                shared_digits_count += 1
                code_list.remove(digit)

        print(f"You got {shared_digits_count} digits right!", end="\n\n")
        num_of_turns += 1

    print(f"Well done! The mystery number was {code}. You got it in {num_of_turns} tries.")

if __name__ == "__main__":
    main_loop(user_guess, num_of_turns)
