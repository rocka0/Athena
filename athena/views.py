from django.shortcuts import redirect, render

from users.views import isUserLoggedIn

# Create your views here.


def landingPage(request):
    user = isUserLoggedIn(request)
    if user:
        return redirect('userProfile')

    return render(request, 'athena/landingPage.html', {})
