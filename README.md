# Tweet Scraper

## This script can pull up to 3200 tweets of any given user

### Install dependencies:

`$ pip install -r requirements.txt`

### To set your enviornment variables in your terminal run the following line:
`$ export 'BEARER_TOKEN'='<your_bearer_token>'`

### Sample execution:

`$ python main.py --username elonmusk`

All tweet data will be stored in a json file which will be named `<username>.json`