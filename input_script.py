import MySQLdb as mdb
import json

DB_USER = 'root'
DB_PASS = 'root'
DB_NAME = 'reviews'


try:

	con = mdb.connect('localhost', DB_USER, DB_PASS, DB_NAME)
	cur = con.cursor()
	input_file = open('sample_data.json' , 'r')
	json_decode = json.load(input_file)

	for product in json_decode:
		name = product["name"]
		size = product["size"]
		price = product["price"]
		brand = product["brand"]
		display = product["display"]
		resolution = product["resolution"]
		weight = product["weight"]
		dimensions = product["dimensions"]
		asin = product["ASIN"]
		image = product["image"]
		query_insert_product = "insert into product (name,size,price,brand,display,resolution,weight,dimensions,ASIN,image) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(name,size,price,brand,display,resolution,weight,dimensions,asin,image)
		cur.execute(query_insert_product)
		product_id = cur.lastrowid
		for review in product["reviews"]:
			query_insert_reviews = "insert into product_review (product_id,is_processed,review) Values (%s, %s, %s)"
			cur.execute(query_insert_reviews, (str(product_id), 0 , review))
		con.commit()


except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    # sys.exit(1)
finally:
    if con:
        con.close()






