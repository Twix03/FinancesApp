from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="index"),
    path('<str:user>/accountSettings/', views.accountSettings, name="accountSettings"),
    path('expenses/', views.expenses, name="expenses"),
    path('expense/update/<int:id>', views.expenseEdit, name="expense-edit"),
    path('expense/delete/<int:pk>', views.deleteExpense, name = "delete_expense"),
    path('expenses/search', csrf_exempt(views.searchview_expense), name="searchview_expense"),
    
    path('download/<str:file_name>/', views.download_file, name='download'),
    
    path('revenue/', views.earnings, name="earnings"),
    path('revenue/update/<int:id>', views.earningEdit, name="earning-edit"),
    path('revenue/delete/<int:pk>', views.deleteEarning, name = "delete_earning"),
    path('revenue/search', csrf_exempt(views.searchview_income), name="searchview_income"),

    path('charts/endpoint', views.charts_endpoint, name="charts_endpoint"),
    path('charts', views.charts, name="charts")


]