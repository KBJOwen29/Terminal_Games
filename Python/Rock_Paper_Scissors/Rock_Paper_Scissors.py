import random as r 

# Choose your weapon
def get_user_choice():
    choices = ['rock', 'paper', 'scissors']
    user_input = input(f"""
(1) Rock
(2) Paper
(3) Scissors
Enter your choice: """)
    print("")
    user_input = user_input.strip().lower()
    if user_input == '1':
        return 'rock'
    elif user_input == '2':
        return 'paper'
    elif user_input == '3':
        return 'scissors'
    else:
        print("Invalid choice. Please try again.")
        return get_user_choice()

# Gets the Computers weapon
def computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return r.choice(choices)

# Compare the weapons of both player
def determine_winner(user, computer):
    if user == computer:
        return "It's a tie!", try_again()
    elif (user == 'rock' and computer == 'scissors') or \
         (user == 'paper' and computer == 'rock') or \
         (user == 'scissors' and computer == 'paper'): 
        return "You win!" , try_again()
    else: 
        return "Computer wins!" , try_again()

# Runs the game
def play_game():
    user = get_user_choice()
    computer = computer_choice()
    print(f"You chose: {user}")
    print("")
    print(f"Computer chose: {computer}")
    print("")
    result = determine_winner(user, computer)
    print(result)

# Ask if you want to play again
def try_again():
    answer = input("Do you want to play again (Y/N)? ")
    if answer == "Y" or answer =="y":
        play_game()
    elif answer == "N" or answer == "n":
        return "Nice Game!"
    else:
        print("Invalid Choice!!")
        try_again()


# Welcomes Player
def main():
    print("Welcome to Rock, Paper, Scissors!")
    play_game()
    
main()
