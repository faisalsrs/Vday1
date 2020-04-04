from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('new_account', views.new_account),  # POST
    path('new_gift', views.new_gift),
    path('submit_a_new_gift', views.submit_a_new_gift),  # GET
    path('giftwall', views.giftwall),  # GET
    path('logout', views.logout),  # GET
    path('login', views.login),
    path('unique', views.unique),  # POST
    path('works', views.works),
    path('grantor_login', views.grantor_login),
    path('grantor_page', views.grantor_page),
    path('gift/edit/<int:id>', views.edit_gift),  # GET
    path('gift/update/<int:id>', views.update_gift),
    path('gift/delete/<int:id>', views.delete)
]
