from platform import release
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pickle
import pandas as pd
import requests
from json import dumps
import random
from .forms import CreateUserForm

# Create your views here.


def Home(request):
    movies_data = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies_dict = pd.DataFrame(movies_data)
    movies = movies_dict['title'].values
    movies_names = (movies_dict['title'].values).tolist()
    api_key = '8bae8488d086270ee807102314329032'

    if request.method == 'GET':
        if request.GET.get("movie"):
            query = request.GET.get("movie").lower()

            if query in movies:

                def fetch_data(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

                def fetch_overview(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return data['overview']

                def fetch_release_date(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return data['release_date']

                def fetch_rating(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return data['vote_average']

                def fetch_genre(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    genres = []
                    for i in data['genres']:
                        genres.append(i['name'])

                    return ", ".join(genres)

                def fetch_backdrop(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return "https://image.tmdb.org/t/p/original/" + data['backdrop_path']

                def recommend_movie(query):
                    movie_index = movies_dict[movies_dict['title']
                                              == query].index[0]
                    search_movie_id = movies_dict[movies_dict['title']
                                                  == query].iloc[0].movie_id
                    search_movie_poster = fetch_data(search_movie_id)
                    overview = fetch_overview(search_movie_id)
                    genres = fetch_genre(search_movie_id)
                    release_date = fetch_release_date(search_movie_id)
                    rating = fetch_rating(search_movie_id)

                    distances = similarity[movie_index]
                    movies_list = sorted(
                        list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

                    results = []
                    posters = []

                    for i in movies_list:
                        movie_id = movies_dict.iloc[i[0]].movie_id
                        results.append(movies_dict.iloc[i[0]].title)
                        posters.append(fetch_data(movie_id))
                    combined_data = []
                    for result, poster in zip(results, posters):
                        combined_data.append([result, poster])

                    return results, posters, combined_data, search_movie_poster, overview, genres, release_date, rating

                    # return render(request, 'home.html', context={'movies':movies, 'query':query, 'results': results})

                results, posters, combined_data, search_movie_poster, overview, genres, release_date, rating = recommend_movie(
                    query)

                movies_names = dumps(movies_names)
                context = {'movies': movies, 'query': query, 'results': results, 'posters': posters,
                           'combined': combined_data, 'main_poster': search_movie_poster, 'overview': overview, 'genres': genres,
                           "release_date": release_date, 'rating': rating, 'movies_names': movies_names}
                return render(request, 'movie.html', context)

            else:
                return render(request, 'error.html')
        else:

            def fetch_data():
                response = requests.get(
                    'https://api.themoviedb.org/3/movie/popular?api_key=8bae8488d086270ee807102314329032&language=en-US&page=1')
                data = response.json()
                posters = []
                backdrop = []
                title = []
                overview = []
                rating = []
                release_date = []
                count = 0
                
                for movie in data['results']:
                    if movie['backdrop_path']:
                        backdrop.append(
                            "https://image.tmdb.org/t/p/original/" + movie['backdrop_path'])
                    title.append(movie['title'])
                    overview.append(movie['overview'])
                    rating.append(movie['vote_average'])
                    release_date.append(movie['release_date'])
                    posters.append(
                        'https://image.tmdb.org/t/p/w500/' + movie['poster_path'])

                return posters, backdrop, title, overview, rating, release_date

            # def fetch_trending():
            #     response = requests.get("https://api.themoviedb.org/3/trending/movie/week?api_key=8bae8488d086270ee807102314329032")

                # return 'https://image.tmdb.org/t/p/w500/' + movie['poster_path']

            posters, backdrop, title, overview, rating, release_date = fetch_data()
            carousel_movies = zip(
                backdrop, title, overview, rating, release_date)
            movies_names = dumps(movies_names)
            return render(request, 'home.html', context={'movies': movies, 'query': '', 'posters': posters, 'movies_names': movies_names, 'carousel_movies': carousel_movies})


def Movie(request):
    movies_data = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies_dict = pd.DataFrame(movies_data)
    movies = movies_dict['title'].values
    movies_names = (movies_dict['title'].values).tolist()
    api_key = '8bae8488d086270ee807102314329032'

    if request.method == 'GET':
        if request.GET.get("movie"):
            query = request.GET.get("movie").lower()
            print(query)
            if query in movies:

                def fetch_data(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

                def fetch_overview(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return data['overview']

                def fetch_release_date(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return data['release_date']

                def fetch_rating(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return data['vote_average']

                def fetch_genre(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    genres = []
                    for i in data['genres']:
                        genres.append(i['name'])

                    return ", ".join(genres)

                def fetch_backdrop(movie_id):
                    response = requests.get(
                        'https://api.themoviedb.org/3/movie/{}?api_key=8bae8488d086270ee807102314329032&language=en-US'.format(movie_id))
                    data = response.json()
                    return "https://image.tmdb.org/t/p/original/" + data['backdrop_path']

                def fetch_trailer(movie_id):
                    response = requests.get("https://api.themoviedb.org/3/movie/{}/videos?api_key=8bae8488d086270ee807102314329032&language=en-US".format(movie_id))
                    data = response.json()
                    
                    return data['results'][0]['key']

                def fetch_watch_providers(movie_id):
                    response = requests.get("https://api.themoviedb.org/3/movie/{}/watch/providers?api_key=8bae8488d086270ee807102314329032".format(movie_id))
                    data = response.json()
                    watch_providers = []
                    logo = [] 
                    try:
                        if data['results']['IN']['flatrate']:
                            for platform in data['results']['IN']['flatrate']:
                                watch_providers.append(platform['provider_name'])
                                logo.append("https://image.tmdb.org/t/p/w154/" + platform['logo_path'])
                    except:
                        watch_providers.append('')
                        logo.append('https://image.tmdb.org/t/p/w154//7Fl8ylPDclt3ZYgNbW2t7rbZE9I.jpg')

                    return zip(watch_providers, logo)


                def recommend_movie(query):
                    movie_index = movies_dict[movies_dict['title']
                                              == query].index[0]
                    search_movie_id = movies_dict[movies_dict['title']
                                                  == query].iloc[0].movie_id
                    search_movie_poster = fetch_data(search_movie_id)
                    overview = fetch_overview(search_movie_id)
                    genres = fetch_genre(search_movie_id)
                    release_date = fetch_release_date(search_movie_id)
                    rating = fetch_rating(search_movie_id)
                    backdrop = fetch_backdrop(search_movie_id)
                    trailer_key = fetch_trailer(search_movie_id)
                    watch_providers = fetch_watch_providers(search_movie_id)

                    distances = similarity[movie_index]
                    movies_list = sorted(
                        list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

                    results = []
                    posters = []

                    for i in movies_list:
                        movie_id = movies_dict.iloc[i[0]].movie_id
                        results.append(movies_dict.iloc[i[0]].title)
                        posters.append(fetch_data(movie_id))

                    combined_data = []
                    for result, poster in zip(results, posters):
                        combined_data.append([result, poster])

                    return results, posters, combined_data, search_movie_poster, overview, genres, release_date, rating, backdrop, trailer_key, watch_providers

                    # return render(request, 'home.html', context={'movies':movies, 'query':query, 'results': results})

                results, posters, combined_data, search_movie_poster, overview, genres, release_date, rating, backdrop, trailer_key, watch_providers = recommend_movie(query)

                movies_names = dumps(movies_names)
                context = {'movies': movies, 'query': query, 'results': results, 'posters': posters,
                           'combined': combined_data, 'main_poster': search_movie_poster, 'overview': overview, 'genres': genres,
                           "release_date": release_date, 'rating': rating, 'movies_names': movies_names, 'backdrop': backdrop, 'trailer_key': trailer_key, 'watch_providers': watch_providers}
                return render(request, 'movie.html', context)

            else:
                return render(request, 'error.html')
    return render(request, 'movie.html')


def About(request):
    return render(request, 'about.html')


def Error(request):
    return render(request, 'error.html')


def Shows(request):
    movies_data = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies_dict = pd.DataFrame(movies_data)
    movies = movies_dict['title'].values
    movies_names = (movies_dict['title'].values).tolist()

    def fetch_shows():
        response = requests.get(
            "https://api.themoviedb.org/3/tv/popular?api_key=8bae8488d086270ee807102314329032&language=en-US&page=1")
        data = response.json()
        posters = []
        name = []
        overview = []
        rating = []
        first_air_date = []
        backdrop = []

        for show in data['results']:
            if show['backdrop_path'] != None:
                backdrop.append(
                    "https://image.tmdb.org/t/p/original/" + show['backdrop_path'])
            else:
                break
            name.append(show['name'])
            overview.append(show['overview'])
            rating.append(show['vote_average'])
            first_air_date.append(show['first_air_date'])
            posters.append(
                'https://image.tmdb.org/t/p/w500/' + show['poster_path'])

        return posters, backdrop, name, overview, rating, first_air_date

    posters, backdrop, name, overview, rating, first_air_date = fetch_shows()
    carousel_movies = zip(
        backdrop, name, overview, rating, first_air_date)
    movies_names = dumps(movies_names)

    context = {'posters': posters, 'backdrop' : backdrop, 'name': name, 'overview': overview, 'rating': rating, 'first_air_date': first_air_date, 'carousel_movies': carousel_movies, 'movies_names': movies_names }
    return render(request, 'shows.html', context)

