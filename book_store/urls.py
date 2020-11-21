from django.contrib import admin
from django.urls import path
from books import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url

from django.conf.urls.static import static
from book_store import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.reg, name='reg'),
    path('forgot/', views.forgot, name='forgot'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search,name='search'),
    url(r'^cate/(?P<prod_id>[0-9]+)', views.cate, name='cate'),
    url(r'^sprod/(?P<prod_id>[0-9]+)', views.sprod, name='sprod'),

    #---------------- Provider ------------------

    path('prohome/',views.pro_home,name='pro_home'),
    path('probook/',views.pro_add_book,name='pro_add_book'),
    path('proreport/',views.pro_report,name='pro_report'),
    # ---------------- Customer ------------------

    path('cart/', views.cart, name='cart'),
    path('cart0/', views.cart0, name='cart0'),
    path('orders/', views.orders, name='orders'),
    path('account/', views.account, name='account'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
