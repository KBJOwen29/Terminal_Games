import random as r 

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

def computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return r.choice(choices)

def determine_winner(user, computer):
    if user == computer:
        return "It's a tie!"
    elif (user == 'rock' and computer == 'scissors') or \
         (user == 'paper' and computer == 'rock') or \
         (user == 'scissors' and computer == 'paper'): 
        return "You win!"
    else: 
        return "Computer wins!"

def play_game():
    print("Welcome to Rock, Paper, Scissors!")
    user = get_user_choice()
    computer = computer_choice()
    print(f"You chose: {user}")
    print("")
    print(f"Computer chose: {computer}")
    print("")
    result = determine_winner(user, computer)
    print(result)
    
play_game()
