import os

mongo_atlas_pw = os.getenv('mongo_atlas_pw')
google_app_pw = os.getenv('google_app_pw')

# mailer
mailcfg = {
	"fromaddr" : "kinghuskier@gmail.com",
	"fromname" : "Kindle++",
	"toaddr" : "\
					patwa.r@husky.neu.edu, \
					patni.a@husky.neu.edu, \
					dedhia.da@husky.neu.edu, \
					gandhi.ruc@husky.neu.edu, \
					jain.shub@husky.neu.edu, \
					mohitpatwa@gmail.com, \
					janhavihkarekar@gmail.com, \
					harshit158@gmail.com, \
					jain95aastha@gmail.com, \
					jainrachita15@gmail.com, \
					patwa.prerna@gmail.com, \
					bothra.sa@northeastern.edu, \
					saloni.jain.official@gmail.com",

	"psswd" : google_app_pw
}



# mongo connection
mongo = {
	"serveraddr_old":f"mongodb+srv://rohit:{mongo_atlas_pw}@rohit-mongo-scv25.mongodb.net/test?retryWrites=true&w=majority",
	"serveraddr":f"mongodb+srv://rohit:{mongo_atlas_pw}@cluster0-zzgfx.mongodb.net/test?retryWrites=true&w=majority",
	"dbname":"kindle",
}