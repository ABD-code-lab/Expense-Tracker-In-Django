from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Income, Expense
from django.shortcuts import render, redirect
from .models import User
from django.db.models import Sum

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User not found'})

    return render(request, 'login.html')


def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    total_income = Income.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expense = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance = total_income - total_expense

    transactions_count = Expense.objects.all().count()

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'transactions_count' : transactions_count,
    }

    return render(request, 'dashboard.html', context)


def logout_view(request):
    request.session.flush()
    return redirect('login')



def current_user(request):
    uid = request.session.get('user_id')
    if not uid:
        return None
    return User.objects.get(id=uid)

# -------- INCOME --------

def income_list(request):
    user = current_user(request)
    if not user:
        return redirect('login')

    incomes = Income.objects.filter(user=user)
    total_income = Income.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    return render(request, 'income/income_list.html', {'incomes': incomes, 'total_income': total_income})


def income_add(request):
    user = current_user(request)
    if not user:
        return redirect('login')

    if request.method == "POST":
        Income.objects.create(
            user=user,
            title=request.POST['title'],
            amount=request.POST['amount'],
            notes=request.POST['notes'],
            date=request.POST['date']
        )
        return redirect('income_list')

    return render(request, 'income/income_form.html')


def income_edit(request, id):
    user = current_user(request)
    income = get_object_or_404(Income, id=id, user=user)

    if request.method == "POST":
        income.title = request.POST['title']
        income.amount = request.POST['amount']
        income.notes = request.POST['notes']
        income.date = request.POST['date']
        income.save()
        return redirect('income_list')

    return render(request, 'income/income_form.html', {'income': income})


def income_delete(request, id):
    user = current_user(request)
    income = get_object_or_404(Income, id=id, user=user)
    income.delete()
    return redirect('income_list')


# -------- EXPENSE --------

def expense_list(request):
    user = current_user(request)
    if not user:
        return redirect('login')

    expenses = Expense.objects.filter(user=user)
    total_expense = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    return render(request, 'expense/expense_list.html', {'expenses': expenses, 'total_expense': total_expense})


def expense_add(request):
    user = current_user(request)
    if not user:
        return redirect('login')

    if request.method == "POST":
        Expense.objects.create(
            user=user,
            title=request.POST['title'],
            amount=request.POST['amount'],
            notes=request.POST['notes'],
            date=request.POST['date']
        )
        return redirect('expense_list')

    return render(request, 'expense/expense_form.html')


def expense_edit(request, id):
    user = current_user(request)
    expense = get_object_or_404(Expense, id=id, user=user)

    if request.method == "POST":
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.notes = request.POST['notes']
        expense.date = request.POST['date']
        expense.save()
        return redirect('expense_list')

    return render(request, 'expense/expense_form.html', {'expense': expense})


def expense_delete(request, id):
    user = current_user(request)
    expense = get_object_or_404(Expense, id=id, user=user)
    expense.delete()
    return redirect('expense_list')
