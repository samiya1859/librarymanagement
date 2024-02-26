
from django.urls import path
from . import views
from book.views import AddReview,borrow_history

urlpatterns = [
    path('signup/',views.UserSignupView.as_view(),name='signup'),

    path('logout/',views.user_logout,name='logout'),

    path('login/',views.UserLoginView.as_view(),name='login'),

    path('profile/<int:id>',views.Profileview.as_view(),
    name='profile'),

    path('update/',views.UserAccountUpdate.as_view(),name='update'),

    path('passchange/',views.PasswordChange.as_view(),name='passchange'),

    path('profile/borrowhis/',borrow_history,name='borrow_history'),

    path('profile/borrowhis/review/<int:book_id>/',AddReview.as_view(),name='review'),
    
]


