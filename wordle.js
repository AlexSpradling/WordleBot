
let answer; // Declare the variable to store the answer
let guesses;
let gameActive;

function initializeGame() {
    answer = officialAnswers[Math.floor(Math.random() * officialAnswers.length)];
    guesses = [];
    gameActive = true;
    displayGuesses();
}

function getFeedbackPattern(guess, answer) {
    let pattern = [];
    let usedIndices = new Set();

    // First pass: Correct letters in the correct position
    for (let i = 0; i < guess.length; i++) {
        if (guess[i] === answer[i]) {
            pattern[i] = "+";
            usedIndices.add(i);
        } else {
            pattern[i] = "0";
        }
    }

    // Second pass: Correct letters in the wrong position
    for (let i = 0; i < guess.length; i++) {
        if (pattern[i] === "0" && answer.includes(guess[i])) {
            for (let j = 0; j < answer.length; j++) {
                if (guess[i] === answer[j] && !usedIndices.has(j)) {
                    pattern[i] = "-";
                    usedIndices.add(j);
                    break;
                }
            }
        }
    }

    return pattern.join('');
}

function displayFeedback(feedback) {
    const container = document.createElement('div');
    container.className = 'feedback-container';

    for (let char of feedback) {
        const block = document.createElement('span');
        block.className = 'feedback-block';
        if (char === '+') block.classList.add('correct');
        else if (char === '-') block.classList.add('present');
        else block.classList.add('absent');
        container.appendChild(block);
    }

    return container;
}


function submitGuess() {
    if (!gameActive) {
        alert("Game over. Please reset to start a new game.");
        return;
    }

    const guessInput = document.getElementById("guessInput");
    const guess = guessInput.value.toUpperCase();
    console.log(guess);

    // Validate the input guess
    if (guess.length !== 5 || !/^[A-Z]+$/.test(guess)) {
        alert("Invalid guess. Please enter a 5-letter word.");
        return;
    }

    if (!officialGuesses.includes(guess)) {
        alert("Invalid guess. Please try a different word.");
        return;
    }

    // Calculate the feedback
    const feedback = getFeedbackPattern(guess, answer);

    // Store the guess and feedback
    guesses.push({ guess, feedback });
    displayGuesses();

    // Clear the input field after submitting
    guessInput.value = '';

    // Check for game end conditions
    if (feedback === "+++++") {
        alert("Congratulations! You've guessed the word!");
        gameActive = false; // End the game
    } else if (guesses.length >= 6) { // Limit the number of guesses
        alert(`Game over. The correct word was ${answer}.`);
        gameActive = false; // End the game
    }
}


function displayGuesses() {
    document.getElementById("guesses").innerHTML = '';
    guesses.forEach(g => {
        const p = document.createElement("p");
        p.innerText = `Guess: ${g.guess}`;
        p.appendChild(displayFeedback(g.feedback));
        document.getElementById("guesses").appendChild(p);
    });
}

function resetGame() {
    initializeGame();
    document.getElementById("guessInput").value = '';
    document.getElementById("guesses").innerHTML = '';
}

// Initialize the game on page load
initializeGame();