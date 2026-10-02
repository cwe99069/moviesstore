from django.contrib import admin
from django.db.models import Count, Sum
from .models import Order, Item, User
from django.urls import path
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404


# Register your models here.
admin.site.register(Item)

admin.site.index_template = "admin/custom_index.html"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls= [
            path(
                'userstats/',
                self.admin_site.admin_view(self.userstats_view),
                name='cart_order_user_most_purchases',
            ),
        ]
        return custom_urls + urls

    def userstats_view(self, request):
        us = User.objects.annotate(num_movies = Sum("order__item__quantity")).order_by('-num_movies')
        user = us.first()
        orders = Order.objects.filter(user=user)
        if user:
            total_movies = user.num_movies
        else:
            total_movies = 0
        template_data = {
            **self.admin_site.each_context(request),
            'title': 'User With Most Purchases',
            'user_orders': orders,
            'user': user,
            'movies_purchased': total_movies,
        }
        return TemplateResponse(
            request,
            'admin/order_summary.html',
            template_data
        )