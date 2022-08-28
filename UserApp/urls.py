from django.urls import path
from UserApp.views import user_logout, user_login, user_register, userprofile, user_update, user_password, user_comment, comment_delete
urlpatterns = [
    path('logout/', user_logout, name='user_logout'),
    path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_signup'),
    path('profile/', userprofile, name='userprofile'),
    path('user_update/', user_update, name='user_update'),
    path('password_update/', user_password, name='user_password'),
    path('user_comment/', user_comment, name='user_comment'),
    path('comment_delete/<int:id>', comment_delete, name='comment_delete'),
]