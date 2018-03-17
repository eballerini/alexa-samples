"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

import json
import os
import ssl

is_local = os.environ.get('ENV', 'local')
if is_local == 'local':
    import requests
else:
    from botocore.vendored import requests


# --------------- Helpers that build all of the responses ----------------------

def build_add_item_to_list():
    return {
        "outputSpeech": {
          "type": "PlainText",
          "text": "What do you want to add to your to do list?"
        },
        "shouldEndSession": False,
        "directives": [
          {
            "type": "Dialog.ElicitSlot",
            "slotToElicit": "Item",
            "updatedIntent": {
              "name": "AddItemToMyTodoListIntent",
              "confirmationStatus": "NONE",
              "slots": {
                "Item": {
                  "name": "Item",
                  "confirmationStatus": "NONE"
                },
              }
            }
          }
        ]
    }
    
def build_confirm_clear_list():
    return {
            "outputSpeech": {
              "type": "PlainText",
              "text": "Are you sure you want to clear your list?"
            },
            "shouldEndSession": False,
            "directives": [
              {
                "type": "Dialog.ConfirmIntent",
                "updatedIntent": {
                  "name": "ClearMyListIntent",
                  "confirmationStatus": "NONE",
                  "slots": {
                  }
                }
              }
            ]
        }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + output + '</speak>'
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to my To Do list."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what I should add to the list by saying, " \
                    "Add buy groceries"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the To Do list. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def create_item_todo_list_attributes(todo_list):
    return {"todoList": todo_list}
    
def get_current_todo_list(session):
    if session.get('attributes', {}) and "todoList" in session.get('attributes', {}):
        todo_list = session['attributes']['todoList']
    else:
        todo_list = []
    return todo_list
        
def add_item_from_service(intent, session):
    """ Adds an item to the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    # shoud be True
    should_end_session = True
    
    if 'Item' in intent['slots']:
        item = intent['slots']['Item'].get('value')
        # todo_list = get_current_todo_list(session)
        todo_list = []
        if item is None:
            return build_response(create_item_todo_list_attributes(todo_list), build_add_item_to_list())
        else:
            domain = os.environ.get('DOMAIN', 'http://localhost:8000')
            print('domain: {}'.format(domain))
            
            # parse return JSON to create list  
            # url = domain + '/todo/add_item?access_token=' + session.get('user', {}).get('accessToken')
            url = domain + '/todo/add_item'
            payload = {'access_token': session.get('user', {}).get('accessToken')}
            
            response_code = 0
            
            # context = ssl._create_unverified_context()
            # try:
            #     data = json.dumps({'description': str(item)})
            #     req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
            #     # response = urllib2.urlopen(url, context=context)
            #     response = urllib2.urlopen(req, context=context)
            #     response_code = response.getcode()
            #     # response = f.read()
            #     # f.close()
            #     
            #     # response = urllib2.urlopen(url, context=context)
            #     # response_code = response.getcode()
            # except urllib2.HTTPError as e:
            #     print(e)
            
            data = json.dumps({'description': str(item)})
            headers = {}
            response = requests.post(url, data=data, params=payload, headers=headers, verify=False)
            response_code = response.status_code
                
            print('response_code: {}'.format(response_code))
            print('response: {}'.format(response.__dict__))
            if response_code != 204:
                # TODO improve this
                print('cannot process the request')
                return None
            
            # current_attributes = session.get('attributes', {})
            # todo_list.append(item)
            # session_attributes = create_item_todo_list_attributes(todo_list)
            session_attributes = {}
            speech_output = 'I added to your list' \
            '<break time="0.5s"/>' + item
            reprompt_text = "You can add more things to your to do list"
    else:
        speech_output = "I'm not sure what you want to add to your to do list. " \
                        "Please try again."
        reprompt_text = "I'm not sure what you want to add to your to do list. " \
                        "You can add a new item to your to do list by saying, " \
                        "add buy milk."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def _get_domain():
    domain = os.environ.get('DOMAIN', 'http://localhost:8000')
    print('domain: {}'.format(domain))
    return domain
        
def get_todo_list_from_service(intent, session):
    session_attributes = {}
    reprompt_text = None
    
    # matches DOMAIN env var in UI
    domain = os.environ.get('DOMAIN', 'http://localhost:8000')
    print('domain: {}'.format(domain))
    
    # parse return JSON to create list  
    # url = domain + '/todo/list?access_token=' + session.get('user', {}).get('accessToken')
    url = domain + '/todo/list'
    payload = {'access_token': session.get('user', {}).get('accessToken')}
    # TODO improve error handling
    response_code = 0
    # this does not validate the SSL certificate. Don't do this in production!
    # context = ssl._create_unverified_context()
    # try:
        # response = urllib2.urlopen(url, context=context)
    # this does not validate the SSL certificate. Don't do this in production!
    # response = requests.get(url, verify=False)
    response = requests.get(url, params=payload, verify=False)
    response_code = response.status_code
    # print('response: ****')
    # print(response.__dict__)
    # response_code = response.getcode()
    # except urllib2.HTTPError as e:
    #     print(e)
    
    # print('response_code: {}'.format(response_code))
    # print('response: {}'.format(response.__dict__))
    if response_code != 200:
        # TODO improve this
        print('cannot process the request. Response code is: {}'.format(response_code))
        return None

    # data = response.read()
    # data = json.load(response)
    data = response.json()
    # print('data: {}'.format(data))
    
    items = data.get('items', [])

    if len(items) > 0:
        # todo_list = session['attributes']['todoList']
        speech_output = 'On your list you have <break time="0.5s"/>'
        for item in items:
            speech_output += item.get('description') + '<break time="0.5s"/>'
        # TODO modify
        session_attributes = create_item_todo_list_attributes(items)
    else:
        speech_output = "Your to do list is empty."
        
    print('speech output: {}'.format(speech_output))
        
    # should be True
    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def clear_list_from_service(intent, session):
    confirmationStatus = intent.get('confirmationStatus')
    print(f'confirmationStatus: {confirmationStatus}')
    # todo_list = get_current_todo_list(session)
    todo_list = []
    should_end_session = True
    if confirmationStatus == "DENIED":
        session_attributes = create_item_todo_list_attributes(todo_list)
        speech_output = "Ok, I am not clearing the list"
        card_title = speech_output
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))
    elif confirmationStatus == "CONFIRMED":
        session_attributes = {}
        domain = _get_domain()
        url = domain + '/todo/clear_list'
        payload = {'access_token': session.get('user', {}).get('accessToken')}
        
        headers = {}
        response = requests.post(url, params=payload, headers=headers, verify=False)
        response_code = response.status_code
            
        print('response_code: {}'.format(response_code))
        print('response: {}'.format(response.__dict__))
        if response_code != 204:
            # TODO improve this
            print('cannot process the request')
            return None
            
        speech_output = "Ok, your list is cleared"
        card_title = intent['name']
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))
        
    else:
        current_attributes = create_item_todo_list_attributes(todo_list)
        return build_response(current_attributes, build_confirm_clear_list())

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhatIsOnMyTodoListIntent":
        return get_todo_list_from_service(intent, session)
    elif intent_name == "AddItemToMyTodoListIntent":
        return add_item_from_service(intent, session)
    elif intent_name == "ClearMyListIntent":
        return clear_list_from_service(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    skill_id = os.environ.get('SKILL_ID')
    if event['session']['application']['applicationId'] != skill_id:
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
