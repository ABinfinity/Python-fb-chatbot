# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:48:39 2018

@author: Abinfinity
"""

#Python libraries that we need to import for our bot
import random
import luis
from flask import Flask, request
from pymessenger.bot import Bot
 
app = Flask(__name__)
ACCESS_TOKEN = 'EAAGv7NHBmfUBAFJ6C5doUMRDn8qZCJFybwyHdjzJ2ozGCfysxXviTmBxztseZCn7m7qftPCxYNl594V9XS45rdEyj0WX368M3OaZAdIJj4UUKwr1UgjipnN53GNvFvRLBXntkUz3anOMrh8wiq9FamDN8NuL52v6ZAk7S4cTN2K8rvI2u0rc'
VERIFY_TOKEN = 'ABinfinity'
bot = Bot(ACCESS_TOKEN)
 
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = chatbot(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = chatbot(message['message'].get('attachments'))
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed",200
 
 
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'
 
 
#chooses a random message to send to the user
"""def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)"""
 
#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"
    
    
    
    
def chatbot(message):
    l = luis.Luis(url='https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b497920d-16ae-428e-8768-ae1135679eb0?subscription-key=49f5e5f0839e439a8cd5ef6343345533&verbose=true&timezoneOffset=0&q=')

    ##taking input query
    #query = message

    r = l.analyze(message) ## analysing query
    #print (r.intents)          ##printing intents
    #print (r.entities)         ##printing entities
    best = r.best_intent()         ##printing best intent
    #print (best)


    ##finding best reply using random
    if best.intent == "greeting":
        return random.choice(['Hey, this is RannLab Technologies. How can we help you?',\
                             'Hello, welcome to RannLab Technologies.How can we assist you?'\
                             ,'Good Day, Welcome to RannLab. Please brief your problem.'])
    elif best.intent == "career":
        return random.choice(['It is good to hear from you. Send us your latest resume and we will try to contact you asap',\
                             'RannLab will be lucky to have you in our team. Send us your latest resume and we will try to contact you asap'\
                             ,'RannLab team will always welcome hardworking spirits like you.\
                             Send us your latest resume and we will try to contact you asap'])
    elif best.intent == "idea":
        return random.choice(['Please submit your idea in brief at ideas@rannlab.com, we will try to connect you asap',\
                             'Your idea seems interesting to us. Mail your ideas at ideas@rannlab.com',\
                             'Love to have innovators like you. Mail your ideas at ideas@rannlab.com'])
    elif best.intent == "enquiry":
        return random.choice(['Please mail your query at enquiry@rannlab.com . We will try to resolve it asap',\
                             'Mail at enquiry@rannlab.com to get the status of yor project',\
                             'Submit your query at enquiry@rannlab.com to know the status'])
    elif best.intent == "feedback":
        return random.choice(['Thank you for your feedback','Your feedback will be really helpful to us',\
                             'Would definitly work on your feedback'])
    else :
        return "Invalid Input"
        

 
if __name__ == "__main__":
    app.run()