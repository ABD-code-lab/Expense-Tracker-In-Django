from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # Income
    path('income/', views.income_list, name='income_list'),
    path('income/add/', views.income_add, name='income_add'),
    path('income/edit/<int:id>/', views.income_edit, name='income_edit'),
    path('income/delete/<int:id>/', views.income_delete, name='income_delete'),

    # Expense
    path('expense/', views.expense_list, name='expense_list'),
    path('expense/add/', views.expense_add, name='expense_add'),
    path('expense/edit/<int:id>/', views.expense_edit, name='expense_edit'),
    path('expense/delete/<int:id>/', views.expense_delete, name='expense_delete'),
]
