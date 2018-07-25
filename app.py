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
import json
import requests
import pymysql

 
app = Flask(__name__)
ACCESS_TOKEN = 'EAAGv7NHBmfUBAGuVjC2q7jXQIh1ZC8inZCZAbRwfMuZARVyR1kNcH0GkV5Pvc3VzwoidqMZCU29ttpeP9Wy7dVnuRGfaOOrZBTLL7vUIWq32cQMcD2fNZBwmDZC0ysOgkA2877OiMLVyjwYXA7O9SugPv1QvdlCfE8BI8GUxDyasnxxvWicYBZCpM'
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
                    response_sent_text = chatbot(message['message'].get('text'),recipient_id)
                    send_message(recipient_id, response_sent_text)
                # else:
                #     send_message(recipient_id,"Sorry I don't talk this way , but i will think about it ;)")
                
    return "Message processed",200
 
 
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'
 
 
#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"
    
    
    
    
def chatbot(message,recipient_id):
    l = luis.Luis(url='https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/641864d4-9a31-4172-9532-840a8f38aea0?subscription-key=c250fdf3697543e48f1e6c86e6819593&verbose=true&timezoneOffset=0&q=')

    r = l.analyze(message) ## analysing query
    #print (r.intents)          ##printing intents
    #print (r.entities)         ##printing entities
    best = r.best_intent()         ##printing best intent
    #print (best)


    ##finding best reply using random
    if best.score>0.8 :
        if best.intent == "greeting":
            send_message(recipient_id, random.choice(['Hey Samaira this side. :)','Hello, I am Samaira. :)','Good Day,my name is Samaira. :)']))
            send_message(recipient_id, random.choice(["ok","hmm"]))
            send_message(recipient_id, random.choice(["What can I do for you?","How can I assist you?","How can I help you?."]))
            send_message(recipient_id, random.choice(["I can help you with career in Rannlab along with its services"]))
           
        elif best.intent == "career" :
            send_message(recipient_id,random.choice(["Ok, so you are looking for a job.. :D","Hmm...so you want a job :D","That gud...you are looking for a job :D"]))
            send_message(recipient_id,random.choice(["for which profile you want to apply?","Do you have any specific profile in mind?", "What is your choice of profile?"]))
        
        elif best.intent == "intern" :
            send_message(recipient_id,random.choice(["ok..","sure.."]))
            send_message(recipient_id,"we provide internship for the following period")
            send_message(recipient_id,"45 days (unpaid)")
            send_message(recipient_id,"3 months (unpaid)")
            send_message(recipient_id,"6 months (performance based)")
            send_message(recipient_id,"If you are interested, you can send your resume at hr@rannlab.com")
            send_message(recipient_id,"I'm sure you will learn a bunch of cool stuffs here :)")
            send_message(recipient_id,random.choice(["Do you need any other help?","Anything else I can do for you?","Is there something else I can do for you?","Anything else you wanted to know?"]))

        elif best.intent == "idea":
            send_message(recipient_id,random.choice(["Oo I like intellectual peeps (y)","Nice, very few people have that kind of spirit (y)"]))
            send_message(recipient_id,random.choice(["I'm sure our team will help to bring your idea to reality O:-)"]))
            send_message(recipient_id,random.choice(['Please submit your idea in brief at info@rannlab.com, we will try to connect you asap','Your thought seems interesting to us. Mail your ideas at info@rannlab.com','Love to have innovators like you. Mail your ideas at info@rannlab.com']))
            send_message(recipient_id,random.choice(["Do you need any other help?","Anything else I can do for you?","Is there something else I can do for you?","Anything else you wanted to know?"]))
        

        elif best.intent == "enquiry":
            send_message(recipient_id,random.choice(['Please mail your query at info@rannlab.com . We will try to resolve it asap','Mail at info@rannlab.com to get the status of yor project','Submit your query at info@rannlab.com to know the status']))
            send_message(recipient_id,random.choice(["Do you need any other help?","Anything else I can do for you?","Is there something else I can do for you?","Anything else you wanted to know?"]))
       

        elif best.intent == "feedback":
            send_message(recipient_id,random.choice(['Thank you for your feedback','Your feedback will be really helpful to us','Would definitly work on your feedback']))
            
            send_message(recipient_id,random.choice(["Do you need any other help?","Anything else I can do for you?","Is there something else I can do for you?","Anything else you wanted to know?"]))
        

        elif best.intent == "profile" :
            send_message(recipient_id,random.choice(["I always wanted to be one but I can never make it out of the screen ;p","Nice, it is currently in demand also. (y)"]))
            send_message(recipient_id,random.choice(['It is good to hear from you. :)','RannLab will be lucky to have you in our team. :)','RannLab team will always welcome hardworking spirits like you. :)']))
            send_message(recipient_id,random.choice(["Send us your latest resume or cv at hr@rannlab.com mentioning the desired profile and we will try to contact you asap","Mail us your latest resume or cv at hr@rannlab.com mentioning the desired profile and we will try to contact you asap"]))
            send_message(recipient_id,random.choice(["Do you need any other help?","Anything else I can do for you?","Is there something else I can do for you?","Anything else you wanted to know?"]))
        

        elif best.intent == "positive" :
            send_message(recipient_id, random.choice(["Please ask your query..I would love to help you.","Please ask, I am open to help"]))
        
        elif best.intent == "bye":
            send_message(recipient_id,random.choice(["^_^",":)",":D","(y)"]))
        elif best.intent == "thank you":
            send_message(recipient_id,random.choice(["Anytime my friend :)"," :)","Anytime :)"]))

        elif best.intent == "negative" :
            send_message(recipient_id,random.choice(["ok, it was good talking to you ^_^","It was nice talking to you ^_^"]))
            visit_button(recipient_id)
            call_button(recipient_id)
            send_message(recipient_id,random.choice(["Also like our page and don't forget to hit subscribe button if you don't want to miss any future job updates","And hey, don't forget to hit like and subscribe if you don't want to miss any job updates"]))
            send_message(recipient_id, random.choice(["bye :D","gud bye :D","namaste :)","ok byee :D"]))    
            return "Message processed",200

        elif best.intent == "services":
            send_message(recipient_id,random.choice(["Hmm.. let's see","Ok, let's have a look","Wait let me see.."]))
            send_message(recipient_id,"We provide services in..")
            send_message(recipient_id," Ecommerce development")
            send_message(recipient_id," Digital marketing")
            send_message(recipient_id," Hosting and cloud support")
            send_message(recipient_id," Software development")
            send_message(recipient_id," Website design and development")
            send_message(recipient_id," Mobile app development")
            send_message(recipient_id," Content Management")
            send_message(recipient_id," IT infrastructure")
            send_message(recipient_id,random.choice(["which service are you specifically looking??","which one of the service do you want from us?"]))
        
        elif best.intent == "spec_service":
            send_message(recipient_id,"In that case..we would like to have a talk with you")
            send_message(recipient_id,"Call us on our number..")
            call_button(recipient_id)
            send_message(recipient_id,"Or just leave a mail at info@rannlab.com")
            send_message(recipient_id,random.choice(["Do you need any other help?","Anything else I can do for you?","Is there something else I can do for you?","Anything else you wanted to know?"]))

        elif best.intent == "call":
            send_message(recipient_id,random.choice(["we are just a call away...","our services are just a call away"]))
            call_button(recipient_id)

        elif best.intent == "address" :
            send_message(recipient_id,random.choice(["you can find us at","our office is located at", "the address of our office is"]))
            send_message(recipient_id,"805, 8th Floor, Om Tower, Alpha-I Commercial Belt, Block E, Alpha I, Greater Noida, Uttar Pradesh 201310")
            send_message(recipient_id,"Fell free to come... :)")
            send_message(recipient_id,"but only in between 10 to 6")
            send_message(recipient_id,"unless you wanted to rob our tower... :D ")

        elif best.intent == "about" :
        	send_message(recipient_id,"Let me tell you about my company..")
        	send_message(recipient_id,"RannLab Technologies Pvt. Ltd. provides customized IT solutions, website design and many Software products.")
        	send_message(recipient_id,"Our Vision is to provide top quality services in the fields of ERP Solutions, Mobile Application Development, Open Source Customization, Computer software development and Web Designing everything under one-roof.")
        	visit_button(recipient_id)



        else :
            send_message(recipient_id,random.choice(["I don't understand what you are saying, Please try again ..","I don't really get you, please try again.","Sorry, what??..could you please be more specific"]))
            send_message(recipient_id,"if your doubts are not clear yet, you can always call for help..")
            send_message(recipient_id, "Not god O:-) ...to our Customer care")
            call_button(recipient_id)
            if recipient_id != '1669830646395897':
            	none_records(message, best.intent, best.score)# storing records for research purposes

    else :
            send_message(recipient_id,random.choice(["I don't understand what you are saying, Please try again ..","I don't really get you, please try again.","Sorry, what??..could you please be more specific"]))
            send_message(recipient_id,"if your doubts are not clear yet, you can always call for help..")
            send_message(recipient_id, "Not god O:-) ...to our Customer care ")
            call_button(recipient_id)
            if recipient_id != '1669830646395897':
            	none_records(message, best.intent, best.score) # storing records for research purposes
    
    


def visit_button(recipient_id):
    message_data = {"recipient": {"id":recipient_id},"message": {"attachment": {"type": "template","payload": {"template_type": "button","text": "For further details visit our website by clicking the button down below","buttons":[ {"type":"web_url","url":"https://www.rannlab.com","title":"Rannlab Technologies"}]}}}}
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    response_message = json.dumps(message_data)
    req = requests.post(post_message_url,headers={"Content-Type": "application/json"},data=response_message)

def call_button(recipient_id):
    message_data = {"recipient": {"id":recipient_id},"message": {"attachment": {"type": "template","payload": {"template_type": "button","text": "Need further assistance, then call by clicking the button down below","buttons":[ {"type":"phone_number","title":"Rannlab Tech","payload":"+919990613366"}]}}}}
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    response_message = json.dumps(message_data)
    req = requests.post(post_message_url,headers={"Content-Type": "application/json"},data=response_message)

# store none response to database
def none_records(message,intent,score):
	db = pymysql.connect("148.72.232.169", "chatbot", "j0b@9Zx1","rannlab_chatbot")
	cursor = db.cursor()
	
	# sql = """CREATE TABLE RESPONSE (message varchar(50),intent varchar(20), score int)"""
	# cursor.execute(sql)
	try :
		cursor.execute("""INSERT INTO RESPONSE VALUES('%s','%s',%.2f)""" % (message,intent,score))
		db.commit()

	except :
		db.rollback()
	
	db.close()



if __name__ == "__main__":
    app.run(debug = True , port = 5000) 
