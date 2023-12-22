def read_js_word_list(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        start = content.find("[")
        end = content.rfind("]") + 1
        array_str = content[start:end]
        word_list = eval(array_str)
        return word_list

# Load the word lists
official_guesses = read_js_word_list('word_lists/officialguesses.js')
original_guesses = read_js_word_list('word_lists/originalguesses.js')

# Check for differences
def check_word_lists(list1, list2):
    for word in list1:
        # Check for non-standard characters
        if not word.isalpha() or not word.isupper():
            print(f"Non-standard format in list1: {word}")
        # Check word length
        if len(word) != 5:  # Assuming Wordle words are 5 letters
            print(f"Unexpected length in list1: {word}")

    for word in list2:
        # Check for non-standard characters
        if not word.isalpha() or not word.isupper():
            print(f"Non-standard format in list2: {word}")
        # Check word length
        if len(word) != 5:  # Assuming Wordle words are 5 letters
            print(f"Unexpected length in list2: {word}")

    # Check for words in list1 not in list2 and vice versa
    diff1 = set(list1) - set(list2)
    diff2 = set(list2) - set(list1)
    print(f"Words in list1 not in list2: {diff1}")
    print(f"Words in list2 not in list1: {diff2}")

check_word_lists(official_guesses, original_guesses)