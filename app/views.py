from django.shortcuts import redirect
from django.http import HttpResponse
from app.oauth2 import DiscordWrapper, get_oauth2_link, get_avatar_link
from django.shortcuts import render
from django.conf import settings
import datetime
from icecream import ic

def index(request) -> HttpResponse:
    ic(request.session.get('user', None))
    if not request.session.get('user', None):
        return render(
            request,
            template_name='login.html'
        )
    else:
        return redirect("results", permanent=True)

def login(request) -> HttpResponse:
    return redirect(get_oauth2_link(), permanent=True)

def results(request) -> HttpResponse:
    user = request.session.get('user', None)
    stage = 1
    now = datetime.date.today()
    stage_1_start = datetime.date.fromisoformat(settings.STAGES['1']['start'])
    stage_1_end = datetime.date.fromisoformat(settings.STAGES['1']['end'])
    stage_2_start = datetime.date.fromisoformat(settings.STAGES['2']['start'])
    stage_2_end = datetime.date.fromisoformat(settings.STAGES['2']['end'])
    status = 'waiting' if now < stage_1_start\
        else 'active' if now <= stage_1_end\
        else 'waiting_for_runoff' if now < stage_2_start\
        else 'runoff' if now <= stage_2_end\
        else 'finished'

    return render(
        request,
        template_name='results.html',
        context={
            'user_name': user['name'] if user is not None else None,
            'user_avatar': get_avatar_link(user) if user is not None else None,
            'current_stage': stage,
            'stage_1_start': stage_1_start,
            'stage_1_end': stage_1_end,
            'stage_2_start': stage_2_start,
            'stage_2_end': stage_2_end,
            'status': status,
            'top_games': None,
            'worst_games': None,
            'results': None,
        }
    )

def vote(request, stage: str) -> HttpResponse:
    user = request.session.get('user', None)
    if stage not in ['1', '2']:
        return redirect("page404")
    if not user:
        return redirect("login")
    return render(
        request,
        template_name='vote.html',
        context={
            'user_name': user['name'] if user is not None else None,
            'user_avatar': get_avatar_link(user) if user is not None else None,
        }
    )

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
            'name': result['global_name'],
            'avatar': result['avatar'],
        }
        return redirect("index")
    return redirect("page404")

def logout(request):
    request.session.flush()
    return redirect("index")
