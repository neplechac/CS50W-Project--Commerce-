from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.show_listing, name="show_listing"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("bid/<int:listing_id>", views.bid_submit, name="bid_submit"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist", views.show_watchlisted, name="watchlisted"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("categories", views.show_categories, name="categories"),
    path("category/<str:name>", views.show_category, name="category")
]
