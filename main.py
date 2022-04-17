import os
import sys
import time
import json
import argparse
import requests

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url_user(username):
	# Specify the usernames that you want to lookup below
	# You can enter up to 100 comma-separated values.
	usernames = f"usernames={username}"
	user_fields = "user.fields=description,created_at,id,name"
	# User fields are adjustable, options include:
	# created_at, description, entities, id, location, name,
	# pinned_tweet_id, profile_image_url, protected,
	# public_metrics, url, username, verified, and withheld
	url = f"https://api.twitter.com/2/users/by?{usernames}&{user_fields}"
	return url


def create_url_tweets(id, pagination_token='', exclude='retweets,replies'):
	tweet_fields = "tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld"
	url = f"https://api.twitter.com/2/users/{id}/tweets?max_results=100&exclude={exclude}&{tweet_fields}"
	if pagination_token != '':
		url = f"{url}&pagination_token={pagination_token}"
	return url


def bearer_oauth(r):
	"""
	Method required by bearer token authentication.
	"""

	r.headers["Authorization"] = f"Bearer {bearer_token}"
	r.headers["User-Agent"] = "v2UserLookupPython"
	return r


def connect_to_endpoint(url):
	response = requests.request("GET", url, auth=bearer_oauth,)
	print(response.status_code)
	if response.status_code != 200:
		raise Exception(
			"Request returned an error: {} {}".format(
				response.status_code, response.text
			)
		)
	return response.json()


def get_all_tweets(user_id):
	count = 0
	next_token = ''
	all_tweets = list()
	while True:
		if count == 0:
			json_response = connect_to_endpoint(create_url_tweets(user_id))
			tweets = json_response["data"]
			meta_data = json_response["meta"]
			all_tweets.extend(tweets)			
			if "next_token" in meta_data:
				next_token = meta_data["next_token"]
				count += 1
			else:
				break
		else:
			json_response = connect_to_endpoint(create_url_tweets(user_id, pagination_token=next_token))
			tweets = json_response["data"]
			meta_data = json_response["meta"]
			all_tweets.extend(tweets)
			if "next_token" in meta_data:
				next_token = meta_data["next_token"]
			else:
				break
		time.sleep(.5)
	return all_tweets



def main():
	parser=argparse.ArgumentParser(
    description="This script retrieves up to 3200 tweets of a given user.")
	parser.add_argument('--username', type=str, required=True)
	args=parser.parse_args()
	try:
		url = create_url_user(args.username)
		user_data = connect_to_endpoint(url)["data"][0]
		user_id = user_data["id"]
		tweets = get_all_tweets(user_id)
		# print(tweets, len(tweets))
		with open(f"{args.username}.json", "w") as outfile:
			json.dump(tweets, outfile)
	except Exception as e:
		print(e)
		sys.exit(1)


if __name__ == "__main__":
	main()