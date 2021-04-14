import re
import sys
import os
import string
#Creates a list containing the known abbreviations found int abbreviations.txt
def makeAbrev():
    abbrev_path = os.path.join(os.getcwd(), "abbreviations.txt") # ABSOLUTE PATH for abbreviations.txt
    abbrevFile = open(abbrev_path)
    abbrevList = []
    for line in abbrevFile:
        for word in line.split():
            abbrevList.append(word)
    return abbrevList

#handles the presense of an apostrophe as a contraction and the posessive
def handleApostrophe(str):
    tokens = []
    if str[-3:] == "n\'t":
        tokens.append(str[:-3])
        tokens.append("not")
    elif str[-3:] == "\'re":
        tokens.append(str[:-3])
        tokens.append("are")
    elif str[-3:] == "\'ll":
        tokens.append(str[:-3])
        tokens.append("will")
    elif str[-2:] == "\'m":
        tokens.append(str[:-2])
        tokens.append("am")
    elif str[-2:] == "\'d": #since it is not possible to differentiate a contraction of 'd between had and would she'd -> she had vs she would, leave as is
        # tokens.append(str[:-2])
        # tokes.append("had/would")
        tokens.append(str)
    elif str[-2:] == "\'s": # assume posessive
        tokens.append(str[:-2])
        tokens.append("\'s")
    return tokens
    

#Tokenize by seperating punctuation from words whenever not integral to word
def tokenizeText(str):
    tokens = []
    broken = str.split()
    abbreviations = makeAbrev()
    for tok in broken:
        temp = []
        if len(tok) <= 1: #if word is of length 1 char we know we can just add it as a token
            tokens.append(tok)
            continue
        while len(tok) > 0 and tok[0] in string.punctuation: # if word starts with punctuation treat punct as seperate token
            tokens.append(tok[0])
            tok = tok[1:]
        while len(tok) > 0 and tok[-1] in string.punctuation and tok[-1] not in ['.', '\'']: #if it ends in non excption punctuation remove punct and add to tokens later 
            temp.insert(0,tok[-1])
            tok = tok[:-1]

        if bool(re.search(r'\d', tok)): # if tok contains a number dont futher tokenize
                tokens.append(tok)
        elif '.' in tok:
            if (tok.count('.') > 1) or (tok.lower() in abbreviations): #word is an abbreviation or acronym
                tokens.append(tok)
            elif tok[-1] == '.':
                tokens.append(tok[:-1])
                tokens.append(tok[-1])
            else:
                tokens.append(tok)
        elif '\'' in tok:
            tokens.extend(handleApostrophe(tok))
        else:
            tokens.append(tok)
        if len(temp) > 0:
            tokens.extend(temp)
    return tokens

def removeStopwords(tokens):
    stopfile_path = os.path.join(os.getcwd(), "stopwords.txt")
    stopList = []
    file = open(stopfile_path)
    removedList = []
    for line in file:
        for word in line.split():
            stopList.append(word)
    for token in tokens:
        t = token.lower()
        if t not in stopList:
            removedList.append(token)
    return removedList


def pprocess(fileString):
    tokens = tokenizeText(fileString)
    removed = removeStopwords(tokens)
    return removed