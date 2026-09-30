from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from movies.models import Review
from .models import Report
from django.contrib.auth.models import User

@login_required
def repreview(request, review_id):
    review_rep = get_object_or_404(Review, id=review_id)
    template_data = {}
    template_data['title'] = 'Report Review'
    if request.method == 'GET':
        return render(request, 'report/index.html', {'template.data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        report = Report()
        report.comment = request.POST['comment']
        report.review = review_rep
        report.user = request.user
        review_rep.reported = True
        review_rep.save()
        movie_id = review_rep.movie.id
        report.save()
        return redirect('movies.show', id=movie_id)
    else:
        return redirect('movies.show', id=movie_id)

