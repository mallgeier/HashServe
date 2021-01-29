import requests
import json
import hashlib
import subprocess
import os
import pytest
from requests import HTTPError


#set $PORT environment variable
os.environ['PORT'] = '8088'

#launch API

subprocess.Popen('C:\\Users\\Mike\\hashserve\\broken-hashserve_win.exe')

#set some variables
url 		=	"http://127.0.0.1:8088/hash"
headers 	=	{'Content-Type': "application/json"}
input 		= 	'angrymonkey'
input2 		= 	'disgruntledorangutan'
input3 		=	'orneryape'
input4		=	'grouchygorilla'
payload 	= 	{'password': input}
payload2 	=	{'password': input2}
payload3 	=	{'password': input3}
payload4 	=	{'password': input4}

#Testing class
class TestHash:
	
	
	def test_hash_create_valid_resp200(self):

		# convert dict to json string by json.dumps() for body data. 
		resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       

		assert resp.status_code == 200
		# Validate response text
		assert resp.text == '1'
		# print(resp.text)
    
	def test_hash_pw_empty_payload(self):
		#url = "http://127.0.0.1:8088/hash"
		#headers = {'Content-Type': "application/json"}
		payload = ""
		
		
		# convert dict to json string by json.dumps() for body data. 
		resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
		
		# Validate response 400 for empty payload
		assert resp.status_code == 400
		
		#print(resp.text)   

	def test_hash_pw_valid(self):
		url = "http://127.0.0.1:8088/hash/1"
		#headers = {'cache-control': "no-cache"}
		payload = ""
	
		
		response = requests.request("GET", url, data=payload, headers=headers)
		assert response.status_code == 200
		#calculate expected hash value for input
		hash = hashlib.sha512( str( input ).encode("utf-8") ).hexdigest()
		
		# validate password is corresponding sha512
		assert hash == response.text    
 

	def test_hash_pw_get_no_identifier_405(self):
		url = "http://127.0.0.1:8088/hash"
		payload = ""
						
		#Get without identifier returns 405 
		response = requests.request("GET", url, data=payload, headers=headers)
		assert response.status_code == 405

	def test_hash_pw_delete_405(self):
		url = "http://127.0.0.1:8088/hash/1"
		payload = ""
						
		#delete returns 405 
		response = requests.request("delete", url, data=payload, headers=headers)
		assert response.status_code == 405


	def test_hash_stats_valid(self):
		url = "http://127.0.0.1:8088/stats"
		payload = ""
						
		
		response = requests.request("GET", url, data=payload, headers=headers)
		response_body = response.json()
		#validate response code 200, total requests is 2 and average time is greater than 5 given spec delay
		
		
		assert response.status_code == 200
		assert response_body["TotalRequests"] == 2
		assert response_body["AverageTime"] >= 5
		
		
	
	def test_shutdown_with_simultaneous_active(self):

		# more calls
		resp2 = requests.post(url, headers=headers, data=json.dumps(payload2,indent=4))       
		resp3 = requests.post(url, headers=headers, data=json.dumps(payload3,indent=4))
						
		#shutdown call immediately after post for new 
		response2 = requests.request("POST", url, data="shutdown", headers=headers)
		
		#validate shutdown response code
		assert response2.status_code == 200
		#validate proper completion for waiting calls finish
		assert resp2.status_code == 200
		assert resp2.text == '2'
		assert resp3.status_code == 200
		assert resp3.text == '3'
		
		#attempt another call after shutdown called
		try:
		   #requests.get('http://www.google.com')
		   requests.post(url, headers=headers, data=json.dumps(payload3,indent=4))
		   assert 0
		except requests.ConnectionError:
		   #print('expected')
		   assert 1
