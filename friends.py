#!/usr/bin/env python
import twitter
import sqlite3
import os.path
import sys
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("/path/to/friends.cfg")

conkey = config.get("twitter","consumer_key")
consec = config.get("twitter","consumer_secret")
accesstok = config.get("twitter","access_token")
accesstoksec = config.get("twitter","access_token_secret")
database = config.get("friends","database")

# Check if the database exists or not, create if necessary
if not os.path.exists(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''create table friends
              (friend text)''')
    conn.commit()
    c.close()
    
# Try and establish a connection with the database
try:
    conn = sqlite3.connect(database)
    c = conn.cursor()
except:
    print "Failed to connect to sqlite3 database"

# Try to connect to the Twitter API
try:
    api = twitter.Api(consumer_key=conkey,consumer_secret=consec, access_token_key=accesstok, access_token_secret=accesstoksec)
except:
    print "Failed to connect to the API"

# Verifying all credentials are good
api.VerifyCredentials()

# Get a dictionary object containing all the IDs of your friends
# If userid is new, adds to database
f = api.GetFriendIDs()
for fid in  f['ids']:
    t = (fid,)     
    c.execute('select * from friends where friend=?', t)
    friend = c.fetchone()
    if not friend:
        c.execute('insert into friends values (?)',t)
# Commits the changes
conn.commit()

# Grab a list of people user used to follow
# Report on changes.

c.execute('select * from friends')
temp = []
for of in c:
    if int(of[0]) not in f['ids']:
        temp.append(of[0])
        userid = api.UsersLookup(user_id=[of[0]])
        for uid in userid:
            unfollowed_user=uid.screen_name
        print "Did you mean to unfollow @%s?" % (unfollowed_user)

# Must be a neater way to do this?
for i in temp:
    c.execute("delete from friends where friend = ?",(i,))
conn.commit()

# Close our connections
c.close()
conn.close()
