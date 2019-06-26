# Xword_task

Crossword drill exercise program

## Functionality
- Present user with a random clue with puzzle details and length of entry
- User can skip to next random clue
- Correct clue entries would be taken to the answer window
- Wrong clue answers would be given the same question again with a "wrong answer" notification
- User can view solution using a provided "escape hatch"
- Show clue entry and other clues with the same entry
- Show all puzzles with the same clue entry
- Show more information about clue

## Models
<img src="https://docs.google.com/uc?id=1MkndBjhgDKIt5WlfN7CM5PFUSpwjdstI" height="80%" width="80%">

- Used 3 models: **Clue**, **Entry**, **Puzzle**
- Used **Django Sessions** to store state of each drill/game.

## Views / Templates
- LogInView: login.html
- DrillView: drill.html
- AnswerView: answer.html
- index.html extends base.html

## Assumptions
- Since clues are selected at random (repeat clues not accounted for)
- Each clue can only have one entry
- Each clue can only have one puzzle
- If users haven't attempted a clue, they can skip to next clue
- Users can view solution for difficult question
- User can start or end drills which resets score
- Each drill would have a count of success and total clues
- User can view total clues answered and total notifications
- Going to root restarts the game


# Users decide to start new game session
<img src="https://docs.google.com/uc?id=1UKh6KJJTQ4YVq7tcY-vuGATjuLzuipoG" height="80%" width="80%">

# Users can input guesses for clues
<img src="https://docs.google.com/uc?id=1yIU2d4TEn6ueaYPxtG_O7lycLHNHw0o6" height="80%" width="80%">


# Users can see Answer page for Successful guess
<img src="https://docs.google.com/uc?id=1C_mwLMkYQDgM_cfxOZimTMajwVVkaCtR" height="80%" width="80%">

# For difficult clues, users can view Answer page with escape option but forfeits the game point
<img src="https://docs.google.com/uc?id=1gIH3ilmtNLetJB_K8V3kDWO4Ve1BEro4" height="80%" width="80%">

## Tools
- Template: HTML / Bootstrap
- DB: SQLITE

## User Sessions
- Browser session without ending drill may stay active up to 2 weeks.

## Test
- [x] Models
- [ ]  Views

## Feedback
The current model structure has a 1-M relationship between Entry and Clue. So although one entry could match multiple clues, one random clue can only have one possible entry (as foreign key). So when a user is congratulated for the right entry text per clue, I'd have a 1-M between clues and entries instead. If an entry text is entered, clue id can now be matched to multiple entries belonging to the same clue. These clue-entry pairs can then be viewed as required.
