from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required    
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .models import expense, income, category
from datetime import datetime  
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.http import FileResponse
import os 
from finances.settings import BASE_DIR
import datetime

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='/authenticate/login')
def index(request):
    print("I came here")
    return render(request, "_user/dashboard_view.html")

def accountSettings(request, user):
    print(user)
    return render(request, "_user/accountSettings.html")

def expenses(request):
    categories = category.objects.all()
    if request.method == "POST":
        context  = {
            "amount": request.POST["amount"],
            "description": request.POST["description"],
            "date": request.POST["date"],
            "category": request.POST["category"],
        }
        if context["date"] == "" and context["description"] != "":
            newexpense = expense.objects.create(amount = context["amount"], description = context["description"], category = context["category"])
        elif context["date"] != "" and context["description"] == "":
            newexpense = expense.objects.create(amount = context["amount"], date = context["date"], category = context["category"])
        elif context["date"] == "" and context["description"] == "":
            newexpense = expense.objects.create(amount = context["amount"], category = context["category"])
        else:
            newexpense = expense.objects.create(amount = context["amount"], date = context["date"], description = context["description"], category = context["category"])
        newexpense.uid = request.user.id
        if 'file' in request.FILES:
            print('file found')
            uploaded_file = request.FILES['file']
            newexpense.file = uploaded_file
        newexpense.save()
        messages.success(request, "New Expense Added Successfully")
        return redirect("expenses")
    else:
        allexpenses = expense.objects.filter(uid = request.user.id)
        newpaginator = Paginator(allexpenses, 5)
        page_num = request.GET.get('page')
        page_obj = Paginator.get_page(newpaginator, page_num)
        return render(request, "_user/expenses.html", {"expenses": allexpenses, "categories": categories, "page_obj":page_obj})
    
def expenseEdit(request, id):
    categories = category.objects.all()
    if request.method == "POST":
        context  = {
            "amount": request.POST["amount"],
            "description": request.POST["description"],
            "date": request.POST["date"],
            "category": request.POST["category"],
        }
        currexpense =  expense.objects.get(pk=id)
        if context["description"] != "":
            currexpense.description = context["description"]
        if context["date"] != "":
            currexpense.date = context["date"]
        currexpense.amount = context["amount"]
        currexpense.category = context["category"]
        if 'file' in request.FILES:
            print('file found')
            uploaded_file = request.FILES['file']
            currexpense.file = uploaded_file
        currexpense.save()
        messages.success(request, "Updated Expense Successfully")
        return redirect("expenses")

    else:
        context = {
            "currexpense": expense.objects.get(pk = id),
        }
        return render(request, "_user/expense_edit.html", {"data": expense.objects.get(pk = id), "categories": categories})
    
def deleteExpense(request, pk):
    messages.success(request, "Expense deleted successfully")
    expense.objects.get(pk = pk).delete()
    return redirect("expenses")

def searchview_expense(request):
    allexpenses = expense.objects.filter(uid = request.user.id)
    search_str = json.loads(request.body).get("query")
    responseList = expense.objects.filter(
        amount__startswith = search_str, uid = request.user.id) | expense.objects.filter(
        date__startswith = search_str, uid = request.user.id) | expense.objects.filter(
        description__icontains = search_str, uid = request.user.id) | expense.objects.filter(
        category__icontains = search_str, uid = request.user.id) 
    data = responseList.values()
    print(responseList)
    return JsonResponse(list(data), safe=False)


def earnings(request):
    categories = category.objects.all()

    if request.method == "POST":
        context = {
            "amount": request.POST["amount"],
            "category": request.POST["category"],
            "date": request.POST["date"],
            "description": request.POST["description"],
        }

        if context["date"] == "" and context["description"] != "":
            newearning = income.objects.create(amount = context["amount"], description = context["description"], category = context["category"])
        elif context["date"] != "" and context["description"] == "":
            newearning = income.objects.create(amount = context["amount"], date = context["date"], category = context["category"])
        elif context["date"] == "" and context["description"] == "":
            newearning = income.objects.create(amount = context["amount"], category = context["category"])
        else:
            newearning = income.objects.create(amount = context["amount"], date = context["date"], description = context["description"], category = context["category"])
        newearning.uid = request.user.id
        print(request)
        if 'file' in request.FILES:
            print('file found')
            uploaded_file = request.FILES['file']
            newearning.file = uploaded_file
        newearning.save()

        messages.success(request, "Earning added Successfully")
        return redirect("earnings")
        
    else:
        allearnings = income.objects.filter(uid = request.user.pk)
        context= {
            "categories": categories,
            "earnings": allearnings,
        }
        return render(request, "_user/earnings.html", context)

def earningEdit(request, id):
    categories = category.objects.all()
    if request.method == "POST":
        earning = income.objects.get(pk = id)
        context  = {
            "amount": request.POST["amount"],
            "description": request.POST["description"],
            "date": request.POST["date"],
            "category": request.POST["category"],
        }
        if context["description"] != "":
            earning.description = context["description"]
        if context["date"] != "":
            earning.date = context["date"]
        earning.amount = context["amount"]
        earning.category = context["category"]
        print("request--> ", request)
        if 'file' in request.FILES:
            print('file found')
            uploaded_file = request.FILES['file']
            earning.file = uploaded_file
        earning.save()
        messages.success(request, "Updated Expense Successfully")
        return redirect("earnings")
    else:
        context = {
            "data": income.objects.get(pk = id),
            "categories": categories,
        }
        return render(request, "_user/earning_edit.html", context)

def deleteEarning(request, pk):
    income.objects.get(pk = pk).delete()
    messages.success(request, "Earning deleted successfully")
    return redirect('earnings')

def searchview_income(request):
    earnings = income.objects.filter(uid = request.user.id)
    search_str = json.loads(request.body).get("query")
    responseList = income.objects.filter(
        amount__startswith = search_str, uid = request.user.id) | income.objects.filter(
        date__startswith = search_str, uid = request.user.id) | income.objects.filter(
        description__icontains = search_str, uid = request.user.id) | income.objects.filter(
        category__icontains = search_str, uid = request.user.id) 
    data = responseList.values()
    print(responseList)
    return JsonResponse(list(data), safe=False)

def download_file(request, file_name):
    # Determine the file path on the server
    file_path = os.path.join(BASE_DIR, file_name)

    # Open the file
    file = open(file_path, 'rb')

    # Create a FileResponse object with the file
    response = FileResponse(file)

    # Set the appropriate content type for the response
    response['Content-Type'] = 'application/pdf'

    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = 'attachment; filename=' + file_name

    return response

def charts_endpoint(request):
    today = datetime.date.today()
    month_6 = today - datetime.timedelta(days = 180)
    
    expenses = expense.objects.filter(uid = request.user.id, date__gte = today, date__lte = month_6)
    
    def getCategory(expnse):
        return expense.category
    categories = list(set(map(getCategory, expenses)))
    

    finalrep = {}
    for category in categories:
        sum = 0
        for item in expenses:
            if item.category == category:
                sum = sum + item.amount
        
        finalrep["category"] = sum

    return JsonResponse({"expenseCategoryData":finalrep}, safe=False)

def charts(request):
    return render(request, "_user/charts.html")