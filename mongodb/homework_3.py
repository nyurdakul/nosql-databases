import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient()
database = client.test

collection = database.movies

collection.update_many(
	{"genres:" : "Drama", "rated" : "NOT RATED"},
	{"$set": {"rated" : "Pending rating"}})

collection.insert({"title" : "Call me By Your Name",
		   "year" : 2017,
		   "countries" : ["Italy", "France", "Brazil", "USA"],
		   "genres" : ["Drama", "Romance"],
		   "directors" : ["Luca Guadagnino"],
		   "imdb" : {"id" : 5726616, "rating" : 8.0, "votes": 98821}})

dramaCount = collection.aggregate( [
  { "$match": { "genres":  "Drama"} },
  { "$group": { "_id": "Drama", "count": { "$sum": 1 } } }
])

pprint.pprint(list(dramaCount))


turkeyCount = collection.aggregate( [
  { "$match": { "countries":  "Turkey" , "rated" : "Pending rating"}},
  { "$group": { "_id": {"country" : "Turkey", "rated" : "Pending rating"}, "count": { "$sum": 1 } } }
] )

pprint.pprint(list(turkeyCount))

names = database.names
ages = database.ages

names.insert_many([
	{"firstname" : "Nazli", "lastname": "Yurdakul"},
	{"firstname" : "Can", "lastname" : "Akdere"},
	{"firstname" : "Montse", "lastname" : "Pladevall"}
])

ages.insert_many([
	{"name" : "Nazli", "age" : 21},
	{"name" : "Can", "age" : 20},
	{"name" : "Montse", "age" : 19}
])

lookupResult = names.aggregate([
	{"$lookup": {"from" : "ages", "localField" : "firstname", "foreignField" : "name", "as" : "records"}}
])

pprint.pprint(list(lookupResult))



