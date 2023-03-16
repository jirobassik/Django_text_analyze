from django.shortcuts import render

def greet_view(request):
    return render(request, 'greeting/greeting.html')
