
def get_feedback_pattern(guess, answer):
    used_indices = set()  # Track used indices in the answer
    pattern = ["0"] * len(guess)  # Initialize feedback pattern with '0's

    # First pass: Check for correct letters in the correct position
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            pattern[i] = "+"
            used_indices.add(i)

    # Second pass: Check for correct letters in the wrong position
    for i, g in enumerate(guess):
        if pattern[i] == "0" and g in answer:
            # Ensure the letter is not already matched
            for j, a in enumerate(answer):
                if g == a and j not in used_indices:
                    pattern[i] = "-"
                    used_indices.add(j)
                    break

    return pattern

print(get_feedback_pattern("THEME", "EVOKE"))