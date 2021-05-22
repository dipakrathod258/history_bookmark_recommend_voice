from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import numpy as numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import datetime
from gtts import gTTS
import os
from googlesearch import search


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
        df = pd.read_csv('/home/rahul/Desktop/movie_dataset.csv')
        #Select  features

        features = ["keywords", 'cast', "genres", "director"]

        for feature in features:
            df[feature] = df[feature].fillna('')

        #Create a colummn in DataFrame & combine features

        df["combined_features"] = df.apply(combine_features, axis=1)

        #Create count matrix using combined features

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df["combined_features"])
        cosine_sim = cosine_similarity(count_matrix)
        cosine_sim.shape

        movie_user_likes = request.POST['movie_name']

        #get index of the movie from its title
        movie_index = get_index_from_title(movie_user_likes, df)
        movie_index
        print("movie_index")
        print(movie_index)

        similar_movies = list(enumerate(cosine_sim[movie_index][0]))
        # for movie in similar_movies:
        #     print(movie[1])


        #Get list of movies in descending order of similarity
        sorted_similar_movies = sorted(similar_movies, key = lambda x: x[1], reverse =True)
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

        return render(request, 'results.html', {'results': results})
    except Exception as e:
        errorObj = True
        results = False

        query = request.POST['movie_name']
        net_results = []
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            net_results.append(j)
        print("net_results")
        print(net_results)
        return render(request, 'results.html', {'errorObj': net_results})
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
