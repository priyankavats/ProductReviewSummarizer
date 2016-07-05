import urllib
import urllib2
import json
import requests


STANFORD_PARSER_SERVER = "http://localhost:8080/stanford_parser_desktop/"


def main(review_list):

	complete_list = []

	for review in review_list:
		    review_edited = review['text'].replace(
		        "!", ".").replace("\n\n", " ").replace("...", ".").replace(".", ". ").lower()
		    params =  { 'text': review_edited }
		    data_parser = requests.post(STANFORD_PARSER_SERVER, params = params)
		    try:
		        data_parser2 = json.loads(data_parser.text)
		        data_parser2['id'] = review['id']
		        complete_list.append(data_parser2)
		    except Exception:
		        pass
	return complete_list

if __name__ == "__main__":
	main(review_list)