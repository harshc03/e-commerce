from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.

def main(request):
    return redirect('home_page')
