from app.models import Game, Votes, get_votes, get_finalists
from app.oauth2 import DiscordWrapper, get_oauth2_link, get_avatar_link
import datetime
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.db.models import Count, Q
import json
from urllib.parse import unquote
import uuid


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

    stage = 1 if status in ['waiting', 'active', 'waiting_for_runoff'] else 2
    results_stage_1 = None
    results_stage_2 = None

    if status in ['waiting_for_runoff', 'runoff', 'finished']:
        all_games = Game.objects.all()
        results = get_votes(1).order_by('-margin', 'positive')
        games_count = len(all_games)
        distinct_voters_count = Votes.objects.filter(stage=1).aggregate(
            distinct_voters=Count('user_id', distinct=True)
        )['distinct_voters']
        votes_count = Votes.objects.filter(stage=1).aggregate(
            total=Count('id'),
            positive=Count('id', filter=Q(value=1)),
            negative=Count('id', filter=Q(value=-1)),
        )

        best_games, worst_games = get_finalists(stage)

        results_stage_1 = {
            'best_games': best_games,
            'worst_games': worst_games,
            'scores': {
                'games': results,
            },
            'games_count': games_count,
            'total_voters': distinct_voters_count,
            'total_votes': votes_count['total'],
            'positive_votes': votes_count['positive'],
            'negative_votes': votes_count['negative'],
        }
        if status == 'finished':
            results_2 = get_votes(2).order_by('-margin', 'positive')
            games_count_2 = len(best_games) + len(worst_games)
            distinct_voters_count_2 = Votes.objects.filter(stage=2).aggregate(
                distinct_voters=Count('user_id', distinct=True)
            )['distinct_voters']
            votes_count_2 = Votes.objects.filter(stage=2).aggregate(
                total=Count('id'),
                positive=Count('id', filter=Q(value=1)),
                negative=Count('id', filter=Q(value=-1)),
            )

            results_stage_2 = {
                'best_games': best_games,
                'worst_games': worst_games,
                'scores': {
                    'games': results_2,
                },
                'games_count': games_count_2,
                'total_voters': distinct_voters_count_2,
                'total_votes': votes_count_2['total'],
                'positive_votes': votes_count_2['positive'],
                'negative_votes': votes_count_2['negative'],
                'best_game': best_games[0],
                'worst_game': worst_games[0],
            }

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
            'results_stage_2': results_stage_2,
        }
    )


def vote(request) -> HttpResponse:
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

    current_active_stage = 1 if status == 'active'\
        else 2 if status == 'runoff'\
        else None

    stage = request.GET.get('stage', current_active_stage)
    user = request.session.get('user', None)

    if stage not in ['1', '2']:
        return HttpResponseNotFound('Podana tura nie istnieje')
    if not user:
        return redirect("login")

    stage = int(stage)

    if stage == 2 and status in ['waiting', 'active']:
        return HttpResponseNotFound('Podana tura nie istnieje')
    locked_vote = stage != current_active_stage

    if stage == 1:
        games = get_votes(1)
    elif stage == 2:
        best_games, worst_games = get_finalists()
        games = {
            'best': best_games,
            'worst': worst_games,
        }
    else:
        games = None
        stage = None

    user_votes = (
        {
            game_vote['game_id']: game_vote['value']
            for game_vote in Votes.objects.filter(
                user_id=user['id'],
                stage=stage,
            ).values('game_id', 'value')
        }
    )

    return render(
        request,
        template_name='vote.html',
        context={
            'games': games,
            'locked_vote': locked_vote,
            'stage': stage,
            'user_name': user['name']
            if user is not None
            else None,
            'user_avatar': get_avatar_link(user)
            if user is not None
            else None,
            'user_votes': user_votes,
        }
    )


def vote_post(request) -> JsonResponse:
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

    stage_statuses = {
        'active': 1,
        'runoff': 2,
    }

    if status not in stage_statuses:
        return JsonResponse({'status': '403', 'reason': 'Voting is inactive'})

    user = request.session.get('user')
    if user is None:
        return JsonResponse({'status': '401', 'reason': 'User is not logged in'})

    data = request.body
    data = str(data, encoding='utf-8')
    data = unquote(data)
    data = json.loads(data)


    stage = data.get('stage')
    if stage_statuses[status] != stage:
        return JsonResponse({'status': '403', 'reason': 'Wrong stage of voting'})

    game_id = data.get('gameId')

    vote_value = data.get('vote')

    stage_votes = {
        'active': [-1, 0, 1],
        'runoff': ["best", "worst"],
    }

    if stage == 1 and vote_value not in stage_votes[status]:
        return JsonResponse({'status': '403', 'reason': 'Wrong vote value'})

    stage_games = {
        1: list(value['id'] for value in Game.objects.all().values('id')),
        2: list(value['id'] for value in get_finalists()[{'best': 0, 'worst': 1}[vote_value]].values('id')),
    }

    game_uuid = uuid.UUID(game_id) if game_id is not None else None
    if game_id is None or game_uuid not in stage_games[stage]:
        return JsonResponse({'status': '400', 'reason': 'Tried to vote for nonexistent game'})

    if stage == 1:
        Votes.objects.update_or_create(
            user_id=user['id'],
            game_id_id=game_id,
            stage=stage,
            defaults={'value': vote_value}
        )
    elif stage == 2:
        value = 1 if vote_value == 'best'\
            else -1 if vote_value == 'worst'\
            else 0
        previous = Votes.objects.filter(
            user_id=user['id'],
            stage=stage,
            value=value,
        )
        if previous:
            previous = previous[0]
            previous_game_id = previous.game_id_id
            previous.delete()
        else:
            previous_game_id = None

        if previous_game_id is None or previous_game_id != game_uuid:
            Votes.objects.update_or_create(
                user_id=user['id'],
                game_id_id=game_id,
                stage=stage,
                value=value,
            )
    return JsonResponse({'status': '200'})


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


def logout(request):
    request.session.flush()
    return redirect("index")
