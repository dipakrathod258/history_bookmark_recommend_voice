from django.urls import path

from .views import SignUpView
from .views import ContactUsView
from .views import AboutUsView
from .views import ThankYouView
from .views import ProductHistoryView
from accounts import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('thank_you/', ThankYouView.as_view(), name='thank_you'),
    path('product_history/', ProductHistoryView.as_view(), name='product_history'),
    path('create_post', views.create_post, name='create_post'),
    path('textToSpeech', views.textToSpeech, name='textToSpeech'),
]
