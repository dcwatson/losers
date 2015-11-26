from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import League, Game, Login, Team, Pick
from .utils import player_required

LOGIN_EMAIL = """
You may log in using the link below:

%(link)s

If you did not request this email, please disregard.
""".strip()

def login(request, code=None):
    if code:
        try:
            token = Login.objects.get(code=code)
        except Login.DoesNotExist:
            return redirect('login')
        league = get_object_or_404(League, current=True)
        player, created = league.players.get_or_create(email=token.email)
        request.session['player_id'] = player.pk
        token.delete()
        return redirect('pick')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if email:
            token = Login.objects.create(email=email)
            link = request.build_absolute_uri('/login/%s/' % token.code)
            msg = LOGIN_EMAIL % {'link': link}
            send_mail('Loser League Login', msg, settings.DEFAULT_FROM_EMAIL, [email])
        return render(request, 'login_sent.html', {
            'email': email,
        })
    return render(request, 'login.html', {
    })

def logout(request):
    try:
        del request.session['player_id']
    except:
        pass
    return redirect('login')

@player_required
def pick(request):
    current_week = Game.objects.latest('game_date').week
    my_pick = request.player.picks.filter(week=current_week).first()
    # Get a list of all the games this week.
    games = list(Game.objects.filter(year=request.player.league.year, week=current_week).select_related('home_team', 'away_team', 'winner', 'loser'))
    exclude_ids = set()
    locked = False
    # If the first game on sunday has started, picks are locked. Otherwise, don't allow the player to pick any team
    # whose game has already started.
    for g in games:
        if g.started:
            exclude_ids.add(g.home_team_id)
            exclude_ids.add(g.away_team_id)
            if g.sunday:
                locked = True
    # Lock the winner/loser picks if the games have started.
    winner_started = my_pick.winner_id in exclude_ids if my_pick else False
    loser_started = my_pick.loser_id in exclude_ids if my_pick else False
    # Don't let players pick any team they've picked before.
    for pick in request.player.picks.filter(week__lt=current_week):
        exclude_ids.update([pick.winner_id, pick.loser_id])
    remaining_teams = list(Team.objects.exclude(pk__in=exclude_ids))
    all_picks = Pick.objects.filter(player__league=request.player.league, week=current_week) if locked else []
    if request.method == 'POST':
        if locked:
            messages.error(request, 'Picks for this week have been locked.')
            return redirect('pick')
        if 'winner' in request.POST:
            # If submitting a new pick, make sure the game hasn't started, and it's not a repeat pick.
            winner = Team.objects.get(pk=request.POST['winner'])
            if winner not in remaining_teams:
                messages.error(request, 'You selected a team that you previously picked, or has already played their game.')
                return redirect('pick')
        else:
            # Otherwise, use the already-picked winner.
            winner = my_pick.winner
        if 'loser' in request.POST:
            # If submitting a new pick, make sure the game hasn't started, or it's not a repeat pick.
            loser = Team.objects.get(pk=request.POST['loser'])
            if loser not in remaining_teams:
                messages.error(request, 'You selected a team that you previously picked, or has already played their game.')
                return redirect('pick')
        else:
            # Otherwise, use the already-picked loser.
            loser = my_pick.loser
        if winner == loser:
            messages.error(request, 'You cannot select the same team to win and lose.')
            return redirect('pick')
        for g in games:
            if set([g.home_team, g.away_team]) == set([winner, loser]):
                messages.error(request, 'You cannot select a winner and loser from the same game.')
                return redirect('pick')
        if my_pick:
            my_pick.winner = winner
            my_pick.loser = loser
            my_pick.save()
        else:
            request.player.picks.create(week=current_week, winner=winner, loser=loser)
        messages.success(request, 'Your pick for this week has been saved.')
        return redirect('pick')
    return render(request, 'pick.html', {
        'player': request.player,
        'games': games,
        'pick': my_pick,
        'week': current_week,
        'locked': locked,
        'all_picks': all_picks,
        'remaining_teams': remaining_teams,
        'winner_started': winner_started,
        'loser_started': loser_started,
    })

@player_required
def standings(request):
    current_week = Game.objects.latest('game_date').week
    players = {}
    for p in Pick.objects.filter(player__league=request.player.league, week__lte=current_week):
        d = players.setdefault(p.player, {'winners': 0, 'losers': 0, 'total': 0})
        if p.winner_correct:
            d['winners'] += 1
            d['total'] += 1
        if p.loser_correct:
            d['losers'] += 1
            d['total'] += 1
    return render(request, 'standings.html', {
        'player': request.player,
        'standings': sorted(players.items(), key=lambda d: d[1]['total'], reverse=True),
    })

@player_required
def profile(request):
    if request.method == 'POST':
        request.player.name = request.POST.get('name', '').strip()
        request.player.send_reminders = request.POST.get('send_reminders', '') == '1'
        request.player.save()
        return redirect('pick')
    return render(request, 'profile.html', {
        'player': request.player,
    })
