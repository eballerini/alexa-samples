# alexa-samples
Samples for Amazon Alexa

Here is a very simple TODO list.
# To setup - standalone skill
1. `/todo_list/alexa-skill.json` is the Alexa skill.
1. `/todo_list/lambda_function_standalone.py` is the lambda function to use in AWS. It needs Python 2.7. This function needs to be hooked up with the Alexa skill.
1. Configure a `SKILL_ID` environment variable. This is the Alexa skill id.

# To setup - connected skill
1. `/todo_list/alexa-skill.json` is the Alexa skill.
1. `/todo_list/lambda_function_connected.py` is the lambda function to use in AWS. It needs Python 3.6. This function needs to be hooked up with the Alexa skill.
1. Configure a `SKILL_ID` environment variable. This is the Alexa skill id.
1. Configure a `ENV` environment variable and set it to 'cloud'. This is necessary to that AWS lambda can import the proper `requests` module.
1. Configure a `DOMAIN` environment variable. This should point to the instance where the app is running, e.g. https://ec2-34-203-214-254.compute-1.amazonaws.com:8000

# To use
Invoke the skill by saying *_wake word_ open my custom list*. For instance *Alexa open my custom list*.
Then you can say:
 - *What is on my list?* this will tell you what is on your list
 - *Add _something_* Will add _someting_ to the list. Try something like _buy groceries_ or _prepare dinner_ (it is limited to what is configured in the Alexa model).
 - *Update list* then Alexa should ask you what you want to add. Answer with *_something_*
 - *Clear the list* you will be asked for confirmation
