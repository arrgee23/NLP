#!/usr/bin/env python
# coding: utf-8

import nltk
#nltk.download('brown')
nltk.download('webtext')
nltk.download('reuters')
from nltk.util import pad_sequence
from nltk.util import bigrams
from nltk.util import ngrams
from nltk.lm.preprocessing import pad_both_ends
from nltk.corpus import webtext
#from nltk.corpus import brown
from nltk.corpus import reuters
from nltk.lm.preprocessing import padded_everygram_pipeline


from nltk.lm import MLE

"""
for fileid in reuters.fileids():
    print((fileid), reuters.raw(fileid)[:65])
"""

def makeModel():
    #sentences = webtext.raw()+brown.raw()+reuters.raw()
    sentences = webtext.raw()+reuters.raw()
    # Tokenize the sentences
    try: # Use the default NLTK tokenizer.
        from nltk import word_tokenize, sent_tokenize 
        # Testing whether it works. 
        # Sometimes it doesn't work on some machines because of setup issues.
        word_tokenize(sent_tokenize("This is a foobar sentence. Yes it is.")[0])
    
    except: # Use a naive sentence tokenizer and toktok.
        import re
        from nltk.tokenize import ToktokTokenizer
        # See https://stackoverflow.com/a/25736515/610569
        sent_tokenize = lambda x: re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', x)
        # Use the toktok tokenizer that requires no dependencies.
        toktok = ToktokTokenizer()
        word_tokenize = word_tokenize = toktok.tokenize


    tokenized_text = [list(map(str.lower, word_tokenize(sent))) 
                    for sent in sent_tokenize(sentences)]

    # Make it ready for making 3 grams
    n = 5
    train_data, padded_sents = padded_everygram_pipeline(n, tokenized_text)

    model = MLE(n) # Lets train a 3-grams model, previously we set n=3

    model.fit(train_data, padded_sents)
    #print(model.vocab)
    
    return model

# dont return offensive and undesired words
def isGoodKey(key):
    if(key[0] in [',','.',"'",'"','*','/','['] or key in ['dick','boob','vagina','pussy','penis','blow','ass','balls']):
        return False
    return True

def returnTop5(model,sentence):
    sentence = sentence.lower()
    wordlist = sentence.split(' ')
    #print(wordlist)
    
    top5 = []
    count = 0
    itr = 0;
    while(itr<len(wordlist) and count < 5):
        l = wordlist[itr:] # each time extract last few words
        dictionary = model.counts[l].copy()
        
        #print(l,dict(dictionary))
        
        #keys = dictionary.keys()
        #if(len(keys)>0):
        while(count<5 and len(dictionary)>0):
            maximum = -1
            maxkey = ""
            
            # find the key with max freq
            for key in dictionary:
                if(dictionary[key]>maximum):
                    maximum = dictionary[key]
                    maxkey = key

            # weve found the max
            if(maximum!=-1):
                maximum = -1
                dictionary.pop(maxkey) # remove max
                
                
                #print("maxkey  ",maxkey)
                
                if(isGoodKey(maxkey) and maxkey not in top5):
                    count = count+1
                    top5.append(maxkey)
                
                
        
        itr+=1
        #print(l)
        
    return top5

# *, ', .,?,


# In[51]:




