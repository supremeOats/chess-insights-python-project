**To set up the project install the necessary libraries via the *requirements.txt* file**

**To start the app call the command:**</br>
    *flask --app web.app run*

**For debug mode:**</br>
    *flask --app web.app run --debug*</br>

The database should set up automatically

**To use the app:**
- To search users go to the "*Search*" page from the navigation bar on top and type their username as they are registered in [chess.com](chess.com)
- Click on the "*Games*" section on a user's profile to see the games they've played
- By default the system loads the games from last week, you can filter them trough the menu below
- The "*Search*" field above the list allows you to search for keywords in the table dynamically (without the page reloading), using the filters below and clicking "*Search*" will reload the page
- An example of the replay system can be seen by clicking on the "Replay" button of a game entry on the game list page

**Example page:**
http://127.0.0.1:5000/profiles/magnuscarlsen/games

**Note:** When a user profile or a game is loaded for the first time it is fetched by the chess.com API, then it is saved to the local database, so the first time a user or games are loaded it may take a little bit more time.

**Note** The front-end of the replay system is not yet implemented
