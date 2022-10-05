import os
import json
from helper import app, stories_collection, users_collection
from helper import story_count, list_by_type, report, calculate_age
from flask import Flask, redirect, url_for, render_template, request
from flask import flash, session
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify


"""Error Handlers"""
"""Page Not Found"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


"""Server Error"""


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


"""Routes"""


@app.route('/')
def index():
    return render_template("index.html")


"""
User authentication with thanks to Miroslav Svec, DCD Channel lead.
Adapted from https://github.com/MiroslavSvec/DCD_lead
"""


# Sign up
@app.route('/register')
def register():
    # Check if user is not logged in already
    if 'username' in session:
        flash('You are already signed in!')
        return redirect(url_for('profile', user=session['username']))
        # Render page for user to be able to register
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def check_registration():
    form = request.form.to_dict()
    # Check if the password and password1 actualy match
    if form['user_password'] == form['user_password1']:
        # If so try to find the user in db
        user = users_collection.find_one({"user_name": form['username']})
        email = users_collection.find_one({"email": form['email']})
        if user:
            flash(form['username'].title(
            ) + " already exists!  Is this you? Please sign in instead. " +
                "Else, please choose a different username.")
            return redirect(url_for('register'))
        elif email:
            flash("We already have a registered user with " +
                  form['email'] +
                  "! Did you forget your username?" +
                  " Sign in with email instead.")
            return redirect(url_for('login'))
        # If user does not exist register new user
        else:
            # Hash password
            hash_pass = generate_password_hash(form['user_password'])
            # Create new user with hashed password
            users_collection.insert_one(
                {
                    'user_name': form['username'],
                    'email': form['email'],
                    'password': hash_pass,
                    'birthday': form['birthday']
                }
            )
            # Check if user is actualy saved
            user_in_db = users_collection.find_one(
                {"user_name": form['username']})
            if user_in_db:
                # Log user in (add to session)
                session['username'] = user_in_db['user_name']
                session['is_admin'] = user_in_db.get('is_admin')
                birthday = user_in_db['birthday']
                age = calculate_age(birthday)
                if age >= 18:
                    session['is_adult'] = True
                else:
                    session['is_adult'] = False
                flash("You have been successfully signed in!")
                # If user came from elsewhere in the app
                if session.get('next') is not None:
                    return redirect(session['next'])
                return redirect(url_for('profile',
                                        user=user_in_db['user_name']))
            else:
                flash("There was a problem saving your profile")
                return redirect(url_for('register'))

    else:
        flash("Passwords don't match!")
        return redirect(url_for('register'))


# Login
@app.route('/login', methods=['GET'])
def login():
    # Check if user is not logged in already
    if session.get('username') is not None:
        flash("You are logged in already!")
        if session.get('next') is not None:
            return redirect(session['next'])
        return redirect(url_for('profile', user=session['username']))
    else:
        # Render the page for user to be able to log in
        return render_template("login.html")


# Check user login details from login form
@app.route('/user_auth', methods=['POST'])
def user_auth():
    form = request.form.to_dict()
    user_in_db = users_collection.find_one(
        {"$or": [{"user_name": form['username']},
                 {"email": form['username']}]})
    # Check for user in database
    if user_in_db:
        # If passwords match (hashed / real password)
        if check_password_hash(user_in_db['password'], form['user_password']):
            # Log user in (add to session)
            session['username'] = user_in_db['user_name']
            session['is_admin'] = user_in_db.get('is_admin')
            birthday = user_in_db['birthday']
            age = calculate_age(birthday)
            if age >= 18:
                session['is_adult'] = True
            else:
                session['is_adult'] = False
            flash("You have been successfully signed in!")
            if session.get('next') is not None:
                return redirect(session['next'])
            return redirect(url_for('profile', user=user_in_db['user_name']))

        else:
            flash("Wrong password / username!")
            return redirect(url_for('login'))
    else:
        flash("You must be registered!")
        return redirect(url_for('register'))


# Log out
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out. We hope to see you again soon!')
    return redirect(url_for('index'))


"""
End of User AUTH
"""


@app.route('/user/<user>')
def profile(user):
    user_profile = users_collection.find_one({'user_name': user})
    if user_profile is None:
        flash(user + " doesn't exist")
        return redirect(url_for('index'))
    if user == session.get('username'):
        user_stories = stories_collection.find({'author': user})
    else:
        if session.get("is_adult") is True:
            user_stories = stories_collection.find(
                {'author': user, "chapters.0": {"$exists": True}})
        else:
            user_stories = stories_collection.find({'author': user, "rating": {
                                                   "$nin":
                                                   ["R/Adult/NSFW",
                                                    "Adult/NSFW"]},
                "chapters.0":
                {"$exists": True}})
    user_stories_count = user_stories.count()
    return render_template("profile.html",
                           user=user,
                           stories=user_stories,
                           profile=user_profile,
                           count=user_stories_count)


@app.route('/user/<user>/make-admin')
def make_admin(user):
    users_collection.find_one_and_update(
        {"user_name": user}, {"$set": {"is_admin": True}})
    return redirect(url_for("profile", user=user))


@app.route('/user/<user>/remove-admin')
def remove_admin(user):
    users_collection.find_one_and_update(
        {"user_name": user}, {"$set": {"is_admin": False}})
    return redirect(url_for("profile", user=user))


@app.route('/admin')
def admin_page():
    users = users_collection.find({"is_admin": True})
    if session.get("is_admin") is True:
        report_list = []
        reports = stories_collection.find({"reports": {'$gt': {'$size': 0}}})
        for report in reports:
            report_list.append(report)
        if len(report_list) > 0:
            report_list
        return render_template("adminteam.html",
                               users=users,
                               reports=report_list)
    return render_template("adminteam.html", users=users)


@app.route('/story/<story_to_read>/clear-report/<loop_index>')
def clear_reports(story_to_read, loop_index):
    list_index = int(loop_index) - 1
    story = stories_collection.find_one({"url": story_to_read})
    report = story['reports'][list_index]
    stories_collection.find_one_and_update(
        {"url": story_to_read}, {'$pull': {'reports': report}})
    return redirect(url_for("admin_page"))


@app.route('/user/<user>/edit')
def edit_profile(user):
    if session:
        user_profile = users_collection.find({'user_name': user})
        if user == session['username']:
            return render_template("editprofile.html",
                                   user=user,
                                   profile=user_profile)
        else:
            flash("You cannot edit someone else's profile!")
            return redirect(url_for('profile', user=user, profile=profile))
    else:
        flash("You must be signed in to edit your profile.")
        return redirect(url_for("login"))


@app.route('/user/<user>/edit', methods=['POST'])
def update_profile(user):
    if session.get('username') is not None:
        if user == session['username']:
            users_collection.find_one_and_update({"user_name": user},
                                                 {"$set": {"user_name": user,
                                                           "birthday":
                                                           request.form.get
                                                           ('birthday'),
                                                           "started_writing":
                                                           request.form.get
                                                           ('started_writing'),
                                                           "intro": json.loads(
                                                               request.form.get
                                                               ('editor')),
                                                           "show_birthday":
                                                           request.form.get
                                                           ('show_birthday')}})
            return redirect(url_for('profile', user=user))
        else:
            flash("You cannot edit someone else's profile!")
            return redirect(url_for('profile', user=user, profile=profile))
    else:
        session['next'] = request.url
        flash("You must be signed in to edit your profile!")
        return redirect(url_for('profile', user=user, profile=profile))


@app.route('/all-stories')
def all_stories():
    if session:
        if session['is_adult'] is True:
            all_stories = stories_collection.find(
                {"chapters.0": {'$exists': True}})
        else:
            all_stories = stories_collection.find(
                {"rating": {"$nin": ["R/Adult/NSFW", "Adult/NSFW"]},
                 "chapters.0": {'$exists': True}})
            flash("Adult stories have been filtered out" +
                  " because you are underage")
    else:
        all_stories = stories_collection.find(
            {"rating": {"$nin": ["R/Adult/NSFW", "Adult/NSFW"]},
             "chapters.0": {'$exists': True}})
        flash(
            "Adult-rated stories have been filtered out. " +
            "You need to sign in to read these.")
    return render_template("allstories.html",
                           stories=all_stories)


@app.route('/search')
def search():
    count = story_count()
    return render_template("search.html", count=count)


@app.route('/search', methods=["POST"])
def get_search_results():
    genre = request.form.get("genre")
    if genre == "No genre selected":
        genre = {'$exists': True}
    fandom = request.form.get("fandom")
    if fandom == "No fandom selected":
        fandom = {'$exists': True}
    rating = request.form.get("rating")
    if rating == "No rating selected":
        if session.get('is_adult') is True:
            rating = {'$exists': True}
        else:
            rating = {"$nin": ["R/Adult/NSFW", "Adult/NSFW"]}
    author = request.form.get("author")
    if author == "No author selected":
        author = {'$exists': True}
    result = stories_collection.find({'$and': [{"genres": genre},
                                               {"fandoms": fandom},
                                               {"rating": rating},
                                               {"author": author},
                                               {"chapters.0":
                                               {'$exists': True}}]})
    return render_template("allstories.html", stories=result)


@app.route('/story/<story_to_read>/<chapter_number>')
def read(story_to_read, chapter_number):
    chapter_index = int(chapter_number) - 1
    for story in stories_collection.find({"url": story_to_read}):
        this_chapter = story['chapters'][chapter_index]
        cover_image = story.get('cover_image')
        author = story['author']
        title = story['title']
        fandoms = story['fandoms']
        disclaimer = story['disclaimer']
        summary = story['summary']
        chapter = this_chapter
        rating = story['rating']
        genres = story['genres']
        total_chapters = len(story['chapters'])
        return render_template(
            "story.html",
            story=story,
            story_to_read=story_to_read,
            cover_image=cover_image,
            title=title,
            author=author,
            fandoms=fandoms,
            genres=genres,
            rating=rating,
            chapter=chapter,
            chapter_number=int(chapter_number),
            summary=summary,
            disclaimer=disclaimer,
            total_chapters=int(total_chapters))


@app.route('/story/<story_url>/new-chapter')
def new_chapter(story_url):
    for story in stories_collection.find({"url": story_url}):
        if session:
            if session['username'] == story['author']:
                return render_template("addchapter.html", story=story)
            else:
                flash("You cannot edit someone else's story!")
                return redirect(url_for("index"))
        else:
            session['next'] = request.url
            flash("You must be signed in to edit your stories!")
            return redirect(url_for("login"))


@app.route('/story/<story_url>/new-chapter', methods=["POST"])
def add_chapter(story_url):
    chapter_title = request.form['chapter_title']
    if request.form['editor'] == '\"<p><br></p>\"':
        flash("You cannot send in empty posts!")
        return redirect(url_for("new_chapter", story_url=story_url))
    elif request.form['editor'] == "":
        flash("You cannot send in empty posts!")
        return redirect(url_for("new_chapter", story_url=story_url))
    elif len(request.form['editor']) < 50:
        flash("Chapter length must be 50 characters or more!")
        return redirect(url_for("new_chapter", story_url=story_url))
    else:
        chapter_content = json.loads(request.form['editor'])
        chapter_number = request.form['chapter_number']
        chapter = {"chapter_number": chapter_number,
                   "chapter_title": chapter_title,
                   "chapter_content": chapter_content}
        stories_collection.find_one_and_update({"url": story_url},
                                               {"$push": {
                                                "chapters": chapter
                                                }}, upsert=True
                                               )

        return redirect(
            url_for(
                'read',
                story_to_read=story_url,
                chapter_number=chapter_number))


@app.route('/story/<story_to_read>/edit')
def edit_story(story_to_read):
    for story in stories_collection.find({"url": story_to_read}):
        if session.get('username') is not None:
            if session['username'] == story['author']:
                genres = list_by_type()["genres"]
                fandoms = list_by_type()["fandoms"]
                ratings = ['R/Adult/NSFW', '15', 'PG13', 'PG', 'All Ages']
                return render_template(
                    "editstory.html",
                    story=story,
                    story_to_read=story_to_read,
                    genres=genres,
                    fandoms=fandoms,
                    ratings=ratings)
            else:
                flash("You cannot edit someone else's story!")
                return redirect(url_for("index"))
        else:
            session['next'] = request.url
            flash("You must be signed in to edit your stories.")
            return redirect(url_for("login"))


@app.route('/story/<story_to_read>/edit', methods=['POST'])
def update_story(story_to_read):
    formatted_inputs = {}
    form_data = request.form
    for key in form_data:
        value_key = key
        key = key.split("-")
        key = key[0]
        if key in formatted_inputs:
            formatted_inputs[key].append(form_data[value_key])
        else:
            formatted_inputs[f"{key}"] = []
            formatted_inputs[key].append(form_data[value_key])
    genres = formatted_inputs.get("genre")
    if genres is None:
        genres = []
    if form_data["newgenre"] != "":
        genres.append(form_data.get("newgenre"))
    fandoms = formatted_inputs.get("fandom")
    if form_data["newfandom"] != "":
        fandoms.append(form_data.get("newfandom"))

    stories_collection.find_one_and_update({"url": story_to_read},
                                           {"$set": {
                                               "title":
                                               request.form.get('title'),
                                               "summary":
                                               request.form.get('summary'),
                                               "author": session['username'],
                                               "genres": genres,
                                               "rating":
                                               request.form.get('rating'),
                                               "fandoms": fandoms,
                                               "disclaimer":
                                               request.form.get('disclaimer'),
                                           }
    })
    return redirect(url_for('profile', user=session['username']))


@app.route('/story/<story_to_read>/<chapter_number>/edit')
def edit_chapter(story_to_read, chapter_number):
    story = stories_collection.find_one({"url": story_to_read})
    chapter_index = int(chapter_number) - 1
    if session.get('username') is not None:
        if session['username'] == story['author']:
            chapter = story['chapters'][chapter_index]
            return render_template(
                "editchapter.html",
                story_to_read=story_to_read,
                story=story,
                chapter=chapter,
                chapter_number=chapter_number)
        else:
            flash("You cannot edit someone else's story!")
            return redirect(url_for("index"))
    else:
        session['next'] = request.url
        flash("You must be signed in to edit your stories!")
        return redirect(url_for("login"))


@app.route('/story/<story_to_read>/<chapter_number>/edit', methods=['POST'])
def update_chapter(story_to_read, chapter_number):
    if request.form['editor'] == '\"<p><br></p>\"':
        flash("You cannot send in empty posts!")
        return redirect(
            url_for(
                "edit_chapter",
                story_to_read=story_to_read,
                chapter_number=chapter_number))
    elif request.form['editor'] == "":
        flash("You cannot send in empty posts!")
        return redirect(
            url_for(
                "edit_chapter",
                story_to_read=story_to_read,
                chapter_number=chapter_number))
    elif len(request.form['editor']) < 50:
        flash("Chapter length must be 50 characters or more!")
        return redirect(
            url_for(
                "edit_chapter",
                story_to_read=story_to_read,
                chapter_number=chapter_number))
    else:
        story = stories_collection.find_one({'url': story_to_read})
        chapters = story['chapters']
        chapter_index = int(chapter_number) - 1
        chapters[chapter_index]['chapter_title'] = request.form[
                                                    'chapter_title']
        chapters[chapter_index]['chapter_content'] = json.loads(
            request.form['editor'])
        stories_collection.find_one_and_update({"url": story_to_read},
                                               {"$set": {
                                                "chapters": chapters
                                                }}, upsert=True
                                               )

        return redirect(
            url_for(
                'read',
                story_to_read=story_to_read,
                chapter_number=chapter_number))


@app.route('/new-story')
def new_story():
    if session.get('username') is not None:
        images = [
            "bay",
            "beach",
            "blue",
            "buddha",
            "circles",
            "city-blue",
            "city-green",
            "city-pink",
            "crowd-blue",
            "crowd-red",
            "daisy",
            "dark-blue",
            "desert",
            "eye-in-the-sky",
            "family",
            "farmhouse",
            "flowers",
            "green-face",
            "heart",
            "justice-is-blind",
            "moon-sea",
            "rose-moon",
            "sailing-day",
            "sailing-night",
            "sea",
            "silhouette-red",
            "storm",
            "wildflowers"]
        genres = list_by_type()["genres"]
        fandoms = list_by_type()["fandoms"]
        return render_template(
            "newstory.html",
            images=images,
            genres=genres,
            fandoms=fandoms)
    else:
        session['next'] = request.url
        flash("You must be signed in to add a story!")
        return redirect(url_for('login'))


@app.route('/new-story', methods=["POST"])
def add_story():
    if session.get('username') is not None:
        formatted_inputs = {}
        form_data = request.form
        for key in form_data:
            value_key = key
            key = key.split("-")
            key = key[0]
            if key in formatted_inputs:
                formatted_inputs[key].append(form_data[value_key])
            else:
                formatted_inputs[f"{key}"] = []
                formatted_inputs[key].append(form_data[value_key])
        genres = formatted_inputs.get("genre")
        if genres is None:
            genres = []
        if form_data["newgenre"] != "":
            genres.append(form_data.get("newgenre"))
        fandoms = formatted_inputs.get("fandom")
        if fandoms is None:
            fandoms = []
        if form_data["newfandom"] != "":
            fandoms.append(form_data.get("newfandom"))
        story_url = (session['username'] + "-" +
                     slugify(request.form.get('title'))).lower()
        stories_collection.insert_one({
            "title": request.form.get('title').title(),
            "cover_image": request.form.get('image'),
            "url": story_url,
            "summary": request.form.get('summary'),
            "author": session['username'],
            "genres": genres,
            "rating": request.form.get('rating'),
            "fandoms": fandoms,
            "disclaimer": request.form.get('disclaimer')
        })
        return redirect(url_for('new_chapter', story_url=story_url))
    else:
        flash("You must be signed in to add a story!")


@app.route('/story/<story_to_read>/delete')
def delete_story(story_to_read):
    story = stories_collection.find_one({"url": story_to_read})
    if session.get('username') is not None:
        if session['username'] == story['author']:
            stories_collection.remove({"url": story_to_read})
            flash("Story deleted!")
            return redirect(url_for('profile', user=session['username']))
        else:
            flash("You cannot delete someone else's story!")
    else:
        session['next'] = request.url
        flash("You must be signed in to delete stories!")
    return redirect(url_for('login'))


@app.route('/story/<story_to_read>/<chapter_number>/delete')
def delete_chapter(story_to_read, chapter_number):
    story = stories_collection.find_one({"url": story_to_read})
    chapter_index = int(chapter_number) - 1
    if session.get('username') is not None:
        if session['username'] == story['author']:
            chapter = story['chapters'][chapter_index]
            stories_collection.find_one_and_update({"url": story_to_read},
                                                   {"$pull": {
                                                       "chapters": chapter
                                                   }}, upsert=True
                                                   )
            flash("Chapter deleted!")
            return redirect(url_for("edit_story", story_to_read=story_to_read))
        else:
            flash("You cannot delete someone else's story!")
            return redirect(url_for("index"))
    else:
        session['next'] = request.url
        flash("You must be signed in to delete chapters!")
        return redirect(url_for("index"))


@app.route('/story/<story_to_read>/<chapter_number>/feedback')
def display_fb_page(story_to_read, chapter_number):
    if session.get('username') is not None:
        stories = stories_collection.find({"url": story_to_read})
        for story in stories:
            chapter = story["chapters"][int(chapter_number) - 1]
            feedback = story.get("feedback")
        return render_template(
            "feedback.html",
            story=story,
            chapter=chapter,
            feedback=feedback)
    else:
        session['next'] = request.url
        flash("You must be signed in to post feedback.")
        return redirect(url_for('login'))


@app.route(
    '/story/<story_to_read>/<chapter_number>/feedback',
    methods=["POST"])
def post_feedback(story_to_read, chapter_number):
    story = story_to_read
    chapter = chapter_number
    if request.form['editor'] == '\"<p><br></p>\"':
        flash("You cannot send in empty posts!")
    elif request.form['editor'] == "":
        flash("You cannot send in empty posts!")
    else:
        feedback = json.loads(request.form['editor'])
        posted_by = request.form['posted_by']
        feedback_post = {"fb_for_chapter": chapter,
                         "posted_by": posted_by, "feedback_content": feedback}
        stories_collection.find_one_and_update({"url": story},
                                               {"$push": {
                                                   "feedback": feedback_post
                                               }}, upsert=True
                                               )
        flash("Feedback Posted")
    return redirect(
        url_for(
            "display_fb_page",
            story_to_read=story,
            chapter_number=chapter))


@app.route('/story/<story_to_read>/report')
def report_story(story_to_read):
    if session.get('username') is not None:
        stories = stories_collection.find({"url": story_to_read})
        for story in stories:
            story
        return render_template('report.html', story=story)
    else:
        session['next'] = request.url
        flash("You must be signed in to report stories.")
        return redirect(url_for('login'))


@app.route('/story/<story_to_read>/report', methods=["POST"])
def send_story_report(story_to_read):
    item = story_to_read
    reported_by = session['username']
    report_reason = request.form["reason"]
    report(item, report_reason, story_to_read, reported_by)
    return redirect(url_for("admin_page"))


if __name__ == "__main__":
    app.run(host=os.getenv("IP"),
            port=os.getenv("PORT"),
            debug=os.getenv("DEBUG"))
