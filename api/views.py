from django.shortcuts import render


def developer_page(request):
    return render(request, "api/developer.html")
