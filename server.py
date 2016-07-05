import MySQLdb as mdb
import sys
import SimpleHTTPServer, SocketServer
import json
import urlparse
import review_processing

DB_USER = 'root'
DB_PASS = 'root'
DB_NAME = 'reviews'

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/products':
            try:
                con = mdb.connect('localhost', DB_USER, DB_PASS, DB_NAME)
                cur = con.cursor(mdb.cursors.DictCursor)
                cur.execute("SELECT * from product")
                rows = cur.fetchall()

                # print products
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(rows).encode())
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])
                # sys.exit(1)
            finally:
                if con:
                    con.close()

        elif '/product_info' in self.path:
            
            try:
                con = mdb.connect('localhost', DB_USER, DB_PASS, DB_NAME)
                cur = con.cursor()
                query = "SELECT `review_id`, `review` FROM `product_review` WHERE  `is_processed` = 0";
                # print query
                cur.execute(query)
                rows = cur.fetchall()
                # print rows
                review_list=[]
                for row in rows:
                    review_list.append({"text": row[1], "id": row[0]})
                result = review_processing.main(review_list)

                feature_polarity =  result[0]
                reviews = result[1]
                phrase_polarity = result[2]
                phrase_feature = result[3]

                for review in reviews:
                    review_id = str(review['id'])
                    for phrase in review['phrases']:
                        polarity = str(phrase_polarity[phrase])
                        feature = str(phrase_feature[phrase])
                        query_insert = "INSERT into phrases (review_id, phrase, polarity, feature) Values ("+ review_id+ ",'" + phrase +"'," +polarity+ ",'" + feature + "');" 
                        cur.execute(query_insert)
                        con.commit()
                    query_update = "UPDATE product_review SET is_processed=1 WHERE review_id="+review_id+";"
                    cur.execute(query_update)
                    con.commit()

                result = {'status': 'reviews processed successfully'}
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())

            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])
                # sys.exit(1)
            finally:
                if con:
                    con.close()

        elif '/product_results' in self.path:

            product_id = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('id', None)[0]
            print "this is the id:"
            print product_id  # Prints None or the string value of imsi

            try:
                con = mdb.connect('localhost', DB_USER, DB_PASS, DB_NAME)
                cur = con.cursor(mdb.cursors.DictCursor)
                query = "SELECT `review_id`, `review` FROM `product_review` WHERE  `product_id` = " + product_id;
                cur.execute(query)
                rows = cur.fetchall()
                result_review_phrase = []
                for row in rows:
                    review_obj = {}
                    review_obj['id'] = row['review_id']
                    review_obj['review'] = unicode(row['review'], errors = 'replace')
                    query_get_phrase = "SELECT `phrase`, `polarity`, `feature` FROM `phrases` WHERE  `review_id` = " + str(review_obj['id']);
                    cur.execute(query_get_phrase)
                    phrases = cur.fetchall()
                    phrases_list = []
                    for row_phrase in phrases:
                        phrases_list.append({'phrase': unicode(row_phrase['phrase'], errors='replace'), 'polarity':  row_phrase['polarity'], 'feature': unicode(row_phrase['feature'], errors='replace') })
                    review_obj['phrases'] = phrases_list
                    result_review_phrase.append(review_obj)

                query = """select feature, avg(polarity) as polarity from phrases p, product_review r
                            where p.review_id = r.review_id
                            and r.product_id = {p_id}
                            group by feature """.format(p_id = product_id)
                cur.execute(query)
                final_polarity = cur.fetchall()

                result = {'result_review_phrase': result_review_phrase, 'final_polarity': final_polarity }

                # print products
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(result))
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])
                # sys.exit(1)
            finally:
                if con:
                    con.close()

        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

handler = MyHandler
server = SocketServer.TCPServer(("",8901), handler)
print "Server started on port 8901"
server.serve_forever()