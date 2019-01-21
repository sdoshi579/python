#!/usr/bin/env python
# coding: utf-8

# In[2]:


import nltk
nltk.download()


# In[3]:


import nltk
from nltk.tokenize import RegexpTokenizer

text = 'Citizens of India are known as Indians.'

# By passing r'\w+' to the RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

tokens = tokenizer.tokenize(text)


# In[4]:


print(tokens)

# ['Citizens', 'of', 'India', 'are', 'known', 'as', 'Indians']

# In[5]:


from nltk.corpus import stopwords

sw = stopwords.words('english')
clean_tokens = [token for token in tokens if token not in sw]


# In[6]:


clean_tokens

# ['Citizens', 'India', 'known', 'Indians']

# In[7]:


from nltk.stem.porter import PorterStemmer

pstemmer = PorterStemmer()
[pstemmer.stem(token) for token in clean_tokens]

# ['citizen', 'india', 'known', 'indian']

# In[8]:


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
[lemmatizer.lemmatize(token) for token in clean_tokens]

#['Citizens', 'India', 'known', 'Indians']






