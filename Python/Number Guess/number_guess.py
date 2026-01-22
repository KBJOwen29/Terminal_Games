import random as r
def check_guess(guess, secret_number):
    if guess > secret_number:
        return("Guess to High: Try a Lower Guess")
    elif guess < secret_number:
        return("Guess to Low: Try a Higher Guess")
    elif guess == secret_number:
        return("You Guessed it correctly")
    else:
        return("Invalid Input")

def main():
    
    guess_count = 0
    
    secret_number = r.randint(1, 100)

    while True:
        guess = int(input("Your Guess: "))
        guess_count += 1
        print(guess_count)
        
        feedback = check_guess(guess, secret_number)
        print(feedback)
        
        if feedback == "You Guessed it correctly":
            print("Number of Guesses: ", guess_count)
            break
        
main()