# Put the use case you chose here. Then justify your database choice:
#Use case:Hackernews
#
#The reason I chose Redis for this assignment is its fast in-memory read/write speed and its support for set and sorted set data structures
#which allows me to keep track of top comments, top articles, newest articles, newest comments etc. Although not all of them are listed here
#the ability to create all these leaderboard are very important for sites like hackernews as the information (ariclec, comments etc) are always 
#displayed in a weighted manner and it is important to give the user the ability to sort according to different criteria.
#
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# Because Redis uses a master-slave model in case of a node failure a slave node would be promoted to master and the system would be able to continue. 
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# User, article and comment are not OKAY to lose as having those three models are enough to reconstruct the other models which are mostly
# used for scorekeeping. For persistance, I can manually call the BGSAVE method whenever a new user or article or comment is created to 
# force redis to take a snapshot and save the dataset.


import redis
import time

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

# Action 1: A user publishes an article
def publish_article(redis, user, title, link):
	user_id = user.split(':')[-1]
	article_id = str(int(redis.zrange("nArticles", 0, 0)[0]) + 1)

	redis.hset("article:" + article_id, "title", title)
	redis.hset("article:" + article_id, "upvotes", 1)
	redis.hset("article:" + article_id, "user", user_id)
	redis.hset("article:" + article_id, "link", link)
	redis.hset("article:" + article_id, "time", time.time())
	redis.hset("article:" + article_id, "comments", 0)
	
	redis.hincrby(name=user, key="submissions", amount=1)
	redis.hincrby(name=user, key="karma", amount=1)

	redis.sadd("uSubmissions:" + user_id, article_id)

	redis.zadd("tArticles", 1, article_id)
	redis.zadd("nArticles", time.time(), article_id)

	return article_id


# Action 2: A user sees a list of the 10 highest-voted articles
def return_top_ten(redis):
	last_id = int(redis.zrange("nArticles", -1, -1)[0])
	return 	redis.zrange("tArticles", last_id - 9, last_id)


# Action 3: A user up-votes an article
def article_vote_up(redis, article):
	article_id = article.split(':')[-1]
	user_id = redis.hget(name=article, key='user')

	redis.zincrby(name='tArticles:', value=article_id, amount=1)

	redis.hincrby(name="user:" + user_id, key='karma', amount=1)
	redis.hincrby(name=article, key='upvotes', amount=1)


# Action 4: A user comments on an article
def comment_article(redis, user, article, comment):
	user_id = user.split(':')[-1]
	article_id = article.split(':')[-1]
	comment_no = str(int(redis.hget("article:" + article_id, "comments")) + 1)

	redis.hset("comment:" + article_id + comment_no, "text", comment)
	redis.hset("comment:" + article_id + comment_no, "upvotes", 1)
	redis.hset("comment:" + article_id + comment_no, "user", user_id)
	redis.hset("comment:" + article_id + comment_no, "time", time.time())

	redis.hincrby(name=user, key="karma", amount=1)
	redis.hincrby(name=user, key="comments", amount=1)
	redis.hincrby(name=article, key="comments", amount=1)

	redis.sadd("aComments:" + article_id, comment_no)

	redis.sadd("uComments:" + user_id, article_id + comment_no)

	return article_id + comment_no


# Action 5: A user sees a list of the 10 newest articles
def return_new_ten(redis):
	last_id = int(redis.zrange("nArticles", -1, -1)[0])
	return redis.zrange("nArticles", last_id - 9, last_id)


# Action 6: A user down-votes an article
def article_vote_down(redis, article):
	article_id = article.split(':')[-1]
	user_id = redis.hget(name=article, key='user')

	redis.zincrby(name='tArticles:', value=article_id, amount=-1)
	
	redis.hincrby(name="user:" + user_id, key='karma', amount=-1)
	redis.hincrby(name=article, key='upvotes', amount=-1)


# Action 7: A user signs up
def new_user(redis, username):
	user_id = str(int(redis.hget("counter", "user")) + 1)
	redis.hset("user:" + user_id, "username", username)
	redis.hset("user:" + user_id, "created", time.time())
	redis.hset("user:" + user_id, "karma", 0)
	redis.hset("user:" + user_id, "comments", 0)
	redis.hset("user:" + user_id, "submissions", 0)


# Action 8: A user upvotes a comment
def comment_vote_up(redis, comment):
	user_id = redis.hget(name=comment, key='user')

	redis.hincrby(name="user:" + user_id, key='karma', amount=1)
	redis.hincrby(name=comment, key='upvotes', amount=1)


#USERS

redis.hset("user:1", "username", "nazli")
redis.hset("user:1", "created", time.time() - 11111)
redis.hset("user:1", "karma", 2266)
redis.hset("user:1", "comments", 1)
redis.hset("user:1", "submissions", 1)

redis.hset("user:2", "username", "can")
redis.hset("user:2", "created", time.time() - 222222)
redis.hset("user:2", "karma", 266)
redis.hset("user:2", "comments", 1)
redis.hset("user:2", "submissions", 1)

redis.hset("user:3", "username", "montse")
redis.hset("user:3", "created", time.time())
redis.hset("user:3", "karma", 66)
redis.hset("user:3", "comments", 2)
redis.hset("user:3", "submissions", 0)

#ARTICLES

redis.hset("article:1", "title", "Shape of Water")
redis.hset("article:1", "upvotes", 1234)
redis.hset("article:1", "user", "1")
redis.hset("article:1", "link", "http://time.com/5185843/oscars-2018-the-shape-of-water-best-picture/")
redis.hset("article:1", "time", time.time() - 333333)
redis.hset("article:1", "comments", 2)

redis.hset("article:2", "title", "Get Out")
redis.hset("article:2", "upvotes", 4321)
redis.hset("article:2", "user", "2")
redis.hset("article:2", "link", "http://www.unewsonline.com/2017/03/02/get-out-now/")
redis.hset("article:2", "time", time.time() - 4444444)
redis.hset("article:2", "comments", 2)

#COMMENTS
redis.hset("comment:11", "text", "Best picture")
redis.hset("comment:11", "upvotes", 826)
redis.hset("comment:11", "user", "2")
redis.hset("comment:11", "time", time.time() - 5555555)

redis.hset("comment:12", "text", "Meh")
redis.hset("comment:12", "upvotes", 426)
redis.hset("comment:12", "user", "3")
redis.hset("comment:12", "time", time.time() - 666666)

redis.hset("comment:21", "text", "Good")
redis.hset("comment:21", "upvotes", 628)
redis.hset("comment:21", "user", "1")
redis.hset("comment:21", "time", time.time() - 777777)

redis.hset("comment:22", "text", "Bad")
redis.hset("comment:22", "upvotes", 624)
redis.hset("comment:22", "user", "3")
redis.hset("comment:22", "time", time.time() - 888888)


#ARTICLE COMMENTS 
redis.sadd("aComments:1", "1", "2")

redis.sadd("aComments:2", "1", "2")

#USER COMMENTS 
redis.sadd("uComments:1", "21")

redis.sadd("uComments:2", "11")

redis.sadd("uComments:3", "12", "22")

#USER SUBMISSIONS
redis.sadd("uSubmissions:1", "1")

redis.sadd("uSubmissions:2", "2")

#TOP ARTICLES
redis.zadd("tArticles", 1234, "1")
redis.zadd("tArticles", 4321, "2")

#NEW ARTICLES
redis.zadd("nArticles", time.time() - 333333, "1")
redis.zadd("nArticles", time.time() - 4444444, "2")

#COUNTER
redis.hset("counter", "user", 3)
redis.hset("counter", "comments", 4)
redis.hset("counter", "articles", 2)


#create new user
new_user(redis, 'niki')

#user publishes article
new_article = publish_article(redis, 'niki', 'hi', 'google.com')

print new_article #should return 3

#other user upvotes
article_vote_up(redis, 'article:' + new_article)

#a user comments
new_comment = comment_article(redis, 'user:1', 'article:' + new_article, 'hey')

print new_comment #should return 31: 3rd article 1st comment = 31

#OP upvotes the comment
comment_vote_up(redis, 'comment:' + new_comment)

#user views top ten articles
print return_top_ten(redis) #this line should return [3, 1, 2] 

#user views newest ten articles
print return_new_ten(redis) #this line should return [2, 1, 3]




