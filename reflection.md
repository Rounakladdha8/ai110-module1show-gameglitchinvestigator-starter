# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
When I first ran the game, the Streamlit application loaded successfully and showed the guessing game interface along with developer debug information. While playing the game, I noticed that several parts of the game logic did not behave as expected. Some hints were incorrect, the game state was inconsistent,nvalid inputs were accepted without validation.

The first bug I noticed was that the hint logic was incorrect. When the secret number was 63 and I guessed 70, the game displayed "GO HIGHER!" instead of telling me to guess lower. Another issue was that the game accepted invalid inputs such as -5, updated the score, and added the value to the game history instead of rejecting it. I also observed inconsistent attempt tracking during gameplay, where the displayed attempt information did not always match the expected game state.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Initial game start | Attempts should start at 0 and attempts left should be 8 | Game state appeared inconsistent during startup | None |
| Guess = 70, Secret = 63 | Show "Go LOWER!" | Showed "GO HIGHER!" | None |
| Guess = -5 | Reject invalid input and ask for a number between 1 and 100 | Accepted input, updated score/history, and gave a hint | None |
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
I used Claude Code and ChatGPT during this project. AI correctly identified that the hint messages were reversed, and I verified the fix by testing the game manually. One misleading suggestion was trying to analyze multiple bugs at once, so I focused on fixing and testing one issue at a time.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
I considered a bug fixed only after testing it manually and checking the game behavior. I also ran pytest, and all 23 tests passed successfully. AI helped generate and explain the tests, but I verified the results myself.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I learned that Streamlit reruns the script after every interaction. Session state stores important values like the secret number and score so the game does not reset each time.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I want to continue fixing one bug at a time and testing each change before moving on. This project taught me that AI is a useful assistant, but its suggestions should always be verified.