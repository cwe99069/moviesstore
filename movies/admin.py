from django.contrib import admin
from django.db.models import Count, Sum
from .models import Movie, Review
from django.urls import path
from django.template.response import TemplateResponse

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls= [
            path(
                'movie-purchased-reviewed/',
                self.admin_site.admin_view(self.movie_purchased_reviewed_view),
                name='movie_purchased_reviewed',
            ),
        ]
        return custom_urls + urls
    
    def movie_purchased_reviewed_view(self, request):
        movies = Movie.objects.annotate(
            num_purchased = Sum("item__quantity"),
        ).order_by('-num_purchased')

        mostPurchased = movies.first()

        movies = Movie.objects.annotate(
            num_reviewed = Count("review")
        ).order_by('-num_reviewed')

        mostReviewed = movies.first()
        
        template_data = {
            **self.admin_site.each_context(request),
            'title': 'Movie with Most Purchases + Reviews',
            'mostPurchased': mostPurchased,
            'mostReviewed': mostReviewed,
        }
        return TemplateResponse(
            request,
            'admin/movie_purchased_reviewed.html',
            template_data
        )
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)