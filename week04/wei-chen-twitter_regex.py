
# coding: utf-8

# ## Problem 4.3. Twitter: Regular Expressions.
# 
# In this problem, you will use regular expressions to process real Twitter data.
# 
# (If you are curious where this data came from, 1,000 tweets were fetched using the search query `#informatics` on Tuesday, February 3rd, 2015, around 10pm. See [Mining the Social Web 2nd Edition](https://github.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition) by Matthew A. Russell. [twitter_to_ascii.py](https://github.com/INFO490/spring2015/tree/master/week04/twitter_to_ascii.py) on the course Github repository is a Python 2 script that collects 1,000 tweets and generates an ASCII text file of status texts.)
# 
# If you used `git clone`/`git pull` from `/data`, the path to the data file will be `/data/spring2015/week04/informatics.txt`. It's an ASCII text file, and when you first get a new data like this, it's a good idea to see how the data looks like. You have learned various ways to do this: you could write a short Python script that reads the file line by line and print them out; you could mount the data container onto a Docker container in terminal mode and use `head`; but here I'll show you how to use shell commands in IPython notebook. Open up a new IPython notebook and run
# 
# ```console
# %%bash
# head /data/spring2015/week04/informatics.txt
# ```
# 
# Then the output will be
# ```console
# RT @KirkDBorne: Feature Selection based on #MachineLearning in MRIs: http://t.co/fwdZRLaSMd Medical imaging #informatics #DataScience
# RT @vikpant: #SocialMedia #BigData #Mining May Improve Population #Health - HIA. http://t.co/YlVwRJb9rH #analytics #informatics #datascienc
# RT @vikpant: #SocialMedia #BigData #Mining May Improve Population #Health - HIA. http://t.co/YlVwRJb9rH #analytics #informatics #datascienc
# RT @vikpant: #SocialMedia #BigData #Mining May Improve Population #Health - HIA. http://t.co/YlVwRJb9rH #analytics #informatics #datascienc
# RT @vikpant: #SocialMedia #BigData #Mining May Improve Population #Health - HIA. http://t.co/YlVwRJb9rH #analytics #informatics #datascienc
# RT @vikpant: #SocialMedia #BigData #Mining May Improve Population #Health - HIA. http://t.co/YlVwRJb9rH #analytics #informatics #datascienc
# RT @KirkDBorne: Feature Selection based on #MachineLearning in MRIs: http://t.co/fwdZRLaSMd Medical imaging #informatics #DataScience
# RT @vikpant: #SocialMedia #BigData #Mining May Improve Population #Health - HIA. http://t.co/YlVwRJb9rH #analytics #informatics #datascienc
# RT @KirkDBorne: Feature Selection based on #MachineLearning in MRIs: http://t.co/fwdZRLaSMd Medical imaging #informatics #DataScience
# RT @KirkDBorne: Feature Selection based on #MachineLearning in MRIs: http://t.co/fwdZRLaSMd Medical imaging #informatics #DataScience
# ```
# 
# Your first is to clean up these texts since many of them contain non-alphabetical characters as well as special characters such as hashtags and @ signs, and HTTP links. Thus,
# 
# - Use `re` regular expressions to write a function named `clean_statuses()` that takes a list of strings (tweets with special characters), and returns a list of strings (only clean words).
# 
# To do this, you should
# 
# - Split the text into words (words in a text are separated by whitespaces),
# 
# and remove all words that contain the following:
# 
# - hashtags (#),
# - users (@),
# - links (begins with http), and
# - any non-alphabetical characters (since a tweet may contain a foreign character).
# 
# The easiest way to do this (that I can think of) is substituting any word that matches the above patterns with empty strings `''` (using regular expressions, or regex), and at the end, using list comprehension to remove all the empty strings from the list.
# 
# At this point, you should
# 
# - Convert everything to lower cases.
# 
# and finally,
# 
# - Return the list of cleaned-up words.
# 
# For example, the output of
# 
# ```python
# with open('/data/spring2015/week04/informatics.txt', 'r') as f:
#     statuses = f.read().splitlines()
#     
# clean_tweets = clean_statuses(statuses[:10])
# ```
# 
# (the result of cleaning up the first 10 lines printed out by `head` above) should be
# 
# ```console
# ['rt', 'feature', 'selection', 'based', 'on', 'in', 'mris', 'medical', 'imaging', 'rt', 'may', 'improve', 'population', 'hia', 'rt', 'may', 'improve', 'population', 'hia', 'rt', 'may', 'improve', 'population', 'hia', 'rt', 'may', 'improve', 'population', 'hia', 'rt', 'may', 'improve', 'population', 'hia', 'rt', 'feature', 'selection', 'based', 'on', 'in', 'mris', 'medical', 'imaging', 'rt', 'may', 'improve', 'population', 'hia', 'rt', 'feature', 'selection', 'based', 'on', 'in', 'mris', 'medical', 'imaging', 'rt', 'feature', 'selection', 'based', 'on', 'in', 'mris', 'medical', 'imaging']
# ```
# 
# Note that words that had #'s, @'s, numbers, or links in them are all gone now, and we have a list of nicely looking words. If you are confused about how to do some of the operations, you can simply google e.g. "python convert string to lowercase" or ask us questions.
# 
# I'll even give you a hint: you can replace every word that contains a # with an empty string with 
# 
# ```python
# clean_tweets = [re.sub('\#.*', '', tweet) for tweet in tweets]
# ```
# 
# where I iterated through `tweets` using list comprehensions. We have to use `\` before the `#` because `#` is a special character. The `.` matches any character (except newline), and `*` means zero or more repetitions. Thus, this line substitues every word in `tweets` that starts with a `#` with an empty string `''`.

# In[2]:

import re

with open('/data/spring2015/week04/informatics.txt', 'r') as f:
    statuses = f.read().splitlines()


# In[3]:

def clean_statuses(statuses):
    '''
    Takes a list of strings (twitter status texts containing special characters)
    and returns a list with all lowercase words
    (no words with #, @, http, or non-alphabetical characters)
    
    Parameters
    __________
    statuses: A list of str.
    
    Returns
    _______
    clean_tweets: A list of str.
    '''

    # your code goes here
    list_of_word_lists = [each_status.split() for each_status in statuses] # split each status into a word list, so statuses becomes a list of word lists
    word_list = []
    for item in list_of_word_lists:
        word_list += item # merge all word_lists together
    
    clean_tweets = [re.sub('(\@.*)|(\#.*)|(http.*)|[^a-zA-Z0-9!"#$%&\'()*+,-\./:;<=>?@[\\]^_`{|}~]', '', item) for item in word_list] # delete words with #, @, http, non-alphabetic characters
    clean_tweets = ["".join(ch for ch in item if (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')) for item in clean_tweets] # remove punctuations
    clean_tweets = [item.lower() for item in clean_tweets if item != ''] # turn each word into lowercase and delete empty string
    # my code ends here

    return clean_tweets


# Now, returned from the `clean_statuses()` function is a list of nicely cleaned-up lowercase words. Next,
# 
# - Write a function named `count_words()` that calculates the frequency of each word and returns a list of tuple of the form (string, int).
# 
# For example, if when you run
# 
# ```python
# count_words(statuse[:10])
# ```
# 
# the output should be
# 
# ```console
# [('rt', 10),
#  ('based', 4),
#  ('selection', 4),
#  ('population', 6),
#  ('mris', 4),
#  ('imaging', 4),
#  ('improve', 6),
#  ('in', 4),
#  ('feature', 4),
#  ('on', 4),
#  ('medical', 4),
#  ('may', 6),
#  ('hia', 6)]
# ```

# In[5]:

def count_words(input_list):
    '''
    Takes a list of strings (sentences containing special characters) and returns a list of tuples (word, frequency).
    
    Parameters
    __________
    inputs_list: A list of strings.
    
    Returns
    _______
    counts: A tuple of (word, frequency)
    '''
    
    # your code goes here
    input_list = clean_statuses(input_list) # clean up the list
    temp_count = {}
    for item in input_list:
        if not (item in temp_count):
            temp_count[item] = 0 # if this entry does not exist, create it!
        temp_count[item] += 1
    
    counts = []
    for item in temp_count: # this loop turns the dictionary into a tuple as the output
        counts += [(item, temp_count[item])]
            
    # my code ends here
    return counts


# In[94]:




# In[ ]:



