# The Writers' Club

When I did the first project ([User Centric Frontend](https://wings30306.github.io/WingsBookClub/)), the main question I got from friends who write and read was: "Can you make it interactive so we can post our own stories and give feedback?" A few months have passed since, but it's here now: a website where you can post your own stories with no requirements: All stories are welcome here with no requirements or limitations for rating, genre, whether it's original or a fan fic, which fandom, how many chapters... and give feedback on other people's stories.

Happy reading / writing!
 
## UX

Read the full document for [thought process and database schemas](thought-process-and-database-schemas.pdf). As this project focuses on the back-end, a [template](https://startbootstrap.com/template-overviews/clean-blog/) has been used for the front-end look.


### User Stories
1.	As a reader, I would like to be able to read stories, preferably without signing in.
2.	**WIP** As a reader, I would like to see the ratings by other people to decide which story I would like to read.
4.	As a reader, I would like to be able to filter stories by fandom, genre, rating,…
5.	As a reader, I would like to give feedback for stories. I understand I’ll have to sign in to do this.
6.	**WIP** As a reader, I would also like to rate stories when I give feedback.
7.	As a writer, I would like to easily add new chapters / stories.
8.	As a writer, I would like to be able to change already-uploaded chapters too, in case I find a mistake or typo that needs to be corrected.
9.	**WIP** As a writer, I would like to be able to upload a cover image for my story. 
1.  If I don’t have a cover image, I'd like to have a choice of placeholder. 
1.	**WIP** As a writer, I would like to receive any feedback in email so I don’t always have to check the site for new posts.
1.	As a writer, I would like to be able to add a keyword (new genre, new fandom,…) if the one applicable to my story isn’t listed yet.
1.	**WIP** As a writer, I would like to know how many times my story has been read. Visualisation (statistical graphs)  would be also be  nice for this. Perhaps a dashboard for each author, to be accessed on sign-in?
1.	**WIP** As an admin, I would like to be able to suspend or block users who don’t follow the terms and conditions, for example those who post spam or don’t follow the guidelines for appropriate conduct.
1. **WIP** As an admin, I'd like to be able to delete inappropriate comments in feedback or edit the story characteristics if they were put in incorrectly.


## Features
 
### Existing Features
- User Registration: allows new users to create an account so they can log in.
- User Log-in: allows existing users to log in using their username or email and password. Passwords are hashed for security reasons. Log-in is required to read adult-rated stories, post your own stories and give feedback. 
- User Profiles: allow users to tell others about themselves, provide a list of stories posted by this user. A user must be logged in to edit their own profile. A user cannot edit someone else's profile. A user must be logged in and an adult to be able to see adult-rated stories by the user whose profile they visit.
- Search: allows a user to search for stories by rating, genre, fandom and/or author.
- All Stories: exactly what it says: provides a list of all stories available to the user (filters out adult-rated stories if user is not logged in or underage).
- Story pages: the main reason of existence for this project. These pages, generated for each chapter of each story, allow the user to actually read said story. 
- Admin Area/Meet the Team: introduces users to the admin team. If user is an admin, they will also see reports by users that may require admin action. 

### Features Left to Implement
- Allow users to upload their own cover image for a story.
- Show graphs for writers as detailed in user stories.
- Allow readers to rate other people's stories.
- Allow readers to search for stories based on other users' average rating.
- Allow admins to block/suspend users when necessary.


## Technologies Used

### Languages
- [HTML](https://html.com/#What_is_HTML) provides the main building blocks of the website in terms of structure and fixed content.
- [CSS](https://techterms.com/definition/css) adds custom styling beyond what's provided in the template.
- [Javascript](https://www.javascript.com/) is used to make the Quill editor work: 
    - customize user options for styling their story, feedback or profile text.
    - transfer the content of the Quill editor to a hidden input field in order to send it to the back-end for storing in the Database.
- [Python](https://www.python.org/) provides the connection to the backend, specifically the NoSQL (Mongo) database that's hosted by [mlab](https://mlab.com). Also, it allows the use of the [Jinja](https://palletsprojects.com/p/jinja/) templating language that's used to display the data to the user and make the website dynamic - no need for hard-coding everything!

### Frameworks
- [Bootstrap](https://getbootstrap.com/) provides the grid system that's used to make the website look good, as well as several components such as the responsive nav bar. The [template](https://startbootstrap.com/template-overviews/clean-blog/) used was also built with and provided by Bootstrap.

### Libraries

- [JQuery](https://jquery.com) was used to simplify DOM manipulation. It is also required to make Bootstrap work. 
- [Popper](https://popper.js.org/) is required to make Bootstrap work.
- [QuillJS](https://quilljs.com/) provides the text editor that allow users to style their own content (stories, feedback, profile text). If you want _italic_ or **bold** text for example, you can add this easily.


## Testing

### Automated

Automated testing has been used to check that pages were loading, see [test file](test_app.py) for details.

### Manual

All forms have been tested extensively both by myself during the build of this website and fellow students who offered to test. Required fields can't be submitted without a minimum amount of characters, so just typing a period or a single space won't allow the forms to pass.

It's also been tested that use of the url won't override the restrictions for users to edit or delete other people's input (profile as well as stories).

A user also can't override the adult restriction by going through the author's profile or a search. I've not restricted individual stories in case of the server restarting during a read (and thus the session expiring) - the user would have to already have the url in order to use this to "cheat" the adult restrictions, meaning they would have to know the exact username of the author as well as the story title, which makes it a bit redundant as neither title or author show up in the story lists for underage or not-signed-in users.

### Checking the code

The Python code itself has been checked and made PEP8-compliant using pep8online.com and pycodestyle.

CSS has been run through the [Jigsaw CSS Validator](http://jigsaw.w3.org/css-validator/) with no errors found:
![Valid CSS](http://jigsaw.w3.org/css-validator/images/vcss-blue "Valid CSS")

HTML has been checked by running the app links in the [W3 Validator](https://validator.w3.org/nu/?doc=https%3A%2F%2Fthe-writers-club.herokuapp.com%2F). This avoids any problems with Jinja templating that might show up if testing the file by upload, seen as the pages are tested **after** Jinja has been loaded rather than before. The only warning given was on the register page where there is a date input. Modern browsers seem to have no issue with this (see Browser Compatibility) as it's at least partially supported, so I've left it as is. 

### Browser compatibility

This site has been tested on following browsers:
- Google Chrome
- Microsoft Edge
- Firefox
- iOS Safari

### Responsive design

The site has been tested on various screen sizes from phone to SmartTV size using the DevTools provided in Google Chrome.

It's also been tested on a Sony Experia smartphone with no discernable issues. 

## Deployment

This project is hosted on [Heroku](heroku.com). It's been deployed using the following steps:
1. Sign up (new user) or sign in to Heroku account. _I already had an account from previous projects, so only needed to sign in._
1. Click the button at the top right that says "New", select "Create new app" in the dropdown.
1. Choose an app name. __Caution! This must be unique!__
1. Select your region. _In my case, this is Europe._ 
1. You'll be redirected to the Deploy tab of the new app.
1. Go to Deployment method. Select your prefered deployment method. _As my code was already on Github, I chose the "Connect to Github" option. The following steps will be specific to this option._
1. Sign in to your Github account to allow Heroku access to repositories.
1. Search for your repo name. If you can't remember the specific spelling of the name, leave the input field blank and click "Search" to get a list of all your repos.
1. When you've found your repo in the list, click the "Connect" button.
1. You now have the choice to enable automatic deploys or deploy manually. 
1. Your project will need to contain the following in order for Heroku to deploy it:
    - a Procfile: this specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including:
        - Your app’s web server
        - Multiple types of worker processes
        - A singleton process, such as a clock
        - Tasks to run before a new release is deployed.

        _In the case of this project, the Procfile contains only a single line:_
        ```
        web: python app.py
        ```
    - a requirements.txt file. This tells Heroku which dependencies need to be installed in order for the project to run. It's created by using the command `pip install` + the name of any dependencies you have (for example, Flask needs to be installed for this project) in the terminal of your prefered editor, followed by the command `pip freeze > requirements.txt` which will write the installed dependencies to a text file which Heroku then installs using `pip install requirements.txt`. 
1. Go to settings in the Heroku tab. Click "Reveal Config Vars". Add the relevant environment variables you've used in your project to the Config Vars so Heroku can access them. Specifically, for this particular project, that means the following Config Vars were added: 
    - DEBUG (set to False to turn off Debug mode in the deployed version. Locally, in development, this variable was set to True.)
    - IP
    - MONGO_DBNAME
    - MONGO_URI
    - PORT
    - SECRET_KEY
1. Check the activity tab. The two most recent items in the list should read "Deployed" and "Build Succeeded" in their status. 
1. Click "Open App" in the top right side if this is the case, this will take you to the live site of the [Project](https://the-writers-club.herokuapp.com/).

### To run this project locally:
1. Clone the [Github repo](https://github.com/wings30306/the-writers-club) using the green "Clone or download" button. Several options are available here.
1. Open the project in your prefered editor.
1. Create a virtual environment using the command `python -m venv envname`, replacing "envname" with the name you want to give this environment. (More information on virtual environments: https://docs.python.org/3/library/venv.html)
1. Open the virtual environment:
    - Windows Cmd Shell: `<envname>\Scripts\Activate`
    - Posix/Linux bash Shell:
    `$ source <envname>/bin/activate`
1. Install the dependencies using the command `pip install -r requirements.txt`
1. Set up environment variables. There are different ways to do this  depending on your system and/or editor. In my editor of choice, VS Code running on Windows, you can do this in the .vscode directory that's generated for every project. This will contain a settings.json file. Add the following to the json dictionary: 
    ``` 
    "terminal.integrated.env.windows": 
    {
        "MONGO_DBNAME": "theDatabaseName",
        "MONGO_URI": "theDatabaseURL",
        "SECRET_KEY": "YourSecretKeyHere"
    },
    ``` 
1. Run the project in your terminal using the command `python app.py` (like pip, for Unix-based systems you may need to use `python3`).

## Credits

### Content
- All stories were provided by the respective authors/users.

### Media
- The masthead image [Person Typing On Typewriter](https://www.pexels.com/photo/person-typing-on-typewriter-958164/) was posted by [rawpixel.com](https://www.pexels.com/@rawpixel) on [Pexels](www.pexels.com).
- The paintings for the cover image choice were kindly provided by [CreaFien](https://robbehenderickx.wixsite.com/creafien).

### Acknowledgements

- I based the layout for the site on this [template: Start Bootstrap - Clean Blog](https://startbootstrap.com/template-overviews/clean-blog/).