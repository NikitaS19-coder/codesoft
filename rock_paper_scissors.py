import random

# Score tracking
user_score = 0
computer_score = 0

while True:
    # User Input
    user_choice = input("Choose rock, paper, or scissors: ").lower()
    while user_choice not in ["rock", "paper", "scissors"]:
        print("Invalid choice! Please choose rock, paper, or scissors.")
        user_choice = input("Choose rock, paper, or scissors: ").lower()

    # Computer Selection
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)

    # Display Choices
    print(f"\nYou chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")

    # Determine Winner
    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        result = "You win!"
        user_score += 1
    else:
        result = "You lose!"
        computer_score += 1

    # Display Result
    print(result)
    print(f"Score: You {user_score} - {computer_score} Computer\n")

    # Play Again?
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        print("Thanks for playing!")
        break
