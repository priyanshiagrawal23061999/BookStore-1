from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
import pdb

urlpatterns = [
#Forget Password
# pdb.set_trace()
path('reset_password/',auth_views.PasswordResetView.as_view(
        template_name="Auth/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(
        template_name="Auth/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name="Auth/password_reset_form.html"),
        name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name="Auth/password_reset_done.html"),
        name="password_rest_complete"),

    #      path('/login/token/', jwt_views.TokenObtainPairView.as_view(), name='gettoken'),
    # path('/api/testing/', views.TestApiView.as_view(), name='gettoken')

    

    
    # body = {
    #     'email':'abcd@gmail.com',
    #     'password':'api@gmail.com',
    #    }
    # await Axios.post('http://127.0.0.1:8000/login/token/', body);
    


]
