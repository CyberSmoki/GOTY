from django.shortcuts import redirect
from django.http import HttpResponse
from app.oauth2 import DiscordWrapper, get_oauth2_link, get_avatar_link
from django.shortcuts import render
from django.conf import settings
import datetime
import random
from icecream import ic
from .models import Game

def index(request) -> HttpResponse:
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

    all_games = Game.objects.all()
    games_ids = list(map(lambda game: game.id, all_games))

    scores = {}

    total_votes = random.randint(1, 100_000)
    for game in all_games:
        id = game.id
        yes = random.randint(0, total_votes//2)
        no = random.randint(0, total_votes//2)
        scores[id] = {'yes': yes, 'no': no}

    scores = dict(sorted(scores.items(), key=lambda item: item[1]['no']))
    scores = dict(sorted(scores.items(), key=lambda item: item[1]['yes'] - item[1]['no'], reverse=True))
    yes_scores = list(map(lambda k: scores[k]['yes'], scores))
    no_scores = list(map(lambda k: scores[k]['no'], scores))
    margin_scores = [yes_scores[i] - no_scores[i] for i in range(len(scores))]
    game_names = list(map(lambda k: all_games.get(id=k).name, scores))

    best_ids = list(scores)[:6]
    worst_ids = list(scores)[-6:]

    best_games = list(map(lambda k: all_games.get(id=k), list(scores)[:6]))
    worst_games = list(map(lambda k: all_games.get(id=k), list(scores)[-6:]))

    ic(best_games)
    ic(worst_games)

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
            'results': {
                'best_games': {
                    'data': best_games,
                    'scores': margin_scores[:6],
                },
                'worst_games': {
                    'data': worst_games,
                    'scores': margin_scores[-6:],
                },
                'scores': {
                    'games': game_names,
                    'yes': yes_scores,
                    'no': no_scores,
                },
                'total_votes': total_votes,
            },
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
