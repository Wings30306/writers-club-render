import os
from flask import Flask, app, flash, session
from flask_pymongo import PyMongo
from datetime import date, datetime

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

mongo = PyMongo(app)


"""Collections"""
stories_collection = mongo.db.stories
users_collection = mongo.db.users
fake_collection = None


"""Helper functions"""


def list_by_type():
    list_by_type = {}
    ratings = []
    genres = []
    fandoms = []
    authors = []
    if session.get('is_adult') == True:
        selection = stories_collection.find()
    else:
        selection = stories_collection.find( {"rating": {"$nin": ["R/Adult/NSFW", "Adult/NSFW"]}})
    for story in selection:
        rating = story['rating']
        genres_in_story = story.get('genres')
        if genres_in_story != []:
            for genre in genres_in_story:
                genre
        fandoms_in_story = story.get('fandoms')
        if fandoms_in_story != []:
            for fandom in fandoms_in_story:
                fandom
        else:
            fandom = "Fandom not added"
        author = story['author']
        if rating not in ratings:
            ratings.append(rating)
        if genre not in genres:
            genres.append(genre)
        if fandom not in fandoms:
            fandoms.append(fandom)
        if author not in authors:
            authors.append(author)
    list_by_type.update({"ratings": ratings, "genres": genres,
                         "fandoms": fandoms, "authors": authors})
    return list_by_type


def story_count():
    story_count = []
    ratings_list = list_by_type()["ratings"]
    genres_list = list_by_type()["genres"]
    fandoms_list = list_by_type()["fandoms"]
    authors_list = list_by_type()["authors"]
    for rating in ratings_list:
        count = stories_collection.count_documents({"rating": rating})
        count_rating = {"rating": rating, "total": count}
        story_count.append(count_rating)
    for genre in genres_list:
        count = stories_collection.count_documents({"genres": genre})
        count_genre = {"genre": genre, "total": count}
        story_count.append(count_genre)
    for fandom in fandoms_list:
        count = stories_collection.count_documents({"fandoms": fandom})
        count_fandom = {"fandom": fandom, "total": count}
        story_count.append(count_fandom)
    for author in authors_list:
        count = stories_collection.count_documents({"author": author})
        count_author = {"author": author, "total": count}
        story_count.append(count_author)
    return story_count


def report(item, reason_given, this_story, reported_by):
    stories_collection.find_one_and_update({"url": this_story}, {'$push': {"reports": {"item_reported": item, "reported_by": reported_by, "reason_given": reason_given}}}, upsert=True)
    return flash("Report sent to admins.")


def calculate_age(born):
    today = date.today()
    bday = datetime.strptime(born, '%Y-%m-%d')
    age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
    return age