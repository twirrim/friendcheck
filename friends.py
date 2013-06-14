#!/usr/bin/env python
import twitter
import os.path
import sys
import ConfigParser
import cPickle

config = ConfigParser.RawConfigParser()
config.read("/path/to/friends.cfg")

conkey = config.get("twitter","consumer_key")
consec = config.get("twitter","consumer_secret")
accesstok = config.get("twitter","access_token")
accesstoksec = config.get("twitter","access_token_secret")
previous = config.get("friends","previous")

# Check if the previous exists or not, create if necessary
if os.path.exists(previous):
    pkl_file = open(previous,'rb')
    knownfriends = cPickle.load(pkl_file)
    pkl_file.close()
else:
    knownfriends = []

# Try to connect to the Twitter API
try:
    api = twitter.Api(consumer_key=conkey,consumer_secret=consec, access_token_key=accesstok, access_token_secret=accesstoksec)
except:
    print "Failed to connect to the API"

# Verifying all credentials are good
api.VerifyCredentials()

# Get a dictionary object containing all the IDs of your friends
# appends all entries to a list for easy native comparison
f = api.GetFriendIDs()
friends = []
for fid in  f:
    friends.append(fid)

# We don't care about order, so we can take advantage of the
# intersection properties of sets in python
difference = list(set(knownfriends)-set(friends))

if (len(difference)>0):
    userid = api.UsersLookup(user_id=difference)
    for uid in userid:
        print "Did you mean to unfollow @%s?" % (uid.screen_name)

# storing for next run
pkl_file = open(previous,'wb')
cPickle.dump(friends,pkl_file, -1)
pkl_file.close()
