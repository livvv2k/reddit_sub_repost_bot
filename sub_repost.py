import praw
import tweepy
import json
import urllib.request
import time
import datetime
import schedule
import os # file handling

def RunAction():
    reddit = praw.Reddit(user_agent='VALUE', client_id='VALUE', client_secret='VALUE', username='VALUE', password='VALUE')

    twitter_auth_info = { 
        "consumer_key"        : "VALUE",
        "consumer_secret"     : "VALUE",
        "access_token"        : "VALUE",
        "access_token_secret" : "VALUE" 
    }

    auth = tweepy.OAuthHandler(twitter_auth_info['consumer_key'], twitter_auth_info['consumer_secret'])
    auth.set_access_token(twitter_auth_info['access_token'], twitter_auth_info['access_token_secret'])
    twitter = tweepy.API(auth)

    dateToday = datetime.date.today()
    dateYesterday = datetime.date.today() - datetime.timedelta(1)

    # initial search done on pushshift which unforunately as of now lacks score updating, use reddit's api to get actual score
    url = "https://api.pushshift.io/reddit/submission/search/?subreddit=AssassinsCreedOdyssey&after={}&before={}&size=512".format(dateYesterday, dateToday)
    data = json.loads(urllib.request.urlopen(url).read().decode())
    most_upvotes = 0
    chosen_post_info = {}
    for x in range(len(data["data"])):
        if "link_flair_text" in data["data"][x] and data["data"][x]["link_flair_text"] == "Photo Mode":
            postinfo = reddit.submission(data["data"][x]["id"])
            if postinfo.score > most_upvotes:
                chosen_post_info = {'author': postinfo.author, "url": postinfo.permalink,'imgurl': postinfo.url, "score": postinfo.score}
                most_upvotes = postinfo.score
    
    if "imgurl" in chosen_post_info:
        tempFile = "temp." + chosen_post_info["imgurl"][-3:]
        urllib.request.urlretrieve(chosen_post_info["imgurl"], tempFile)
        tweet_text = "Tweet Test"
        twitter.update_with_media(filename = tempFile, status = tweet_text)
        os.remove(tempFile)


schedule.every().day.at("00:15").do(RunAction)

while True:
    schedule.run_pending()
    time.sleep(30)

#RunAction()
