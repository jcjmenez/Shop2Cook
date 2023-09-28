import numpy as np
from nltk.stem import SnowballStemmer
from sklearn.datasets import load_files
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import make_pipeline

import os

def classify(texts_path, algorithm):
    food_data = load_files(texts_path, encoding="latin-1")
    X, y = food_data.data, food_data.target
    documents = []

    stemmer = SnowballStemmer('spanish')

    for sen in range(0, len(X)):
        print(sen)
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(X[sen]))
        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)
        # Converting to Lowercase
        document = document.lower()
        # Stemming
        document = document.split()
        document = [stemmer.stem(i) for i in document]
        document = ' '.join(document)
        documents.append(document)
        
    stopwords = []
    with open('stopwords.txt', 'r') as file:
        stopwords=[file.read().replace('\n', ',')]

    tfidfconverter = TfidfVectorizer(min_df=5, max_df=0.7, stop_words=stopwords)
    X = tfidfconverter.fit_transform(documents).toarray()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    model_name = ""
    if (algorithm == "Random Forest"):
        classifier = RandomForestClassifier(random_state=0)
        model_name = "Random Forest"
    elif (algorithm == "Decision Tree"):
        classifier = DecisionTreeClassifier()
        model_name = "Decision Tree"
    elif (algorithm == "Bayes"):
        classifier = MultinomialNB()
        model_name = "Bayes"
    elif (algorithm == "Support Vector Machine"):
        classifier = SVC()
        model_name = "Support Vector Machine"
    elif (algorithm == "K-Nearest-Neighbor"):
        classifier = KNeighborsClassifier(n_neighbors=4)
        model_name = "K-Nearest-Neighbor"
    else:
        classifier = DecisionTreeClassifier()
        model_name = "Decision Tree"
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    matrix = confusion_matrix(y_test,y_pred)
    print(classification_report(y_test,y_pred))
    print(accuracy_score(y_test, y_pred))
    return_object = {"Matrix": matrix}
    # return_object[model_name] = classifier
    # pipeline = make_pipeline(tfidfconverter, classifier)
    model_pipe = {"Tfidf": tfidfconverter, "Classifier": classifier}
    return_object[model_name] = model_pipe

    return return_object
        

def classify_with_model(texts_path, tfidfconverter, classifier):
    food_data = load_files(texts_path, encoding="latin-1")
    X = food_data.data
    documents = []
    stemmer = SnowballStemmer('spanish')
    
    for sen in range(0, len(X)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(X[sen]))
        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)
        # Converting to Lowercase
        document = document.lower()
        # Stemming
        document = document.split()
        document = [stemmer.stem(i) for i in document]
        document = ' '.join(document)
        documents.append(document)
        
    X = tfidfconverter.transform(documents).toarray()
    y_pred = classifier.predict(X)
    # 0 -> carnes, pescados y verduras
    # 1 -> cereales y derivados
    # 2 -> leche, huevo y derivados
    # 3 -> legumbres
    print(y_pred)
    return y_pred

def get_food_from_text(text):
    X = ""
    with open(text, "r", encoding="latin1") as f:
        X = f.read()

    document = re.sub(r'\W', ' ', str(X))
    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    # Converting to Lowercase
    document = document.lower()
    document = document.split()
        
    food_words = []
    with open('palabras-comida.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            food_words.append(line.replace("\n", ""))
    
    stopwords = []
    with open('stopwords.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            stopwords.append(line.replace("\n", ""))
    
    shopping_list = []
    for d in document:
        if d not in shopping_list and d in food_words and d not in stopwords:
            shopping_list.append(d)
    
    return shopping_list