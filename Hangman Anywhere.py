import unirest
from random import randint

from twilio.rest import TwilioRestClient
ACCOUNT_SID = "AC93ffb3dac85d04f10355a146aefdf2da" 
AUTH_TOKEN = "aa9d7c79e30dceca14efaf302d647195" 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
myNumber="+15067990350"

def clearMessages():
    try:
        for m in client.messages.list():
            client.messages.delete(m.sid)
    except:
        clearMessages()
dictionary=open('HangmanWords.txt','r')
wordList=[]
for line in dictionary:
    if len(line)>3:
        wordList.append(line)
while True:
    word=wordList[randint(0,len(wordList))].strip().upper()
    current=['_']*len(word)
    clearMessages()
    lives=6
    guessed=""
    incorrect=""
    started=False
    while True:
        messages = client.messages.list()
        if len(messages)!=0:
            text=messages[0].body.upper()
            print text
            incomingNum=messages[0].from_
            if started:
                if len(text)==1 and ord(text)>=65 and ord(text)<=90:
                    if text not in guessed:
                        if (text in word):
                            for c in range (0,len(word)):
                                if word[c]==text:
                                      current[c]=text
                            if '_' not in current:
                                msg=client.messages.create(
                                body="You win! The word was "+word+"\nText anything to start another game.",
                                to=incomingNum,
                                from_=myNumber)
                                break
                        else:
                            lives=lives-1
                            if (lives<0):
                                msg=client.messages.create(
                                body="You lose! The word was "+word+"\nText anything to start another game.",
                                to=incomingNum,
                                from_=myNumber)
                                break
                            incorrect+=text
                        guessed+=text
                        msg=client.messages.create(
                            body=' '.join(current)+"\nGuessed letters: "+incorrect+"\nLives: "+str(lives),
                            to=incomingNum,
                            from_=myNumber)
                    else:
                        msg=client.messages.create(
                            body="You have already guessed the letter "+text+"\n"+' '.join(current)+"\nGuessed letters: "+incorrect+"\nLives: "+str(lives),
                            to=incomingNum,
                            from_=myNumber)
                else:
                    msg=client.messages.create(
                        body="Please enter a single letter!",
                        to=incomingNum,
                        from_=myNumber)
            else:
                msg=client.messages.create(
                    body="New Game!\n"+' '.join(current)+"\nLives: "+str(lives),
                    to=incomingNum,
                    from_=myNumber)
                started=True
            clearMessages()
            
