import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient()
database = client.test

collection = database.movies

#collection.update_many( {"genres:" : "Drama", "rated" : "NOT RATED"}, {"$set": {"rated" : "Pending Rating"}} )

#collection.insert({"title" : "Call me By Your Name",
#		   "year" : 2017,
#		   "countries" : ["Italy", "France", "Brazil", "USA"],
#		   "genres" : ["Drama", "Romance"],
#		   "directors" : ["Luca Guadagnino"],
#		   "imdb" : {"id" : 5726616, "rating" : 8.0, "votes": 98821}})

dramaCount = collection.aggregate( [
  { "$match": { "genres":  "Drama"} },
  { "$group": { "_id": "Drama", "count": { "$sum": 1 } } }
])

pprint.pprint(list(dramaCount))

turkeyCount = collection.aggregate( [
  { "$match": { "countries":  "Turkey", "rated" : "NOT RATED"} },
  { "$group": { "_id": {"country" : "Turkey", "rating" : "NOT RATED"}, "count": { "$sum": 1 } } }
] )

pprint.pprint(list(turkeyCount))
