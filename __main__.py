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

# Other functions (calculate_entropy, get_next_guess, update_word_list) remain the same


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


def calculate_entropy(guess, answer_list):
    """
    Calculates the entropy of the guess based on the answer list.

    Entropy is calculated as the sum of the product of the probability of each feedback pattern and the log of the probability.

    :param guess: The guess to calculate the entropy for.
    :param answer_list: The list of possible answers.
    :return: The entropy of the guess.

    """
    # explanation of entropy: https://www.youtube.com/watch?v=ErfnhcEV1O8


    # Dictionary to hold counts of each feedback pattern
    pattern_counts = {}

    # Generate feedback patterns for each word in the answer list
    for answer in answer_list:
        pattern = []
        for g, a in zip(guess, answer):
            if g == a:
                pattern.append('+')  # Correct letter and position
            elif g in answer:
                pattern.append('-')  # Correct letter, wrong position
            else:
                pattern.append('0')  # Incorrect letter
        pattern = tuple(pattern)
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

    # Calculate entropy based on the frequency of each pattern
    entropy = 0
    total_patterns = len(answer_list)
    for count in pattern_counts.values():
        probability = count / total_patterns
        entropy -= probability * math.log(probability, 2)
        # guess, probability, entropy
        print(f'{guess}, p:{probability}, e:{entropy}')
    return entropy

def refine_guess_list(guess_list, current_guess, feedback):
    """
    Refine the guess list based on feedback.
    """
    refined_list = []
    for word in guess_list:
        match = True
        for i in range(len(current_guess)):
            if feedback[i] == '+':
                if word[i] != current_guess[i]:
                    match = False
                    break
            elif feedback[i] == '-':
                if current_guess[i] == word[i] or current_guess[i] not in word:
                    match = False
                    break
            elif feedback[i] == '0':
                if current_guess[i] in word:
                    match = False
                    break
        if match:
            refined_list.append(word)

    return refined_list



def get_next_guess(guess_list, answer_list, current_guess=None, feedback=None):
    if current_guess and feedback:
        # Refine the guess list based on feedback
        refined_guess_list = refine_guess_list(guess_list, current_guess, feedback)
        # If the refined list is empty, return a random guess from the original list
        if not refined_guess_list:
            return random.choice(guess_list)
    else:
        refined_guess_list = guess_list

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
        match = True
        for i in range(len(current_guess)):
            if feedback[i] == '+':
                # Letter must be in the correct position
                if word[i] != current_guess[i]:
                    match = False
                    break
            elif feedback[i] == '-':
                # Letter must be in the word but not in this position
                if current_guess[i] == word[i] or current_guess[i] not in word:
                    match = False
                    break
            elif feedback[i] == '0':
                # Letter must not be in the word
                if current_guess[i] in word:
                    match = False
                    break
        if match:
            new_word_list.append(word)
    return new_word_list


guess_list_path = ("word_lists/officialguesses.js" )
answer_list_path = ("word_lists/officialanswers.js" )
guess_list = load_word_list_from_js(guess_list_path)
answer_list = load_word_list_from_js(answer_list_path)


# Create a prompt session
session = PromptSession()

# Main CLI loop
current_guess = None
feedback = None

print(banner)
print("Welcome to WordleBot!, a Wordle solver.")
print('')

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
    answer_list = update_word_list(current_guess, feedback, answer_list)
    print(f"Size of answer list after update: {len(answer_list)}")

    if feedback == '+++++':
        print("Congratulations! The word has been guessed correctly.")
        break

    if not answer_list:
        print("No more possible answers. Please check the feedback.")
        break 


def simulate_wordle(answer, guess_list, answer_list):
    current_guess = None
    feedback = None
    num_guesses = 0

    # Start with a strong initial guess
    current_guess = "RAISE" if "RAISE" in guess_list else random.choice(guess_list)

    while True:
        num_guesses += 1

        # Generate feedback based on the answer
        feedback = ''
        for g, a in zip(current_guess, answer):
            if g == a:
                feedback += '+'
            elif g in answer:
                feedback += '-'
            else:
                feedback += '0'

        # Update the guess list and answer list based on the feedback
        guess_list = refine_guess_list(guess_list, current_guess, feedback)
        answer_list = update_word_list(current_guess, feedback, answer_list)

        if feedback == '+++++':
            break

        if not answer_list:
            print(f"Failed to guess the word: {answer}")
            break

        # Use entropy for subsequent guesses
        current_guess = get_next_guess(guess_list, answer_list, current_guess, feedback)

    return num_guesses


# # Define the number of simulations you want to run
# num_simulations = 100  # You can adjust this number

# # Initialize a variable to keep track of the total number of guesses across all simulations
# total_guesses = 0

# # Run the simulations
# for _ in range(num_simulations):
#     print(f"Running simulation {_ + 1} of {num_simulations}")
#     # Randomly select a word from the answer list
#     random_answer = random.choice(answer_list)

#     # Simulate the game for this word
#     num_guesses = simulate_wordle(random_answer, guess_list.copy(), answer_list.copy())

#     print(f"Number of guesses: {num_guesses}")

#     # Add the number of guesses to the total
#     total_guesses += num_guesses

# # Calculate the average number of guesses
# average_guesses = total_guesses / num_simulations

# # Print the result
# print(f"Average number of guesses over {num_simulations} simulations: {average_guesses}")
