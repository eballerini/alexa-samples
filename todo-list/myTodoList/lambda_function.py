"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_elicit_slot():
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

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            # 'type': 'PlainText',
            #'text': output
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

# def get_welcome_response_old():
#     """ If we wanted to initialize the session to have some attributes we could
#     add those here
#     """

#     session_attributes = {}
#     card_title = "Welcome"
#     speech_output = "Welcome to the Alexa Skills Kit sample. " \
#                     "Please tell me your favorite color by saying, " \
#                     "my favorite color is red"
#     # If the user either does not reply to the welcome message or says something
#     # that is not understood, they will be prompted again with this text.
#     reprompt_text = "Please tell me your favorite color by saying, " \
#                     "my favorite color is red."
#     should_end_session = False
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to my To Do list. "
                  #  "Please tell me what I should add to the list"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what I should add to the list by saying, " \
                    "Add buy groceries"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the To Do list. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# def create_item_todo_list_attributes(item):
#     return {"todoList": [item]}

def create_item_todo_list_attributes(todo_list):
    # print("create_item_todo_list_attributes")
    # print(todo_list)
    return {"todoList": todo_list}
    
def get_current_todo_list(session):
    if session.get('attributes', {}) and "todoList" in session.get('attributes', {}):
        todo_list = session['attributes']['todoList']
    else:
        todo_list = []
    return todo_list

def add_item_in_session(intent, session):
    """ Adds an item to the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    print('slots: ')
    print(intent['slots'])

    if 'Item' in intent['slots']:
        item = intent['slots']['Item'].get('value')
        print("new item: ")
        print(item)
        todo_list = get_current_todo_list(session)
        if item is None:
            # todo_list = get_current_todo_list(session)
            return build_response(create_item_todo_list_attributes(todo_list), build_elicit_slot())
        else:
            current_attributes = session.get('attributes', {})
            print("current attributes: " + str(current_attributes))
                
            # if session.get('attributes', {}) and "todoList" in session.get('attributes', {}):
            #     todo_list = session['attributes']['todoList']
            # else:
            #     todo_list = []
            print("current # of items: " + str(len(todo_list)))
            # print("my todoList before: ")
            # for item_before in todo_list:
            #     print(item_before)
            todo_list.append(item)
            # print("updated_list")
            # print(todo_list)
            session_attributes = create_item_todo_list_attributes(todo_list)
            # print(session_attributes)
            # todo_list_after = session['attributes']['todoList']
            # print("my todoList after: ")
            # for item2 in session_attributes.get('todoList'):
            #     print(item2)
            # print("----")
            # speech_output = item + " has been added to your to do list"
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
        
def get_todo_list_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "todoList" in session.get('attributes', {}):
        # todo_list = session['attributes']['todoList']
        # speech_output = 'On your to do list you have <break time="1s"/>' + todo_list
        # TODO make it a list
        todo_list = session['attributes']['todoList']
        speech_output = 'On your list you have <break time="0.5s"/>'
        for item in todo_list:
            speech_output += item + '<break time="0.5s"/>'
        # should_end_session = False
        session_attributes = create_item_todo_list_attributes(todo_list)
    else:
        speech_output = "Your to do list is empty."
        
    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
# def set_color_in_session(intent, session):
#     """ Sets the color in the session and prepares the speech to reply to the
#     user.
#     """

#     card_title = intent['name']
#     session_attributes = {}
#     should_end_session = False

#     if 'Color' in intent['slots']:
#         favorite_color = intent['slots']['Color']['value']
#         session_attributes = create_favorite_color_attributes(favorite_color)
#         speech_output = "I now know your favorite color is " + \
#                         favorite_color + \
#                         ". You can ask me your favorite color by saying, " \
#                         "what's my favorite color?"
#         reprompt_text = "You can ask me your favorite color by saying, " \
#                         "what's my favorite color?"
#     else:
#         speech_output = "I'm not sure what your favorite color is. " \
#                         "Please try again."
#         reprompt_text = "I'm not sure what your favorite color is. " \
#                         "You can tell me your favorite color by saying, " \
#                         "my favorite color is red."
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))


# def get_color_from_session(intent, session):
#     session_attributes = {}
#     reprompt_text = None

#     if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
#         favorite_color = session['attributes']['favoriteColor']
#         speech_output = "Your favorite color is " + favorite_color + \
#                         ". Goodbye."
#         should_end_session = True
#     else:
#         speech_output = "I'm not sure what your favorite color is. " \
#                         "You can say, my favorite color is red."
#         should_end_session = False

#     # Setting reprompt_text to None signifies that we do not want to reprompt
#     # the user. If the user does not respond or says something that is not
#     # understood, the session will end.
#     return build_response(session_attributes, build_speechlet_response(
#         intent['name'], speech_output, reprompt_text, should_end_session))





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
    # if intent_name == "MyColorIsIntent":
    #     return set_color_in_session(intent, session)
    # elif intent_name == "WhatsMyColorIntent":
    #     return get_color_from_session(intent, session)
    if intent_name == "WhatIsOnMyTodoListIntent":
        return get_todo_list_from_session(intent, session)
    elif intent_name == "AddItemToMyTodoListIntent":
        return add_item_in_session(intent, session)
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
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
