
# Replace 'your_file.txt' with the path to your file
input_file = 'word_lists/original_guesses.txt'
output_file = 'word_lists/originalguess.js'

# Read the file, process each line, and write to a new file
with open(input_file, 'r') as file, open(output_file, 'w') as outfile:
    for line in file:
        # Strip whitespace and add quotes and comma
        formatted_line = f'"{line.strip()}",\n'
        outfile.write(formatted_line.upper())

print(f"Formatted words have been written to {output_file}")