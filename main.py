# import dotenv
import os
from dotenv import load_dotenv
load_dotenv()

import tweepy

from fastapi import FastAPI

# fast api init
app = FastAPI()

CONSUMER_KEY =os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")  
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") 
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

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
@app.get("/get_tweets_content")
async def get_tweets_text(tweets):
    tweets_text = []
    for tweet in tweets:
        print(tweet)
        tweets_text.append(tweet["text"])
    
    return tweets_text


# function to get tweets from text
@app.get("/get_tweets/{text}")
async def get_tweets(text):
    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + text
    tweets = []
    for tweet in get_data_with_token(url).get("statuses"):
        tweets.append(tweet["text"])
    return tweets


# function to get user from username twitter
@app.get("/get_user/{username}")
async def get_user(username):
    url = "https://api.twitter.com/1.1/users/show.json?screen_name=" + username
    return get_data_with_token(url)

# function that returns array of tweets id from username
@app.get("/get_tweets_id/{username}")
async def get_tweets_id(username):
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
@app.post("/reply_to_tweet/{tweet_id}")
async def reply_to_tweet(tweet_id, text):
    url = "https://api.twitter.com/1.1/statuses/update.json?status=" + text + "&in_reply_to_status_id=" + tweet_id, 
    return post_data(url, text)


#function post tweet from text
@app.post("/post_tweet/{text}")
async def post_tweet(text):
    url = "https://api.twitter.com/1.1/statuses/update.json?status=" + text
    return post_data(url, text)

#function get followers screen_name in array from username
@app.get("/get_user_followers/{username}")
async def get_followers(username):
    followers = []
    url = "https://api.twitter.com/1.1/followers/list.json?screen_name=" + username
    data = get_data_with_token(url)
    for user in data["users"]:
        followers.append(user["screen_name"])
    return followers

#find tweet with word at the end of the tweet
@app.get("/find_tweets_from_word/{word}")
async def find_tweets(word):
    tweets = []

    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + word
    data = get_data_with_token(url)
    for tweet in data["statuses"]:
        tweets.append(tweet["id"])
    return tweets

@app.post("/reply_from_word/{word}")
async def reply_to_tweet_from_word(word, text):
    tweets = find_tweets(word)

    for tweet in tweets:
        api = tweepy.API(auth)
        api.update_status(status = text, in_reply_to_status_id = tweet , auto_populate_reply_metadata=True)

    return tweets

#function to find my own tweets that contains word
@app.get("/find_my_tweets/{word}")
async def find_my_tweets(word):
    tweets = []
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + "jayzon95"
    data = get_data_with_token(url)
    for tweet in data:
        if word in tweet["text"]:
            tweets.append(tweet["id"])
    return tweets


# delete my tweets from words
@app.post("/delete_tweets_from_word/{word}")
async def delete_tweets_from_word(word):
    tweets = find_my_tweets(word)

    for tweet in tweets:
        api = tweepy.API(auth)
        api.destroy_status(tweet)



