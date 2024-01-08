# WORDLE BOT!
Author: Alex Spradling

---

# Introduction

A lot of folks have done this, and probably done it better [most notably 3blue1brown!](https://www.3blue1brown.com/lessons/wordle), but this is how I did it. 

This package consists of a script for running `AlexBot` a WORDLE bot, and a Jupyter Notebook that walks the reader through building a WORDLE bot algorithm from the ground up. The datasets have shifted a bit since WORDLE's initial release, but the final `AlexBot` uses the starting word `SALET` and solves all WORDLE words in the answer set with a mean score of 3.57 guesses -- which is very close to the "mathematically optimal" solution. 

I'm happy enough with the results and happier to share them with you. So here we go, here's how you build a WORDLE bot that is pretty good. 

## Package Content
1. [AlexBot - A pretty good WORDLE bot](alex_bot.py)
2. [How to make a WORDLE bot - A Jupyter Notebook stepping you through the entire process](entropy_notebook.ipynb)
3. [Words - The data I'm using](word_lists)
---
# Application

The WORDLE bot can be used in two ways:
1. You can play WORDLE with it, enter your chosen starting word and then encode the feedback as either `+` for the right letter in the right place, `-` for a correct letter in  wrong place, or `0` for a letter that is not in the word -- you'll end up entering a string that looks something like `00-++`. Enter the feedback and the bot sill suggest the next word and so on. 

2. You can evaluate a word choice -- enter the word you'd like to evaluate, and the bot will iterate through the entire WORDLE answer list using your word as the starting word. It will return the mean number of guesses for the whole set. 

# How it works

*(The following is excerpted text from the Jupyter Notebook. The notebook implements the algorithm from scratch, providing many intuition building examples along the way!)*

---

The heart of algorithm is based on INFORMATIONAL ENTROPY, which at its core is just some 9th grade math applied in a very clever way.

INFORMATIONAL ENTROPY was developed by Claude Shannon at Bell Labs in 1948. It provides a quantitative measure of the uncertainty or randomness in a set of outcomes. Let's delve into the foundational concepts and the mathematical formulation of entropy.

## Defining Key Concepts

1. **Information**: In the context of information theory, 'information' quantifies the reduction in uncertainty. When an event occurs that we were uncertain about, we gain information. The more uncertain the event, the more information it provides.

2. **Bit**: A 'bit' is the basic unit of information in information theory. It represents 1 unit of information in the form of a binary choice. A decision that can result in two equally likely outcomes provides one bit of information -- If I flip a fair coin and tell you I have Heads, you now know that the other side must be Tails -- we've eliminated 1 piece of uncertainty (and therefore gained 1 piece of information).

3. **Probability**: The chance of a random event happening. A basic probability is found by dividing your preferred event by all other possible events. (The probability of getting heads when flipping a fair coin is .5 -- one event/two possible outcomes = 1/2 = .5)


## Information as Uncertainty

If I flip a (fair) coin and tell you the side facing up is heads I've given you a little bit (to be precise, one bit) of information. 

You know, as a matter of fact, that a coin has two sides, heads and tails, and that it turns out that flipping a coin many times results in one side or the other coming up in my palm with equal probability. 

By telling you that Heads is up *you also know that tails is down* -- you've gained that 1 piece of information. 

Information Entropy rigorously reconciles this concept of uncertainty and information. 


## The Formula for Entropy

$$ H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i) $$

- **The Summation $\sum$**: Represents the sum of information from all possible outcomes.
- **Probability $P(x_i)$**: The likelihood of each outcome.
- **Logarithm $\log_2$**: A logarithm, in simple terms, tells us how many times we need to multiply a base number (like 2) by itself to get another number. For example, $\log_2 8 = 3$ because $2 \times 2 \times 2 = 8$. 
- **Why Base 2?**: In information theory, we often deal with scenarios that have two outcomes, like flipping a coin. Using a base-2 logarithm is natural here because it directly relates to these binary (two-option) scenarios. Each bit of information represents a choice between two equally likely possibilities. Thus, the base-2 logarithm measures the number of binary choices (or bits) needed to encode the information from an outcome.

For a fair coin (H for Heads, T for Tails), each with a probability of 0.5:

$$ H(X) = -[P(H) \log_2 P(H) + P(T) \log_2 P(T)] $$
$$ H(X) = -[0.5 \log_2 0.5 + 0.5 \log_2 0.5] $$
$$ H(X) = -[-0.5 - 0.5] $$
$$ H(X) = 1 \text{ bit} $$

So, we see that as defined above, 1 piece of information is an event with a binary outcome, I tell you I've got Heads, and since you know that we have an equal probability of getting Tails you can eliminate the uncertainty that the coin could be showing tails. That's the information you just gained. 

## Stay With Me!

Now, let's consider a six-sided die. Unlike the coin toss, a dice roll has more outcomes, each with its own probability. If I roll a fair dice and tell you that I rolled a 1, I've informed you of more than just the outcome. Implicitly, I've also told you that the dice *isn't showing 2, 3, 4, 5, or 6.*

This means you've gained more information from the result of a dice roll than from a coin flip because more potential outcomes are eliminated based on the lower probability of each outcome occurring. 

The Math:


Applying our entropy formula:

$$ H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i) $$

For a fair dice, our random variable $X$ can take six values (1, 2, 3, 4, 5, 6), each with a probability of 1/6. The calculation is:

$$ H(X) = -\sum_{i=1}^{6} \frac{1}{6} \log_2 \frac{1}{6} $$
$$ H(X) = -6 \times \left( \frac{1}{6} \log_2 \frac{1}{6} \right) $$
$$ H(X) = -\log_2 \frac{1}{6} $$
$$ H(X) \approx 2.58 \text{ bits} $$


Ok, so hopefully things are starting to make a little bit more sense now. We know a 1 on a fair die also means NOT 2,3,4,5,6, which is more information than just 1 is not 2. But as we look at the calculation above and see 2.58 bits as the result and the definition of a bit is "1 piece of information" which is further defined as a result that can be narrowed down to 2 equally likely outcomes we start to get confused again -- what exactly is 2.58 decisions that result in equally likely outcomes?



Consider you're trying to guess the outcome of a die roll:

In this scenario, the path to the answer may vary, sometimes being shorter or longer, which is why the average information content is a fractional number like 2.58. This represents the average amount of uncertainty resolved, or information gained, from observing the outcome of a fair die roll.
    
1. **First Question: "Is the number greater than 3?"**
   - If Yes: The possible outcomes are 4, 5, or 6.
   - If No: The possible outcomes are 1, 2, or 3.

2. **Second Question:**
   - If the answer to the first question was Yes:
     - Ask: "Is the number less than 5?"
       - If Yes: The outcome is 4.
       - If No: The outcomes are 5 or 6.
   - If the answer to the first question was No:
     - Ask: "Is the number greater than 1?"
       - If Yes: The outcomes are 2 or 3.
       - If No: The outcome is 1.

3. **Third Question:**
   - Only needed if there are still two possibilities after the second question.
     - If the remaining possibilities are 5 and 6:
       - Ask: "Is the number less than 6?"
         - If Yes: The outcome is 5.
         - If No: The outcome is 6.
     - If the remaining possibilities are 2 and 3:
       - Ask: "Is the number less than 3?"
         - If Yes: The outcome is 2.
         - If No: The outcome is 3.

In this scenario, the path to the answer may vary, sometimes being shorter or longer, which is why the average information content is a fractional number like 2.58. This represents the average amount of uncertainty resolved, or information gained, from observing the outcome of a fair die roll.

### More Certainty = Less Uncertainty to Eliminate = Less Information

Ok, you understand more uncertainty = more information. What does less uncertainty = less information look like?

Back to the coins. What if the coin was *not* fair, it's loaded and it will come up heads more often than tails. We start flipping the coin and it's coming up heads more than tails and this isn't really surprising to you because *you know* that I've skewed the probabilities and the fact that heads is coming up more than tails just isn't really news to you. So with less uncertainty, we gain a little less information. 

Let's do the math again, we'll say that heads comes up 70% of the time with my new fixed coin.

$$ H(X) = -[P_1 \log_2 P_1 + P_2 \log_2 P_2] $$
$$ H(X) = -[0.7 \log_2 0.7 + 0.3 \log_2 0.3] $$
$$ H(X) = -[0.7 \times -0.5146 + 0.3 \times -1.7370] $$
$$ H(X) = -[-0.3602 - 0.5211] $$
$$ H(X) \approx 0.8813 \text{ bits} $$

I've rigged the results and you are less surprised and therefore less informed by the results of the coin flip, we can see that the calculated information is now $.88$ bits where it was once $1$ when we had a fair coin. 

