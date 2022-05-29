from django.contrib import admin
from brasileiro.models import Estadio, Time, Jogador, Partida, Partida_Stats

class Estadios(admin.ModelAdmin):
    list_display = ('nome', 'nomeCompleto', 'estado', 'cidade', 'capacidade')
    list_display_links = ('nome',)
    search_fields = ('nome',)
    list_per_page = 10

admin.site.register(Estadio, Estadios)

class Times(admin.ModelAdmin):
    list_display = ('nome', 'nomeCompleto', 'estado', 'cidade', 'estadioPrincipal')
    list_display_links = ('nome',)
    list_per_page = 10

admin.site.register(Time, Times)

class Jogadores(admin.ModelAdmin):
    list_display = ('nome', 'nomeCompleto', 'time', 'numero')
    list_display_links = ('nome',)
    list_per_page = 10

admin.site.register(Jogador, Jogadores)

class Partidas(admin.ModelAdmin):
    list_display = ('numeroRodada', 'descricao', 'estadio', 'datahora', 'mandante', 'visitante')
    list_display_links = ('descricao',)
    list_per_page = 10

admin.site.register(Partida, Partidas)

class Partidas_Stats(admin.ModelAdmin):
    list_display = ('partida', 'tipoStat', 'jogador', 'minuto')
    list_display_links = ('partida',)
    list_per_page = 10

admin.site.register(Partida_Stats, Partidas_Stats)