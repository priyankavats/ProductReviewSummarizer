import urllib
import urllib2
import json
import requests

STANFORD_PARSER_SERVER = "http://localhost:8080/stanford_parser_desktop/"

def main(phrase, feature):

	temp_list = []
	params =  { 'text': phrase }
	data_parser = requests.post(STANFORD_PARSER_SERVER, params = params)
	try:
		data_parser2 = json.loads(data_parser.text)
		temp_list.append(data_parser2)

		#---------------
		for row in temp_list:
			for word in row['list']:
				if len(word['pos']) == 3:
					for tag in word['pos']:
						if tag['word'] != feature:
							if tag['tag']=="VB" or "NN":
								temp =  tag['word']
								phrase = feature + " does not " + temp
							if tag['tag'] == "JJ":
								temp = tag['word']
								phrase = "does not have " + temp + " " + feature
				if len(word['pos']) == 4:
					for tag in word['pos']:
						if tag['word'] != feature:
							if tag['tag'] == "JJ":
								temp = tag['word']
								phrase = "does not have " + temp + " " + feature  
							if tag['tag'] == "NN":
								feature_new = feature + " " + tag['word']
								print "-------"
								for tag1 in word['pos']:
									if tag1['word'] != feature:
										if tag1['tag'] == "VB":
											temp = tag1['word']
											phrase = feature_new + " does not " + temp
		print phrase
		return phrase				



	except Exception:
		pass
	return temp_list

if __name__ == "__main__":
	main(phrase,feature)
	# main("not sharp settings", "settings")