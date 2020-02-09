import flask
from flask import jsonify, request
from pymongo import MongoClient
from config import mongo
import hashlib

app = flask.Flask(__name__)
app.config["DEBUG"] = True

client = MongoClient(mongo['serveraddr'])
db = client[mongo['dbname']]



@app.route('/books', methods=['GET'])
def home():
	cursor = db['books'].find().limit(100)
	books = []
	for doc in cursor:
		books.append(doc)
	return jsonify({"data":books, "status_code":200})



@app.route('/subscribe', methods=['GET', 'POST']) 
def subscribe(): 
	""" 
		Upload image with base64 
	"""

	data = request.get_json()

	if data is None:
	  print("No valid request body, json missing!")
	  return jsonify({'error': 'No valid request body, json missing!', 'status_code':101})
	else:

		name = data['name']
		email = data['email']
		books = data['book_ids']

		try:
			name = name.strip()
			email = email.lower().strip()
			email_hash = hashlib.md5(email.encode('UTF-8')).hexdigest() 
			doc = {
					"_id" : email_hash,
					"name": name,
					"email" : email,
					"contributions" : [],
					"subscriptions" : books,
					'reading_quality': 0,
					'frequency':0,
					'active':1
				}
			db['users'].insert_one(doc)
			return jsonify({'message': 'User added successfully!', 'status_code':200})
		
		except Exception as e:
			if '_id_ dup key' in str(e):
				return jsonify({'error': 'User already exists', 'status_code':101})
			return jsonify({'error': 'Unable to add user, please insert data correctly', 'status_code':101})


@app.route('/unsubscribe', methods=['GET', 'POST']) 
def unsubscribe(): 
	""" 
		Upload image with base64 
	"""

	data = request.get_json()

	if data is None:
		print("No valid request body, json missing!")
		return jsonify({'error': 'No valid request body, json missing!', 'status_code':101})
	else:

		email = data['email']
		email = email.lower().strip()
		email_hash = hashlib.md5(email.encode('UTF-8')).hexdigest() 
		try:
			db['users'].update_one({"_id":email_hash}, {"$set":{"active":0}})
			return jsonify({'message': 'User unsubscribed successfully', 'status_code':200})
		
		except Exception as e:
			if '_id_ dup key' in str(e):
				return jsonify({'error': 'User already exists', 'status_code':101})
			return jsonify({'error': 'Unable to add user, please insert data correctly', 'status_code':101})

			
app.run(host="0.0.0.0")



# @app.route('/upload', methods=['POST']) 
# def upload_base64_file(): 
# 	""" 
# 		Upload image with base64 
# 	"""

# 	data = request.get_json()

# 	if data is None:
# 	  print("No valid request body, json missing!")
# 	  return jsonify({'error': 'No valid request body, json missing!'})
# 	else:

# 	  img_data = data['img']

# 	  # this method convert and save the base64 string to image
# 	  convert_and_save(img_data)
# 	  return "ho gaya"




# def convert_and_save(b64_string):

# 	b64_string += '=' * (-len(b64_string) % 4)  # restore stripped '='s

# 	string = b'{b64_string}'

# 	with open("tmp/imageToSave.png", "wb") as fh:
# 		fh.write(base64.decodebytes(string))
	  # this method convert and save the base64 string to image
		  # this method convert and save the base64 string to image
	  # convert_and_save(img_data)
	  # return "ho gaya"




