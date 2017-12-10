# alexa-samples
Samples for Amazon Alexa

Here is a very simple TODO list.
# To setup
1. `todo-list/alexa-skill.json` is the Alexa skill.
1. `/todo-list/myTodoList/lambda_function.py` is the lambda function to use in AWS. It is written in Python 2.7. This function needs to be hooked up with the Alexa skill.

# To use
Invoke the skill by saying *_wake word_ ask my list*
Then you can say:
 - *What is on my list?* this will tell you what is on your list
 - *Add _something_* Will add _someting_ to the list
 - *Update list* then Alexa should ask you what you want to add. Answer with *_something_*
