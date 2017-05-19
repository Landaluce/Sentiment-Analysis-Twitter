import tweepy
from textblob import TextBlob
import re


def get_tweets(search_query, number_tweets=50):
    """
    Gets a list of tweets
    :param search_query: search query used to find tweets (String)
    :param number_tweets: number of tweets to get (Integer)
    :return: List of tweets
    """
    consumer_key = 'XXXXXX'
    consumer_secret = 'XXXXXX'
    access_token = 'XXXXXX'
    access_token_secret = 'XXXXXX'
    consumer_key = 'RLBnivPChhdTjB9s2lL1M88Po'
    consumer_secret = 'UFXipb6TJb9H9vGolaZoxQczRbPfsy5QafwYSlK80ypAJvfmYx'
    access_token = '850748910930972672-wTQ7Gm0zUhrhipOm49N4gpWW6CXwZer'
    access_token_secret = 'Tnj3vU8kc51rti8kfZRRvphfs7vDD6dfbDcYLYpnEv8uP'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.search(q=search_query, count=number_tweets)
    text = []
    for tweet in tweets:
        new_text = scrub_tweet(tweet.text)
        if len(new_text) > 0:
            text.append(new_text)
    return text, tweets


def scrub_tweet(tweet):
    """
    Scubs a list of tweets
    :param tweet: tweet (String)
    :return: scrubed_tweets: Scrubbed list of tweets (List of Strings)
    """
    tweet = tweet.lower()
    tweet = re.sub(r'https://.*', '', tweet)

    tweet = re.sub(r'rt.*?:', '', tweet)
    tweet = re.sub(r'\(.*?.\)', '', tweet)
    tweet = re.sub(r'@.*? ', '', tweet)
    tweet = re.sub(r'@.*?', '', tweet)
    tweet = re.sub(r'#.*? ', '', tweet)
    tweet = tweet.replace("&gt", ' ')
    tweet = tweet.replace("&lt", ' ')
    tweet = tweet.replace("&amp", ' ')

    tweet = tweet.replace(u'\u2014', '-')
    tweet = tweet.replace(u'\u2013', '-')
    exclude = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    exclude += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    exclude.append(u'\u2018')  # '
    exclude.append(u'\u2019')  # '
    exclude.append(u'\u201c')  # "
    exclude.append(u'\u201d')  # "
    exclude.append(u'\u2022')  # bullet point
    exclude.append(u'\u2026')  # ...

    for c in exclude:
        tweet = tweet.replace(c, ' ')
        tweet = tweet.strip()
    tweet.replace("\n", " ")
    tweet = tweet.replace('-', ' ')
    scrubed_tweet = ' '.join(tweet.split())
    return scrubed_tweet


def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 1 #positive
    elif analysis.sentiment.polarity == 0:
        return 0 #neutral
    else:
        return -1 #negative


def get_sentiments(search_query, number_tweets):
    texts, tweets = get_tweets(search_query, number_tweets)
    users = []
    messages = []
    for tweet in tweets:
        if tweet.text.startswith("RT @"):
            temp = re.sub('RT @.*:', '', tweet.text)
            messages.append(temp)
        else:
            messages.append(tweet.text)
        users.append(tweet.user.name)
    positive = 0
    neutral = 0
    negative = 0

    for text in texts:
        sentiment = get_tweet_sentiment(text)
        if sentiment > 0:
            positive += 1
        elif sentiment == 0:
            neutral += 1
        else:
            negative += 1

    found = positive + neutral + negative
    zipped_content = zip(users, messages)

    return [positive, neutral, negative, found], zipped_content

