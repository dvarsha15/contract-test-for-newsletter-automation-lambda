"""
consumer test for contract testing -
to verify the response using mock host

"""


import atexit
import unittest
import requests
from pact import Consumer, Provider

pact = Consumer('Consumer').has_pact_with(Provider('Provider'), pact_dir='./pact')

pact.start_service()
atexit.register(pact.stop_service)

class PostArticleContract(unittest.TestCase):
    
    def test_add_article(self):
        #endpoint
        path='/api/articles'

        #payload
        body={ "Records": 
            [{"body": "{\"Message\":\"{\\\"msg\\\": \\\"Test:https://www.local.com/138/ I am learning contract testing\\\", \\\"chat_id\\\": \\\"19:1941d15dada14943b5d742f2acdb99aa@thread.skype\\\", \\\"user_id\\\":\\\"blah\\\"}\"}"} ] 
            }
        
        #expected response body
        expected_body = {
                            "statusCode": 200,
                            "body": "[\"https://www.local.com/138/\"]"
                        }

        (pact
        .given('a request to add an article')
        .upon_receiving('a response after adding article')
        #.with_request('post', path, body)
        .with_request(
                        method='POST',
                        path= path,
                        body=body,
                        #headers={'Content-Type': 'application/json'},
                     )
        .will_respond_with(200, body=expected_body))

        
        with pact:
            result = requests.post(pact.uri+path, json=body).json()
        
        

        self.assertEqual(result, expected_body)
        
