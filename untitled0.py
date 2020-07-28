from newspaper import Article
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS 
import os 
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
import yaml
import pyaudio
import speech_recognition as sr

warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)
### website from where we want to extract the data
article1 = Article('https://en.wikipedia.org/wiki/Coronavirus')
article1.download()
article1.parse()
article1.nlp()

article2 = Article('https://www.euro.who.int/en/health-topics/noncommunicable-diseases/mental-health/data-and-resources/mental-health-and-covid-19')
article2.download()
article2.parse()
article2.nlp()

article3 = Article('https://www.healthline.com/health-news/what-covid-19-is-doing-to-our-mental-health')
article3.download()
article3.parse()
article3.nlp()

article4 = Article('https://www.webmd.com/lung/coronavirus')
article4.download()
article4.parse()
article4.nlp()

article5 = Article('https://www.healthline.com/health/coronavirus-covid-19')
article5.download()
article5.parse()
article5.nlp()

article6 = Article('https://timesofindia.indiatimes.com/coronavirus')
article6.download()
article6.parse()
article6.nlp()

article7 = Article('https://www.helpguide.org/articles/depression/dealing-with-depression-during-coronavirus.htm')
article7.download()
article7.parse()
article7.nlp()


corpus = article1.text + article2.text + article3.text + article4.text + article5.text + article6.text + article7.text
text = corpus
sentence_list = nltk.sent_tokenize(text)
def greeting_response(text):
  text = text.lower()

  #Bots respnse
  bot_greetings = ['hi','hey','hello','hey there']
  #Users Greeing
  user_greeting = ['hi','hello','greetings','wassup','hey','hey there']

  for word in text.split():
    if word in user_greeting:
      return random.choice(bot_greetings)

def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]]>x[list_index[j]]:
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp
  return list_index

def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response=''
  cm = CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1],cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)
  index =index[1:]
  response_flag = 1

  j=0
  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0.0:
      bot_response = bot_response +' '+ sentence_list[index[i]]
      response_flag = 1
      j = j+1
    if j > 2:
      break

  if response_flag==0:
    bot_response = bot_response+' '+"I apologise, I don't Understand."

  sentence_list.remove(user_input)

  return bot_response
# Chat
print("Doctor Bot")




while(True):
    exit_list = ['exit', 'see you later', 'bye', 'break', 'quit']

    r=sr.Recognizer()
    r.energy_threshold=4000
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        r.dynamic_energy_threshold = True 
        s=("Speak now")
        language = 'en'
        myobj = gTTS(text=s, lang=language, slow=False) 
        myobj.save("welcome.mp3") 
        playsound("welcome.mp3") 
        os.remove("welcome.mp3")
        print('Bot: '+s)

        audio=r.listen(source,timeout=40,phrase_time_limit=40)
        user_input=r.recognize_google(audio)
        print("YOU: "+ user_input)
    

    if user_input.lower() in exit_list:
        res = ('Bye, Chat with you later')
        language = 'en'
        myobj = gTTS(text=res, lang=language) 
        myobj.save("welcome.mp3") 
        playsound("welcome.mp3") 
        os.remove("welcome.mp3")
        print(res)
        break
    
    else:
        if greeting_response(user_input) != None:
            res = (greeting_response(user_input))
        else:
            res = (bot_response(user_input))
    language = 'en'
    myobj = gTTS(text=res, lang=language, slow=False) 
    myobj.save("welcome.mp3") 
    print('Bot:'+res)
    playsound("welcome.mp3") 
    os.remove("welcome.mp3")
   
 