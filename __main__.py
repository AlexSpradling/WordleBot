import math
import random
from prompt_toolkit import HTML, PromptSession, print_formatted_text

banner =  """
---------------------------------------------------
 __      __                   .___.__            
/  \    /  \ ____ _______   __| _/|  |    ____   
\   \/\/   //  _ \\_  __ \ / __ | |  |  _/ __ \  
 \        /(  <_> )|  | \// /_/ | |  |__\  ___/  
  \__/\  /  \____/ |__|   \____ | |____/ \___ > 
       \/                      \/            \/  
                                                 
            __________          __               
            \______   \  ____ _/  |_             
             |    |  _/ /  _ \\   __\            
             |    |   \(  <_> )|  |              
             |______  / \____/ |__|              
                    \/                 
---------------------------------------------------
"""

# Other functions (calculate_entropy, get_neess, update_word_list) remain the same


def load_word_list_from_js(file_path):
    """
    Load the word list from a JavaScript file containing an array of words.

    :param file_path: Path to the JavaScript file.
    :return: List of words.
    """
    with open(file_path, "r") as file:
        content = file.read()
        # Extract the array part from the JavaScript file (assuming the format is like 'const name = [...];')
        start = content.find("[")
        end = content.rfind("]") + 1
        array_str = content[start:end]
        # Convert the string representation of the array to a Python list
        word_list = eval(array_str)
        return word_list

def get_feedback_pattern(guess, answer):
    used_indices = set()  # Track used indices in the answer
    pattern = ['0'] * len(guess)  # Initialize feedback pattern with '0's

    # First pass: Check for correct letters in the correct position
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            pattern[i] = '+'
            used_indices.add(i)

    # Second pass: Check for correct letters in the wrong position
    for i, g in enumerate(guess):
        if pattern[i] == '0' and g in answer:
            # Ensure the letter is not already matched
            for j, a in enumerate(answer):
                if g == a and j not in used_indices:
                    pattern[i] = '-'
                    used_indices.add(j)
                    break

    return pattern

def calculate_entropy(guess, answer_list):
    # Dictionary to hold counts of each feedback pattern
    pattern_counts = {}

    # Generate feedback patterns for each word in the answer list
    for answer in answer_list:
        pattern = tuple(get_feedback_pattern(guess, answer))
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

    # Calculate entropy based on the frequency of each pattern
    entropy = 0
    total_patterns = len(answer_list)
    for count in pattern_counts.values():
        probability = count / total_patterns
        entropy -= probability * math.log(probability, 2)

    return entropy


def refine_guess_list(guess_list, current_guess, feedback):
    refined_list = []

    for word in guess_list:
        remaining_letters = list(word)  # Track remaining letters
        match = True

        # First Pass: Correctly Placed Letters
        for i, letter in enumerate(current_guess):
            if feedback[i] == '+':
                if word[i] != letter:
                    match = False
                    break
                remaining_letters.remove(letter)  # Remove matched letter

        if not match:
            continue

        # Second Pass: Misplaced Letters
        for i, letter in enumerate(current_guess):
            if feedback[i] == '-':
                if letter not in remaining_letters or letter == word[i]:
                    match = False
                    break
                remaining_letters.remove(letter)  # Remove matched letter
            elif feedback[i] == '0' and letter in remaining_letters:
                match = False
                break

        if match:
            refined_list.append(word)

    return refined_list


def get_next_guess(guess_list, answer_list, current_guess=None, feedback=None):
    
    if current_guess and feedback:
        # Refine the guess list based on feedback
        refined_guess_list = refine_guess_list(guess_list, current_guess, feedback)
       
    else:
        refined_guess_list = guess_list

    if not refined_guess_list:
    
        return None
    
    # Calculate entropy for each word in the refined list
    entropies = {guess: calculate_entropy(guess, answer_list) for guess in refined_guess_list}

    # Prioritize guesses that are also in the answer list
    valid_guesses = [guess for guess in entropies if guess in answer_list]

    # If there are valid guesses, return the one with the highest entropy
    if valid_guesses:
        return max(valid_guesses, key=entropies.get)
    
    # If there are no valid guesses, return the guess with the highest entropy from the refined list
    return max(entropies, key=entropies.get)



def update_word_list(current_guess, feedback, word_list):
    new_word_list = []

    for word in word_list:
        remaining_letters = list(word)  # Track remaining letters
        match = True

        # First Pass: Correctly Placed Letters
        for i, letter in enumerate(current_guess):
            if feedback[i] == '+':
                if word[i] != letter:
                    match = False
                    break
                remaining_letters.remove(letter)  # Remove matched letter

        if not match:
            continue

        # Second Pass: Misplaced Letters
        for i, letter in enumerate(current_guess):
            if feedback[i] == '-':
                if letter not in remaining_letters:
                    match = False
                    break
                remaining_letters.remove(letter)  # Remove matched letter
            elif feedback[i] == '0' and letter in remaining_letters:
                match = False
                break

        if match:
            new_word_list.append(word)

    return new_word_list


def play_wordle(guess_list, answer_list):
    # Create a prompt session
    session = PromptSession()

    # Main CLI loop
    current_guess = None
    feedback = None

    while True:
        if current_guess is None:
            # Prompt the user for the initial guess
            current_guess = session.prompt("Enter your initial guess (we recommend RAISE): ", ).strip().upper()
        else:
            # Suggest the next guess based on previous feedback
            next_guess = get_next_guess(guess_list, answer_list, current_guess, feedback)
            print_formatted_text(HTML(f"Suggested guess: <b>{next_guess}</b>"), )
            current_guess = next_guess

        feedback = session.prompt("Enter feedback (e.g., '+-00+') or 'exit' to quit: ", ).strip().lower()

        if feedback == 'exit':
            break

        if len(feedback) != len(current_guess):
            print("Invalid feedback length. Please try again.")
            continue

        guess_list = refine_guess_list(guess_list, current_guess, feedback)

        # Debugging: Output the size of the answer list before and after update
        print(f"Size of answer list before update: {len(answer_list)}")
       
        print('BEFORE', answer_list)
        answer_list = update_word_list(current_guess, feedback, answer_list)

        print(f"Size of answer list after update: {len(answer_list)}")
        print('AFTER', answer_list)

        if feedback == '+++++':
            print("Congratulations! The word has been guessed correctly.")
            break

        if not answer_list:
            print("No more possible answers. Please check the feedback.")
            break 

def simulate_wordle(answer, original_guess_list, answer_list):
    current_guess = "SALET" if "SALET" in original_guess_list else random.choice(original_guess_list)
    feedback = None
    num_guesses = 0

    # Create a fresh copy of the guess list for this simulation
    guess_list = original_guess_list

    while True:
        num_guesses += 1
        feedback = ''.join(get_feedback_pattern(current_guess, answer))
        guess_list = refine_guess_list(guess_list, current_guess, feedback)
        answer_list = update_word_list(current_guess, feedback, answer_list)

        if feedback == '+++++':
            break

        if not answer_list:
            print(f"Failed to guess the word: {answer}")
            break

        next_guess = get_next_guess(guess_list, answer_list, current_guess, feedback)
        if next_guess is None:
            print("No valid next guess available.")
            break
        current_guess = next_guess

    return num_guesses


def simulate_all_wordle_games(guess_list, answer_list):
    total_guesses = 0
    total_simulations = len(answer_list)

    for i, word in enumerate(answer_list, 1):
        # Use a fresh copy of the guess list for each simulation
        num_guesses = simulate_wordle(word, guess_list, answer_list)
        total_guesses += num_guesses
        print(f"Simulation {i}/{total_simulations}: Word='{word}', Number of guesses={num_guesses}")

    average_guesses = total_guesses / total_simulations
    print(f"Average number of guesses over {total_simulations} simulations: {average_guesses:.2f}")

    return average_guesses



if __name__ == "__main__":
    guess_list_path = ("word_lists/officialguesses.js" )
    answer_list_path = ("word_lists/officialanswers.js" )
    guess_list = load_word_list_from_js(guess_list_path)
    answer_list = load_word_list_from_js(answer_list_path)

    print(banner)
    print("Welcome to Wordle!")
    print("Please select a mode: 1 - Play, 2 - Simulate")

    # play:1 simulate:2
    mode = int(input("Please select a mode: "))
    if mode == 1:
        play_wordle(guess_list=guess_list, answer_list=answer_list)
    elif mode == 2:
        simulate_all_wordle_games(guess_list=guess_list, answer_list= answer_list)
    else:
        print("Invalid mode. Please try again.")
    