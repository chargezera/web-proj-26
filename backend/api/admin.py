from django.contrib import admin

from .models import Match, MatchMap, Player, Post, Team, Tournament


admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(MatchMap)
admin.site.register(Post)
