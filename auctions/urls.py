from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:id>", views.item, name="item"),
    path("add/<int:id>", views.add, name="add"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("mylist", views.mylist, name="mylist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("categories", views.categories, name="categories"),
    path("<str:category>", views.clisting, name="clisting")

]
