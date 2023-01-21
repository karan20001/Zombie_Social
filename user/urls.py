from django.urls import path
from .views import LoginView, UserReportingView, UserTradingingView, UserView, LogoutView, ReportsView, UserLocationView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('', UserView.as_view()),
    path('<int:user_id>', UserLocationView.as_view()),
    path('<int:user_id>/mark_infected', UserReportingView.as_view()),
    path('<int:user_id>/trade', UserTradingingView.as_view()),
    path('reports', ReportsView.as_view()),
    path('logout', LogoutView.as_view())
]