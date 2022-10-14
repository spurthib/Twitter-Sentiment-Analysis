#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[1]:


from googletrans import Translator
import tweepy
import re
import os             
import nltk
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
nltk.download('punkt')
import preprocessor as p
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer 


# In[2]:


#input tweeter credentials#
CONSUMER_KEY = '3bAsLVoFl8HmlJBwJAB3hATYO'
CONSUMER_SECRET = 'mOyV7MHc22fhxGJdUrvVjqHY4cUcsApPBHu0tyiAzenWxCM1wB'
OAUTH_TOKEN = '1310696980859899909-1E9G87iXHIUOyPQcHJqxF4nsHptPac'
OAUTH_TOKEN_SECRET = 'YPXkDZz2K0dny0NfdS0clfJ4uCCKQVZn0hGaTIR9HV5tN'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


# In[3]:


def removeNLTKStop(text):
    stop_words = set(stopwords.words('english')) 
    filtered_sentences = []
    w = []
    result_string=""
    
    text = re.sub(r'\.COM|[^a-zA-Z ]+|\s(?=&)|(?<!\w\w)\s+(?!\w\w)', '', text, 0, re.IGNORECASE)
    
    word_tokens = word_tokenize(text.lower()) 
    #print(word_tokens)
    
    #Removed NLTK Stopwords 
    filtered_article = [w for w in word_tokens if not w in stop_words] 
    filtered_article = [] 
    
    ps = PorterStemmer() 
    stemmer = nltk.SnowballStemmer('english')
    lemmatizer = WordNetLemmatizer() 
    #for s in word_tokens:
     #   s = re.sub(r'\.COM|[^a-zA-Z ]+|\s(?=&)|(?<!\w\w)\s+(?!\w\w)', '', s, 0, re.IGNORECASE)
     #   result_string = result_string+s
        
    #print(result_string)
    for w in word_tokens: 
        #w = ps.stem(w)
        #w = stemmer.stem(w)
        
     #   result_string = result_string+s
        w = lemmatizer.lemmatize(w,pos="v") 
        if w not in stop_words: 
            filtered_article.append(w)
    return " ".join(filtered_article)


# In[ ]:





# In[4]:


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return str(tweet)


# In[30]:


def translateTweet(tweet):
    #translate
    translator = Translator()
    tweet = translator.translate(tweet) 
    print(tweet)
    return str(tweet)


# In[31]:


def processTweet2(tweet):
    
  
    #Remove RT
    tweet = re.sub('RT','',tweet)
    #print(tweet)
    #Convert to lower case
    tweet = tweet.lower()
    tweet = tweet.replace('-',' ', 1) 
    #tweet=re.sub(r'-(?:(?<!\b[0-9]{4}-)|(?![0-9]{2}(?:[0-9]{2})?\b))', ' ', tweet)

    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Convert @username to ''
    tweet = re.sub('@[^\s]+','',tweet)
    
    tweet = re.sub('u.s.','us',tweet)
    tweet = re.sub('united states','us',tweet)


    tweet = re.sub('u.k.','uk',tweet)
    tweet = re.sub('united kingdom','uk',tweet)


    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #print("here",tweet)
    #remove NLTK
    tweet = removeNLTKStop(tweet)
    
    
    #tweet = tweet.strip('\'"')
    tweet = re.sub('[^a-zA-Z0-9]', ' ', tweet)
    tweet.lstrip()


    #trim consecutive spaces
    tweet = re.sub(' +', ' ', tweet) 
    
    
    
    tweet = replaceTwoOrMore(tweet)

    
    # remove emoticons
    tweet = p.clean(tweet)
    return str(tweet)  


# In[32]:


#strings =['W','A','R' N I N G']
#for s in strings:
#    s = re.sub(r'\.COM|[^a-zA-Z ]+|\s(?=&)|(?<!\w\w)\s+(?!\w\w)', '', s, 0, re.IGNORECASE)
#    print(s)


# In[33]:


def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end


# In[34]:


i=0
all_files = os.listdir(os.path.expanduser("~/Desktop/Courses in MS/Machine Learning/Project/COVID-19-TweetIDs-master/2020-03"))
#print(len(all_files))
for a in all_files: 
    print("starting",a)
    f_name = 'COVID-19-TweetIDs-master/2020-03/'+a
    with open(f_name) as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            #print(line)
            try:
                api = tweepy.API(auth)
                tweet = api.get_status(line,tweet_mode="extended")
                if 'retweeted_status' in dir(tweet):
                    text=tweet.retweeted_status.full_text
                    #print("This is retweeted")
                else:
                    text=tweet.full_text
                    #print("This is original tweet")
                #print(tweet.user.location)
                #Change language
                if(tweet.lang!="en"):
                    print(text)
                    text=translateTweet(text)
            
                #print(text)
                tweet=processTweet2(text)
                filename = 'Tweet_Data/'+str(i)+'.txt'
    
                f = open(filename, "w")

                f.write(tweet.lstrip())
                f.write("\n")
                i=i+1
                f.close()
                #print(tweet)
            except tweepy.TweepError:
                #print("Cannot fetch tweets")
                pass
        print("Done")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


from twython import Twython, TwythonError
from googletrans import Translator
CONSUMER_KEY = '3bAsLVoFl8HmlJBwJAB3hATYO'
CONSUMER_SECRET = 'mOyV7MHc22fhxGJdUrvVjqHY4cUcsApPBHu0tyiAzenWxCM1wB'
OAUTH_TOKEN = '1310696980859899909-1E9G87iXHIUOyPQcHJqxF4nsHptPac'
OAUTH_TOKEN_SECRET = 'YPXkDZz2K0dny0NfdS0clfJ4uCCKQVZn0hGaTIR9HV5tN'
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

with open("C:\\Users\\Trisha\\Desktop\\1.txt") as fp:
    line = fp.readline()
    cnt = 1
    while line:
        ids = fp.readline()
        print(type(ids))
        cnt += 1
        tweet = twitter.show_status(id=ids)
        print(tweet['text'])


        tweet = tweet['text']
        translator = Translator()
        tw_inggris = translator.translate(tweet)
        print(tw_inggris.text)
    print("Done")





# In[ ]:



import tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)

tweet = api.get_status('1219755875407224832')
print(tweet.text)


# In[ ]:


' traveler from china diagnosed in seattle with wuhan coronavirus cdc spokesman'.lstrip()


# In[ ]:


all_files = os.listdir("C:\\Users\\Trisha\\Downloads\\COVID-19-TweetIDs-master\\COVID-19-TweetIDs-master\\2020-01")


# In[ ]:


# import these modules 
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
   
ps = PorterStemmer()   
# choose some words to be stemmed 
words = ["United States", "us", "programer", "programing", "programers","play"] 
  
for w in words: 
    print(w, " : ", ps.stem(w)) 


# In[ ]:


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize("unites states"))
print(lemmatizer.lemmatize("u.s."))
print(lemmatizer.lemmatize("geese"))
print(lemmatizer.lemmatize("rocks"))
print(lemmatizer.lemmatize("python"))
print(lemmatizer.lemmatize("better", pos="a"))
print(lemmatizer.lemmatize("best", pos="a"))
print(lemmatizer.lemmatize("run"))
print(lemmatizer.lemmatize("run",'v'))


# In[ ]:




