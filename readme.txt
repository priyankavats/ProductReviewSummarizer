Project Requirements:
- Python 2.7
- Python package MySQLdb (pip install MySQLdb)
- Java 1.7+
- Any web server capable to run Java projects (Tomcat, Jetty etc)
- MySql 5+
- Internet connection to connect to AlchemyAPI

Project Structure:
- stanford-parser: The stanford parser models are loaded here. All the logic specific
to the app is in servlets.UniversalDependencies
- alchemyapi_python: The alchemy api python wrapper
- api_key.txt: Contains the alchemy api key. If key gets rate limited running the system,
you can issue a new key and paste it in the text file (http://www.alchemyapi.com/api/register.html)
- server.py: The python server which calls the python modules as well as the Java Server web url for processing
- index.html: The ui file with JavaScript logic
- input_script.py: Contains the script to load reviews into the DB
- sample_data.json: When input_script is run, this is the file whose data is loaded into the db.
- reviews.sql: Existing reviews database. 
- generalwords.csv: Contains words which are not processed as features by the system

How to run the application:
- Install MySQL and create a new DB called "reviews"
- Import reviews.sql file to that DB
- Based on your credentials modify the DB_NAME, DB_USER, DB_PASS constansts in input_script.py
and server.py
- Run stanford-parser. I used run-jetty-run with eclipse (import existing maven project into eclipse)
- Based on your Java server configuration change the url, change the STANFORD_PARSER_SERVER url in 
not_words.py and get_complete_list.py
- Run server. Default config starts the server in localhost:8091
- Opening this url loads the index.html page in your browser.
- To process unprocessed reviews, you can go to http://localhost:8901/product_info in any browser