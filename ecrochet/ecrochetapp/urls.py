from django.urls import path
from ecrochetapp import views
from django.conf import settings
from django.conf.urls.static import static 
from ecrochet import settings


urlpatterns = [
    path('index',views.index),
    path('pdetails/<pid>',views.pdetails),

    path('viewcart',views.viewcart),

    path('register',views.register),
    path('ulogin', views.ulogin),
    path('ulogout', views.ulogout),

    path('pdetails/<pid>', views.pdetails),

    path('patterns', views.patterns, name='patterns'),
    path('pattern/<int:pid>', views.pattern_details, name='pattern_details'),

    path('placeorder', views.placeorder),

    path('addtocart/<pid>', views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>', views.updateqty),

    path('makepayment',views.makepayment),
    path('sendusermail',views.sendusermail),

    path('search', views.search, name='search'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)