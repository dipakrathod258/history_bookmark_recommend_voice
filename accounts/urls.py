from django.urls import path

from .views import SignUpView
from .views import ContactUsView
from .views import AboutUsView
from .views import ThankYouView
from .views import ProductHistoryView
from .views import ThankYouBookmarkView
from accounts import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('thank_you/', ThankYouView.as_view(), name='thank_you'),
    path('product_history/', ProductHistoryView.as_view(), name='product_history'),
    path('thank_you_bookmark/', ThankYouBookmarkView.as_view(), name='thank_you_bookmark'),
    path('create_post', views.create_post, name='create_post'),
    path('textToSpeech', views.textToSpeech, name='textToSpeech'),
    path('save_contact', views.saveContact, name='save_contact'),
]
