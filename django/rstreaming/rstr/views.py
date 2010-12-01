# from django.views.decorators.vary import vary_on_headers
from django.views.decorators.vary import vary_on_cookie
# from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from rstr.config import Config
from rstr.mainviewer import MainViewer
import logging

# @vary_on_header s('Cookie')
# @cache_control(private=True, must_revalidate=True, max_age=3600)
@never_cache
@vary_on_cookie
def index(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    request.session.clear()
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
    return MainViewer(request, request.session.session_key).getViewer()

# def error(request):
    # p = get_object_or_404(Poll, pk=poll_id)

def auth_login(request):
    if request.method == 'POST':
        if request.session['user'].is_authenticated():
            messages.add_message(request, messages.ERROR, 'User already logged in')
            if request.META['HTTP_REFERER'] is not None:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponse(reverse('index'))
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'User logged in')
                request.session['user'] = user
                if request.META['HTTP_REFERER'] is not None:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponse(reverse('index'))
            else:
                # Return a 'disabled account' error message
                messages.add_message(request, messages.ERROR, 'Your account is disabled.')
                if request.META['HTTP_REFERER'] is not None:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponse(reverse('index'))
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.ERROR, 'Username or password error.')
            if request.META['HTTP_REFERER'] is not None:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponse(reverse('index'))
    elif request.method == 'GET':
        return HttpResponse("Login.")
    else:
        raise Http404

def auth_logout(request):
    if request.session['user'].is_authenticated():
        logout(request)
        messages.add_message(request, messages.INFO, 'User logged out.')
        if request.META['HTTP_REFERER'] is not None:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse(reverse('index'))
    else:
        messages.add_message(request, messages.ERROR, 'User not logged in.')
        if request.META['HTTP_REFERER'] is not None:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse(reverse('index'))