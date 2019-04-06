#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "1065497629767991296-bIp1dADwScXufcJn3Px1hJoksR84T3"
access_token_secret = "1BlMiT1DYtO6aRoMbG7H93ZmrS53YCREUSSp68IKdaotc"
consumer_key = "kGNm4K8DhGZBqzKmWEUsozgZQ"
consumer_secret = "tO4pWXf0X4rlKfvzvayx0xBpaaUzxNyJTluJyuTJa1Cu9FkvSW"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Udemy','udemy','UDEMY'])


# In[ ]:


#python twitter_live_v1_udemy.py > twitter_data_udemy.txt


# In[ ]:




