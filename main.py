# import dotenv
import os
from dotenv import load_dotenv
load_dotenv()

import tweepy

CONSUMER_KEY =os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")  
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") 
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
# api.update_status("j'aime poopy")

#reply to tweet with tweepy
def reply_to_tweet_with_tweepy(text, username):
    tweets = get_tweets_id(username)

    for tweet in tweets:
        api = tweepy.API(auth)
        api.update_status(status = text, in_reply_to_status_id = tweet , auto_populate_reply_metadata=True)


# get data from api
import requests

bearer_token = os.getenv("BEARER_TOKEN")

# function to get data from api with bearer token
def get_data_with_token(url):
    response = requests.get(url, headers={'Authorization': 'Bearer ' + bearer_token})
    return response.json()

# function that returns array of string from object
def get_tweets_text(tweets):
    tweets_text = []
    for tweet in tweets:
        tweets_text.append(tweet.get("text"))
    
    return tweets_text

# function to get tweets from string
def get_tweets(string):
    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + string
    return get_data_with_token(url).get("statuses")

# function to get user from username twitter
def get_user(username):
    url = "https://api.twitter.com/1.1/users/show.json?screen_name=" + username
    return get_data_with_token(url)

# function that returns array of tweets id from username
def get_tweets_id(username):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username
    tweets = get_data_with_token(url)
    tweets_id = []
    for tweet in tweets:
        tweets_id.append(tweet.get("id_str"))
    return tweets_id

#function to post data to twitter from url using api key
def post_data(url, data):
    response = requests.post(url, data=data, headers={'Authorization': 'Bearer ' + bearer_token}, auth=(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET")))
    return response.json()

# function that reply to tweet from tweet id
def reply_to_tweet(tweet_id, text):
    url = "https://api.twitter.com/1.1/statuses/update.json?status=" + text + "&in_reply_to_status_id=" + tweet_id, 
    return post_data(url, text)

#function to authenticate with twitter
def authenticate():
    url = "https://api.twitter.com/oauth2/token"
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET")))
    return response.json()

#function post tweet from text
def post_tweet(text):
    url = "https://api.twitter.com/1.1/statuses/update.json?status=" + text
    return post_data(url, text)

#function get followers screen_name in array from username
def get_followers(username):
    followers = []
    url = "https://api.twitter.com/1.1/followers/list.json?screen_name=" + username
    data = get_data_with_token(url)
    for user in data["users"]:
        followers.append(user["screen_name"])
    return followers

#find tweet with word at the end of the tweet
def find_tweets(word):
    tweets = []

    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + word
    data = get_data_with_token(url)
    for tweet in data["statuses"]:
        tweets.append(tweet["id"])
    return tweets


def reply_to_tweet_from_word(word, text):
    tweets = find_tweets(word)

    for tweet in tweets:
        api = tweepy.API(auth)
        api.update_status(status = text, in_reply_to_status_id = tweet , auto_populate_reply_metadata=True)

reply_to_tweet_from_word("En gros", "En gros ? En gros, le Omar et Fred Burger, c’est un Omar Burger + un Fred Burger. Moi qui m’attendais à un mix des ingrédients, une sauce originale, des émincés de poulets avec des trous dedans... eh bien non. On a droit à un simple Lego. Du coup ma chronique va être facilitée.")