# stock_tracker/urls.py
from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/realtime/', views.fetch_realtime_data),
    path('api/portfolio-value/', views.get_portfolio_value),
    path('api/simulate-trade/', views.simulate_trade),
]
