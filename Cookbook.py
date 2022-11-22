#!/usr/bin/env python
# coding: utf-8

# # Performing Sentiment Analysis on Tweets
# - Following Tutorial: [https://youtu.be/uPKnSq6TaAk]
# - See Also:           [https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?text=I+like+you.+I+love+you]

# In[3]:


import tweepy
import configparser
import pandas as pd


# # Initialization of Tokens, Keys, & Twitter API

# In[4]:


config = configparser.ConfigParser()


# In[5]:


config.read('config.ini')


# In[6]:


api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']


# In[7]:


auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)


# In[8]:


import tweepy
import configparser
import pandas as pd

config = configparser.ConfigParser()

config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)


# # Sentiment Analysis

# In[27]:


from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
import numpy as np
from scipy.special import softmax



# In[112]:


def sentiment_analyze(tweet):
    # Preprocess Tweet
    words = tweet.split(' ')
    words = ['@user' if (w.startswith('@') and len(w) > 1) else w for w in words]
    tweet_preprocessed = " ".join(words)
    print(f'Tweet (Preprocessed): {tweet_preprocessed}')
    
    # Initialize Model
    roberta_url = 'cardiffnlp/twitter-roberta-base-sentiment'
    model = AutoModelForSequenceClassification.from_pretrained(roberta_url)
    tokenizer = AutoTokenizer.from_pretrained(roberta_url)
    labels = ['Negative', 'Neutral', 'Positive']
    
    # Run Model(Tweet)
    tweet_encoded = tokenizer(tweet_preprocessed, return_tensors='pt')
    #output = model(tweet_encoded['input_ids'], tweet_encoded['attention_mask'])
    output = model(**tweet_encoded)
    
    # Output
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    for i in range(len(scores)):
        print(f'{labels[i]}: {scores[i]}')
        
    return labels, scores


# In[113]:



