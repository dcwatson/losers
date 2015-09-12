from django.shortcuts import redirect

def player_required(view_func):
    def _dec(request, *args, **kwargs):
        from .models import Player
        try:
            request.player = Player.objects.get(pk=request.session['player_id'])
        except:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _dec
