import time
import random


def prompt_validate_input():
    while True:
        user_input = input("How many questions would you like (5-20)? ").strip()

        # presence check
        if not user_input:
            print("Error: input cannot be empty.", end="\n\n")
            continue

        # type check
        try:
            num = int(user_input)

            # range check
            if 5 <= num <= 20:
                print()
                return num

            print("Error: input must be between 5 and 20.", end="\n\n")

            
        except ValueError:
            print("Error: input must be a number.", end="\n\n")

def get_rows(num: int):
    with open("quiz.txt", "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    return random.sample(lines, num)

def main():
    n = prompt_validate_input()

    print(f"--- Welcome to the Quiz! ({n} questions) ---\n")
    print("Any numbers must be entered as numbers, not words\n")

    time.sleep(1)


    score = 0
    rows = get_rows(n)

    for i, row in enumerate(rows, 1):
        # split using the format
        question, answers_raw = row.split("?")
        best_answer = answers_raw.split(",")[0]

        # makes every answer lowercase and splits answers
        answers_list = [answer.strip().lower() for answer in answers_raw.split(",")]

        print(f"Question {i}: {question}?")
        user_answer = input("Your answer: ").strip().lower()

        if user_answer in answers_list:
            print("Correct!\n")
            score += 1
            time.sleep(1)

        else:
            print(f"Incorrect. The right answer was {best_answer}.\n")
            time.sleep(2)
        

    print("--- Quiz Finished! ---\n")
    print(f"Your score is {score}/{n}!")
    print(f"Your accuracy is {(score/n):.1%}!\n")
    
if __name__ == "__main__":
    main()
