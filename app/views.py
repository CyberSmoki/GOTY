from django.shortcuts import redirect
from django.http import HttpResponse
from app.oauth2 import DiscordWrapper, get_oauth2_link

def index(request) -> HttpResponse:
    if not request.session.get('user', None):
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <a href="{get_oauth2_link()}">Authorize</a>
        </body>
        </html>
        """)
    else:
        user = request.session.get('user')
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <p>
        <img style="border-radius: 48px; height: 96px;" src="https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}?size=96">
        <h3>{user['name']}</h3>
        </p>
        <a href="/app/logout">Logout</a>
        </body>
        </html>
        """)

def oauth2(request) -> HttpResponse:
    if request.session.get('user', None):
        return redirect("index")
    wrapper = DiscordWrapper()
    if 'code' in request.GET:
        code = request.GET['code']
        result = wrapper.process_code(code)
        if result is None:
            return redirect("index")
        request.session['user'] = {
            'id': result['id'],
            'name': result['username'],
            'avatar': result['avatar'],
        }
        return redirect("index")
    return HttpResponse("404")

def logout(request):
    request.session.flush()
    return redirect("index")
