# getInfo libraries
import random
import csv
import json
import requests
from random import randint
from time import sleep

def detailed_info():
	json_format="/?__a=1"

	file= open("./data/instagram/followers.txt", 'r') 
	f=open("./data/instagram/user-data.csv", 'wb')
	writer=csv.writer(f, delimiter=',')
	writer.writerow(['Full Name','Biography','Followers Count','Following Count','ID', 'User Name', 'Media', 'Profile Link'])
	for line in file:
		url="https://www.instagram.com/"+line.strip()+json_format
		print url
		try:
			sleep(randint(3,7)) # random sleep for avoiding back to back requests
			data = requests.get(url).json()
			full_name= data['user']['full_name'] # Full_Name
			biography= data['user']['biography'] #Biography
			followed_by=data['user']['followed_by']['count'] # followers count
			follows= data['user']['follows']['count'] # following count
			user_id =data['user']['id'] # Insta ID count
			username=data['user']['username']# username
			media_count= data['user']['media']['count']# Media count
			writer.writerow([full_name,biography,followed_by,follows,user_id,username,media_count])
		except ValueError:
			pass