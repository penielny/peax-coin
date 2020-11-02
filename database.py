from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
database = client.peaxcoin

# users :[{
# 	"email":"pe@mial.com",
# 	"password":"xxxxxxxxxxx",
# 	"private_key":"xxx-x-xx-xx-xxx-x",
# 	account:{
# 	"tokens":"0.003"
# 	},
# 	keys:[
# 		"xxxxxxxxxxxxxxxxx"
# 	],
# }]

# transaction :[
	# {
	# 	"id": "xxxxxxxxxxxxxxxxx",
	# 	"date":"12-3-33",
	# 	"token" : "-0.000004",
	# 	"recv_wallet":"xxx-xxx-xxxx-xxx-xx"
	# 	"confirmation" : 10,
	# 	"comment" : "safe and reliable",
	# 	"sender_wallet":"xxxxxxxxxxxx"
	# }
# ]