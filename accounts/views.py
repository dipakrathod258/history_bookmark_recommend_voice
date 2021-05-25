# Django packages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

# Machine Learning packages
import pandas as pd
import numpy as numpy
from sklearn.feature_extraction.text import CountVectorizer
#sklearn : Scikit learn (Science kit learn) used for fetching the ML model
#CountVectorizer: We want to convert text into matrix/vector
#CountVectorizer: Matrix/vector is the only format understood by ML model
# Options: word2vec, bert etc.(Deep learning) -> 1 Billion

from sklearn.metrics.pairwise import cosine_similarity

# Python packages
import json
import datetime
import os

# Third part packages
from gtts import gTTS
from googlesearch import search
from playsound import playsound


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ContactUsView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'contact_us.html'

class AboutUsView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'about_us.html'

class ThankYouView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'thank_you.html'

class ProductHistoryView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'product_history.html'

class ThankYouBookmarkView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'thank_you_bookmark.html'

def combine_features(row):
    try:
        return row["keywords"]+" "+row["cast"]+" "+row["genres"]+" "+row["director"]
    except:
        print("Error", row)



#Helper functions, use them if needed

def get_title_from_index(index, df):
    return df[df.index==index]["title"].values[0]

def get_index_from_title(movie_title, df):
    return df[df["title"]==movie_title]["index"]


def create_post(request):
    # print(request.POST['movie_name'])
    try:
        # HttpResponse()
        df = pd.read_csv('C:/Users/Akhil/Downloads/movie_dataset.csv')
        #pd = pandas datframe
        #df = DataFrame
        # Dataframe is used for converting the text csv into object
        #Select  features

        features = ["keywords", 'cast', "genres", "director"] # cold call
        # Feature selection im machine learning
        for feature in features:
            df[feature] = df[feature].fillna('')

        #Create a colummn in DataFrame & combine features

        df["combined_features"] = df.apply(combine_features, axis=1) # Truth values

        #Create count matrix using combined features

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df["combined_features"]) # Training of the model
        cosine_sim = cosine_similarity(count_matrix) # validation or predictions or testing
        cosine_sim.shape # rows and  columns in matrix

        movie_user_likes = request.POST['movie_name']

        #get index of the movie from its title
        movie_index = get_index_from_title(movie_user_likes, df)
        movie_index
        print("movie_index")
        print(movie_index)

        similar_movies = list(enumerate(cosine_sim[movie_index][0])) # Return the list of records 
        # which mathces with the data set titles after model prediction
        # for movie in similar_movies:
        #     print(movie[1])


        #Get list of movies in descending order of similarity
        sorted_similar_movies = sorted(similar_movies, key = lambda x: x[1], reverse =True) # Anonymous function to sort the records in descending order 
        sorted_similar_movies

        #Get list of first 50 similar movies
        i=0
        results = list()
        for movie in sorted_similar_movies:
            # print(get_title_from_index(movie[0], df))
            
            results.append(get_title_from_index(movie[0], df))
            i+=1
            if(i>15):
                break
        # to search
        results = set(results)
        for x in results:        
            language = 'en'
            myobj = gTTS(text=x, lang=language, slow=False)
            print("title")
            print(x)
            file_name = x+".mp3"
            print(file_name)
            myobj.save(file_name)
            # os.chmod(file_name, stat.S_IRUSR)
            os.system("mpg321 file_name")
            playsound(file_name)
            os.remove(file_name)

        return render(request, 'results.html', {'results': results})
    except Exception as e:
        errorObj = True
        results = False
        print("error")
        print(e)
        query = request.POST['movie_name']
        textSample = "Hey! Your Search has the recommendations as per below link."+query
        language = 'en'
        myobj = gTTS(text=textSample, lang=language, slow=False)
        myobj.save("recommendations.mp3")
        os.system("mpg321 recommendations.mp3")
        playsound("recommendations.mp3")
        os.remove('recommendations.mp3')


        net_results = []
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            net_results.append(j)
        print("net_results")
        print(net_results)
        return render(request, 'results.html', {'errorObj': net_results}) # We are passing these net results so that
        # we will have a track of all the global searches
    else:
        pass
    finally:
        pass


def textToSpeech(request):
    mytext = 'Welcome to geeksforgeeks!'
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("mpg321 welcome.mp3")

