from unittest import TestCase
import mock
from mock import patch, Mock
import os

from ..lambda_function_connected import lambda_handler

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

def mocked_requests_get(*args, **kwargs):
    return MockResponse({"items": [{"description": "prepare dinner", "completed": False}]}, 200)
    
def mocked_requests_post(*args, **kwargs):
    return MockResponse({}, 204)

@mock.patch.dict(os.environ, {'SKILL_ID':'my_skill', 'DOMAIN': 'http://localhost:8000'})
class MyTestCase(TestCase):    

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_what_is_on_my_list__success(self, mock_get):
        # mocked_response = Mock()
        # mocked_response.read.side_effect = [ {"items": [{"description": "prepare dinner", "completed": False}]} ]
        # mocked_response.getcode.return_value = 200
        # mock_urlopen.return_value = mocked_response
        # mocked_response = Mock()
        # mocked_response.side_effect = MockResponse({"items": [{"description": "prepare dinner", "completed": False}]}, 200)
        # # mock_urlopen.get.return_value = [ {"items": [{"description": "prepare dinner", "completed": False}]} ]
        # mock_get.return_value = mocked_response
        
        expected_result = {
            'version': '1.0', 
            'response': {
                'outputSpeech': {
                    'ssml': '<speak>On your list you have <break time="0.5s"/>prepare dinner<break time="0.5s"/></speak>', 
                    'type': 'SSML'
                }, 
                'shouldEndSession': True, 
                'reprompt': {
                    'outputSpeech': {
                        'text': None, 
                        'type': 'PlainText'
                    }
                }, 
                'card': {
                    'content': 'SessionSpeechlet - On your list you have <break time="0.5s"/>prepare dinner<break time="0.5s"/>', 
                    'type': 'Simple', 
                    'title': 'SessionSpeechlet - WhatIsOnMyTodoListIntent'
                }
            }, 
            'sessionAttributes': {
                'todoList': [{
                    'completed': False, 
                    'description': 'prepare dinner'
                }
            ]}
        }
        context = {}
        event = {
            'session': {
                'new': False,
                'sessionId': '190',
                'application': {
                    'applicationId': 'my_skill',
                },
                'user': {
                    'accessToken': 'abc',
                }
            },
            'request': {
                'type': 'IntentRequest',
                'requestId': '123',
                'intent': {
                    'name': 'WhatIsOnMyTodoListIntent',
                },
            }
        }
        
        result = lambda_handler(event, context)
        print('result: {}'.format(result))
        self.assertIsNotNone(result)
        self.assertEquals(expected_result, result)
        
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_add_item_to_my_list__success(self, mock_post):
        expected_result = {
            'version': '1.0', 
            'sessionAttributes': {},
            'response': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': '<speak>I added to your list<break time="0.5s"/>buy apples</speak>'
                }, 
                'card': {
                    'type': 'Simple', 
                    'title': 'SessionSpeechlet - AddItemToMyTodoListIntent',
                    'content': 'SessionSpeechlet - I added to your list<break time="0.5s"/>buy apples',
                },
                'reprompt': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'You can add more things to your to do list',
                    }
                }, 
                'shouldEndSession': True,
            }
        }
        event = {
            'session': {
                'new': False,
                'sessionId': '190',
                'application': {
                    'applicationId': 'my_skill',
                },
                'user': {
                    'accessToken': 'abc',
                }
            },
            'request': {
                'type': 'IntentRequest',
                'requestId': '123',
                'intent': {
                    'name': 'AddItemToMyTodoListIntent',
                    'slots': {
                        'Item': {
                            'value': 'buy apples',
                        }
                    }
                },
            }
        }
        context = {}
        result = lambda_handler(event, context)
        self.assertIsNotNone(result)
        self.assertEquals(expected_result, result)
        
        
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_clear_list__success(self, mock_post):
        expected_result = {
            'version': '1.0', 
            'sessionAttributes': {},
            'response': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': '<speak>Ok, your list is cleared</speak>'
                }, 
                'card': {
                    'type': 'Simple', 
                    'title': 'SessionSpeechlet - ClearMyListIntent',
                    'content': 'SessionSpeechlet - Ok, your list is cleared',
                },
                'reprompt': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'Ok, your list is cleared',
                    }
                }, 
                'shouldEndSession': True,
            }
        }
        actual = {
            'version': '1.0', 
            'sessionAttributes': {}, 
            'response': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': '<speak>Ok, your list is cleared</speak>'
                }, 
                'card': {
                    'type': 'Simple', 
                    'title': 'SessionSpeechlet - ClearMyListIntent', 
                    'content': 'SessionSpeechlet - Ok, your list is cleared'
                }, 
                'reprompt': {
                    'outputSpeech': {
                        'type': 'PlainText', 
                        'text': 'Ok, your list is cleared'
                    }
                }, 
                'shouldEndSession': True
            }
        }
        event = {
            'session': {
                'new': False,
                'sessionId': '190',
                'application': {
                    'applicationId': 'my_skill',
                },
                'user': {
                    'accessToken': 'abc',
                }
            },
            'request': {
                'type': 'IntentRequest',
                'requestId': '123',
                'intent': {
                    'name': 'ClearMyListIntent',
                    'confirmationStatus': 'CONFIRMED',
                    # 'slots': {
                    #     'Item': {
                    #         'value': 'buy apples',
                    #     }
                    # }
                },
            }
        }
        context = {}
        result = lambda_handler(event, context)
        self.assertIsNotNone(result)
        self.assertEquals(expected_result, result)
        