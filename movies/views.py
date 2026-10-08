from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import Movie, Review, Star
from django.contrib.auth.decorators import login_required
from report.views import repreview
# Create your views here.

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})


def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    user_star = Star.objects.filter(movie=movie, user= request.user).first()
    avg_rating = Star.objects.filter(movie=movie).aggregate(Avg('value'))['value__avg']

    if avg_rating is not None:
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = 0

    template_data= {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['avg_rating'] = avg_rating
    template_data['reviews'] = reviews.filter(reported=False)
    template_data['user_star'] = user_star
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
        {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def report_review(request, review_id):
    repreview(request, review_id)

@login_required
def star_review(request, id):
    if request.method == 'POST':
        specific_movie = Movie.objects.get(id=id)
        specific_value = int(request.POST.get("rating[rating]"))
        print(specific_movie)
        print(specific_value)
        Star.objects.update_or_create(
            movie = specific_movie,
            user = request.user,
            defaults= {'value': specific_value} 
            )
    return redirect('movies.show', id=id)

    