#!/usr/bin/env python
import twitter
import cPickle
import sqlite3
import os.path
import sys

conkey=''
consec=''
accesstok=''
accesstoksec=''

if not os.path.exists('./friends.sqlite3'):
    conn = sqlite3.connect('./friends.sqlite3')
    c = conn.cursor()
    c.execute('''create table friends
              (friend text)''')
    conn.commit()
    c.close()
    
try:
    conn = sqlite3.connect('./friends.sqlite3')
    c = conn.cursor()
except:
    print "Failed to connect to sqlite3"

try:
    api = twitter.Api(consumer_key=conkey,consumer_secret=consec, access_token_key=accesstok, access_token_secret=accesstoksec)
except:
    print "Failed to connect to the API"

users = api.GetFriends()
current = []
for u in users:
    current.append(u.screen_name)

for u in current:
    t = (u,)
    c.execute('select * from friends where friend=?', t) 
    friend = c.fetchone()
    if not friend:
        c.execute('insert into friends values (?)',t)
conn.commit()

c.execute('select * from friends')
for of in c:
    if of[0] not in current:
        print "Did you mean to unfollow %s?" % (of)

# Close our connections
c.close()
conn.close()
