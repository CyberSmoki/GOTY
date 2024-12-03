from django.shortcuts import redirect
from django.http import HttpResponse
from app.oauth2 import DiscordWrapper, get_oauth2_link, get_avatar_link
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseNotFound
import datetime
import random
from icecream import ic
from django.db.models import Count, Q
from .models import Game, Votes

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

    if status in ['waiting_for_runoff', 'runoff', 'finished']:
        best_indices = slice(None, 6)
        worst_indices = slice(-6, None)

        all_games = Game.objects.all()
        results = (
            Votes.objects
            .select_related('game_id')  # Fetch related Game data
            .values('game_id', 'game_id__name', 'game_id__developer', 'stage')  # Grouping fields
            .annotate(
                positive_votes=Count('value', filter=Q(value=1)),  # Count votes = 1
                negative_votes=Count('value', filter=Q(value=-1))  # Count votes = -1
            )
        )
        games_count = len(all_games)
        total_votes_count = Votes.objects.aggregate(
            total_votes=Count('id')
        )['total_votes']
        distinct_voters_count = Votes.objects.aggregate(
            distinct_voters=Count('user_id', distinct=True)
        )['distinct_voters']
        positive_votes_count = Votes.objects.aggregate(
            positive_votes=Count('id', filter=Q(value=1))
        )['positive_votes']
        negative_votes_count = Votes.objects.aggregate(
            negative_votes=Count('id', filter=Q(value=-1))
        )['negative_votes']

        scores = {}

        for row in results:
            id = row['game_id']
            yes = row['positive_votes']
            no = row['negative_votes']
            scores[id] = {'yes': yes, 'no': no}


        scores = dict(sorted(scores.items(), key=lambda item: item[1]['no']))
        scores = dict(sorted(scores.items(), key=lambda item: item[1]['yes'] - item[1]['no'], reverse=True))
        yes_scores = list(map(lambda k: scores[k]['yes'], scores))
        no_scores = list(map(lambda k: scores[k]['no'], scores))
        margin_scores = [yes_scores[i] - no_scores[i] for i in range(len(scores))]
        game_names = list(map(lambda k: all_games.get(id=k).name, scores))

        best_games = list(map(lambda k: all_games.get(id=k), list(scores)[best_indices]))
        worst_games = list(map(lambda k: all_games.get(id=k), list(scores)[worst_indices]))

        ic(best_games)
        ic(worst_games)
        results_stage_1 = {
            'best_games': {
                'data': best_games,
                'margins': margin_scores[best_indices],
                'positive': yes_scores[best_indices],
                'negative': no_scores[best_indices],
            },
            'worst_games': {
                'data': worst_games,
                'margins': margin_scores[worst_indices],
                'positive': yes_scores[worst_indices],
                'negative': no_scores[worst_indices],
            },
            'scores': {
                'games': game_names,
                'yes': yes_scores,
                'no': no_scores,
            },
            'games_count': games_count,
            'total_votes': total_votes_count,
            'total_voters': distinct_voters_count,
            'positive_votes': positive_votes_count,
            'negative_votes': negative_votes_count,
        }
    else:
        results_stage_1 = None

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
            'results_stage_1': results_stage_1,
        }
    )

def vote(request, stage: str) -> HttpResponse:
    user = request.session.get('user', None)
    if stage not in ['1', '2']:
        return HttpResponseNotFound('Podana tura nie istnieje')
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
