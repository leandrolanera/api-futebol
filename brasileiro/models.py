from django.db import models

class Estadio(models.Model):
    nome = models.CharField(max_length=50)
    nomeCompleto = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    capacidade = models.IntegerField(null=True)

    def __str__(self):
        return "%s (%s)" % (self.nome)

class Time(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    nomeCompleto = models.CharField(max_length=200, null=True)
    apelido = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    estadioPrincipal = models.ForeignKey(Estadio, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.nome)

class Jogador(models.Model):
    nome = models.CharField(max_length=50)
    nomeCompleto = models.CharField(max_length=200, null=True)
    dtnasc = models.DateField(null=True) 
    numero = models.IntegerField()
    time = models.ForeignKey(Time, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (self.nome, self.time)

class Partida(models.Model):
    codCBF = models.IntegerField()
    descricao = models.CharField(max_length=100)
    datahora = models.DateTimeField()
    numeroRodada = models.IntegerField()
    estadio = models.ForeignKey(Estadio, on_delete=models.CASCADE)
    mandante = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='mandante_partida_set')
    visitante = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='visitante_partida_set')

    def __str__(self):
        return "Rodada: %s - %s" % (self.num_rodada, self.descricao)

class Partida_Stats(models.Model):
    TIPOSTAT = (
        ('G', 'Gol'),
        ('A', 'Assistência'),
        ('D', 'Advertência (Cartão Amarelo)'),
        ('E', 'Expulsão (Cartão Vermelho)')
    )
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE) 
    tipoStat = models.CharField(max_length=1, choices=TIPOSTAT, blank=False, null=False, default='G')
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    minuto = models.CharField(max_length=4)

    def __str__(self):
        return "%s %s" % (self.partida)        