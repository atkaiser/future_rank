# Future Tennis Rank

## About

The code here is for the website at www.futuretennisrank.com.  Code within the scripts directory is for getting data off the ATP world tour website, such as the current rankings and the draws for upcoming tournaments.  Files in the static folder are for the javascript used to run the site.  And finally files in the server directory are for actually serving the site.

## Getting started

Run (with python3):

	pip install -r requirements.txt
	npm install
	npm install -g gulp
	cd scripts; python generate_data.py > ../static/js/data.js
	cd ..
	gulp css
	gulp js
	python runserver.py
	
## Contributing

If you find a bug or want to contribute feel free to submit a pull request or log an issue.