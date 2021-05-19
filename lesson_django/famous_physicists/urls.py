from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', PhysicistsHome.as_view(), name='home'),
    path('about/', cache_page(60)(About.as_view()), name='about'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('sign_in/', SignInUser.as_view(), name='sign_in'),
    path('logout/', logout_user, name='logout'),
    path('sign_up/', RegisterUser.as_view(), name='sign_up'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', PhysicistsCategory.as_view(), name='category'),
]
