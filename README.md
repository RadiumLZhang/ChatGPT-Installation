# ChatGPT-Installation

## User Guide
### Installation


## Developer Guide
### Code Structure
### Frontend
- 1st - Intro
  - Let user choose to play or create
- 2nd - Play
    - Pop out the question database
    - Show 5 images and 1 generated image
    - Let user type in the prompt
    - Show the result
    - Show the correct answer
    - Show the score
    - Let user choose to play again or go back to the intro
- 3rd - Create
    - Let user choose a theme
    - Show 5 images
    - Let user type in the prompt
    - Show the result
    - Show the score
    - Let user choose to play again or go back to the intro
- 4th - Question Scoreboard
    - show the theme name
    - show the correct percentage, label it as easy, medium, hard
    - show the create time: if it is created within a hour, show the new tag
    - show the creator name
    - show the number of players
- 5th - Player Scoreboard
    - show the player name
    - show the correct percentage
    - show the number of questions answered
    - show the number of questions created

### Backend
- Creator Scoreboard
- Player Scoreboard

- Origin Image Database:
  - image_id: int
  - image_path: str
  - theme_id: int
  - theme_name: str
  - theme_description: str

- Generated Image Database
  - image_id: int
  - image_path: str

- Creator theme Database: for each question, there is several origin images
  - theme_id: int
  - suggested_prompt: List[str]
  - origin_image_ids: List[int]

- Player Question Database: for each question, there is 5 origin images and 1 generated image
  - question_id: int
  - selected origin_image_ids: List[int]
  - generated_image_id: int
  - create_time: timestamp
  
- Answer Database:
  - answer_id: int
    - question_id: int
    - answer: str
    - score: int
    - player_id: int
    - create_time: timestamp

- Player Database:
    - player_id: int
    - player_name: str
    - player_correct_percentage: float
    - player_answers: List[answer_id]



### Developer Guide
#### Project Setup
```bash
pip install Flask Flask-SQLAlchemy
```

Execute the script to set up your environment:
./setup_env.sh





---

### Questions

1. Guesser page: 2 posts, one is AI generated, the other one is human made. 
   1. Where the human genearted one come from? 
   2. if the comparisons in a group is different, the answer would be different. 

2. Database prepared
3. 
