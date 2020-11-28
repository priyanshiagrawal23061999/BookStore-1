from django.contrib import admin
from django.urls import path, include
from books import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url

from django.conf.urls.static import static
from book_store import settings
import pdb
# from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
   
    path('', views.index, name='index'),
    path('search/', views.search,name='search'),
    url(r'^cate/(?P<prod_id>[0-9]+)', views.cate, name='cate'),
    url(r'^sprod/(?P<prod_id>[0-9]+)', views.sprod, name='sprod'),

    #*****************Forgot Password***********************'''
    # path('reset_password/',auth_views.PasswordResetView.as_view(
    #     template_name="Auth/password_reset.html"),
    #      name="reset_password"),

    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(
    #     template_name="Auth/password_reset_sent.html"),
    #     name="password_reset_done"),

    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
    #     template_name="Auth/password_reset_form.html"),
    #     name="password_reset_confirm"),

    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(
    #     template_name="Auth/password_reset_done.html"),
    #     name="password_rest_complete"),

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
