import random
import five_letter_words

def check_word(word, selected_word):
    """
    Check word against the selected word.
    Returns a string with symbols:
    '✓' for correct position
    'O' for in word, wrong position
    'X' for not in word
    """
    # Initialize result with ('X')
    result = ['X', 'X', 'X', 'X', 'X']
    
    for i in range(5):
        letter = word[i]
        
        # Check if it's correct position
        if letter == selected_word[i]:
            result[i] = '✓'
            continue
        
        # Check if it's wrong position
        wrong_position = False
        for k in range(5):
            # Check if correct
            if word[i] == selected_word[k] and word[k] == letter:
                wrong_position = True
                break
            if letter == selected_word[k] and k != i and result[k] != '✓':
                result[i] = 'O'
        
        if wrong_position:
            result[i] = 'X'
    
    return ''.join(result)

random_int = random.randint(0, len(five_letter_words.FIVE_LETTER_WORDS) - 1)
word = five_letter_words.FIVE_LETTER_WORDS[random_int].upper()
print(f"Random five-letter word selected\n")

print(word) # For testing purposes; remove or comment out in production

guess_count = 5

for attempts in range(1, guess_count + 1):
    word_guessed = input("Enter your five-letter word guess: ").upper()
    
    # Check input length
    if len(word_guessed) != 5:
        print("Please enter exactly 5 letters.\n")
        continue  
    
    # Get feedback from check_word function
    feedback = check_word(word_guessed, word)
    
    # Display the guess with feedback symbols below
    print("\nGuess:    ", end="")
    for letter in word_guessed:
        print(f"{letter} ", end="")
    print()
    print("Feedback: ", end="")
    for symbol in feedback:
        print(f"{symbol} ", end="")
    print("\n")
    
    # Check if guessed correctly
    if word_guessed == word:
        print(f"Congratulations! You guessed the word '{word}' in {attempts} attempts!")
        break
    elif attempts < guess_count:
        print(f"Attempts remaining: {guess_count - attempts}\n")
else:
    print(f"Sorry, you've used all {guess_count} guesses. The correct word was: {word}")