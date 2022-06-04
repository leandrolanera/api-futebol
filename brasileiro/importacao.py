from tracemalloc import stop
from django.shortcuts import render
##Imports necessários para raspar os dados da página
import requests
from bs4 import BeautifulSoup
##Import necessário para criação dos dataframes para análise
import pandas as pd
##Import necessário para criação de gráficos
import matplotlib.pyplot as plt
##Import necessário para trabalhar com data e hora.
import datetime as dtm
from datetime import date as dt
##Import necessário para tratar acentuação
from unicodedata import normalize as nm


#Remover acentos das strings
def remove_acentos(str):
  str_sem_acentos = nm('NFKD', str).encode('ASCII', 'ignore').decode('ASCII')
  return str_sem_acentos

#Padronizar mês da data do Jogo.
def retMes(mes):
    if mes == 'Janeiro':
        return '01'
    elif mes == 'Fevereiro':
        return '02'
    elif mes == 'Março':
        return '03'
    elif mes == 'Abril':
        return '04'
    elif mes == 'Maio':
        return '05'
    elif mes == 'Junho':
        return '06'
    elif mes == 'Julho':
        return '07'
    elif mes == 'Agosto':
        return '08'
    elif mes == 'Setembro':
        return '09'
    elif mes == 'Outubro':
        return '10'
    elif mes == 'Novembro':
        return '11'
    elif mes == 'Dezembro':
        return '12'

def trataNomeTime(nome_origem, uf_origem):
    if (uf_origem == 'PR' and (nome_origem == 'Athletico Paranaense' or nome_origem == 'Atlético Paranaense' or nome_origem == 'Atletico' or nome_origem == 'Atlético')):
      nome = 'Athletico Paranaense'
    elif (uf_origem != 'PR' and (nome_origem == 'Atlético' or nome_origem == 'Atletico')):
      nome = 'Atlético-'+uf_origem
    elif (nome_origem == 'America Fc' or nome_origem == 'América Fc' or nome_origem == 'America' or nome_origem == 'América'):
      nome = 'América-'+uf_origem
    elif (nome_origem == 'Botafogo'):
      nome = 'Botafogo-'+uf_origem
    elif (nome_origem == 'C.r.b.' or nome_origem == 'Crb'):
      nome = 'CRB-'+uf_origem
    elif (nome_origem == 'A.b.c.' or nome_origem == 'Abc'):
      nome = 'ABC-'+uf_origem
    elif (nome_origem == 'A.s.a.'):
      nome = 'ASA-'+uf_origem
    elif (nome_origem == 'Csa'):
      nome = 'CSA-'+uf_origem
    else:
      nome = nome_origem
      
    return remove_acentos(nome)

#Busca dados iniciais do jogo
#numero, rodada, turno
def getDadosInicJogo(soup):
    dadosInicJogo = soup.find(class_='color-white block text-1')
    
    ##Tratando a requisição que contém o número do jogo
    num_jogo = int(dadosInicJogo.get_text().strip().replace('Jogo: ','').replace('<font color="red">(W.O. Duplo)</font>', ''))

    '''
        1) A cada rodada ocorrem 10 jogos, sendo assim quando o número do jogo dividido por 10 tiver 0 como resto, a rodada será o quociente.
        Ex: 200 / 10 = 20 - sendo assim a rodada a que pertence o jodo de nº 200 é a 20
        2) Caso o **resto da divisão** do número do jogo for **diferente de 0** então a rodada corresponderá ao quociente (inteiro) + 1
        Ex: 201 / 10 = 20,1 - sendo assim a rodada será 21, pois o resto é 1 e o quociente inteiro é 20.
    '''
    if (num_jogo%10 == 0):
        rodada = int(int(num_jogo)/10)
    else:
        rodada = int((int(num_jogo)//10)+1)

    #Calcular o turno ao qual o jogo pertence usando if ternario
    turno = 1 if int(num_jogo) <= 190 else 2

    #numero do jogo, rodada e turno
    listaResult = [num_jogo, rodada, int(turno)]
    return listaResult

#Busca dados do local e data do jogo
## estadio, cidade uf, diasemana, data, hora
def getDadosLocalJogo(soup):

    dadosLocalJogo = soup.find_all(class_='text-2 p-r-20') 
    listaResult = []
    listaResult.append(remove_acentos(dadosLocalJogo[0].get_text().split(" - ")[0].strip()))
    listaResult.append(remove_acentos(dadosLocalJogo[0].get_text().split(" - ")[1].strip()))
    listaResult.append(remove_acentos(dadosLocalJogo[0].get_text().split(" - ")[2].strip()))
    listaResult.append(remove_acentos(dadosLocalJogo[1].get_text().split(",")[0].strip()))
    listaResult.append(remove_acentos(dadosLocalJogo[2].get_text().split(",")[0].strip()))

    data_origem = dadosLocalJogo[1].get_text().split(",")[1].strip()
    lstData = data_origem.split(" de ")                        ##Separar os elementos que compõe a data
    dia = lstData[0]                                           ##Extrai o dia da data
    mes = retMes(lstData[1])                                   ##Extrai o mês da data
    ano = lstData[2]                                           ##Extrai o ano da data
    data_origem = dt(int(ano), int(mes), int(dia)).isoformat()   
    listaResult.append(data_origem)   

    return listaResult

#Retorna o time, estado e gols
# mandante ou visitante
def getDadosTime(dados, deQuem):    
    index = 0 if deQuem == 'mandante' else 1

    nome_orig = dados[index].get_text().split("-")[0].strip()    
    uf_orig = dados[index].get_text().split("-")[1].strip()
        
    nome = trataNomeTime(nome_orig)
    dadosTime = [nome, uf_orig]
    return dadosTime

#Esta função retorna quantos gols o time mandante fez
def retGolMandante(captGols):
    if len(captGols)== 2:
        golmandante = captGols[0].get_text().strip()
    else:
        golmandante = 0
    return int(golmandante)

#Esta função retorna quantos gols o time visitante fez
def retGolVisitante(captGols):
    if len(captGols)== 2:
        golvisitante = captGols[1].get_text().strip()
    else:
        golvisitante = 0
    return int(golvisitante)

#Esta função retorna o total de gols do jogo
def totalGolsJogo(captGols):
    if len(captGols)== 2:
        golmandante = captGols[0].get_text().strip()
        golvisitante = captGols[1].get_text().strip()
        gols_jogo = int(golmandante) + int(golvisitante)
    else:
        gols_jogo = 0
    return int(gols_jogo)

##Esta função retorna uma lista que armazena quem venceu o jogo, qual o resultado do mandante e qual o resultado do visitante
def resultJogo(captGols):
    if len(captGols)== 2:
        gol_mandante = int(captGols[0].get_text().strip())
        gol_visitante = int(captGols[1].get_text().strip())        
        if (gol_mandante == gol_visitante):
            resultado = 'Empate'
            resultado_mandante = 'Empate'
            resultado_visitante = 'Empate'
        elif (gol_mandante > gol_visitante):
            resultado = 'Mandante'
            resultado_mandante = 'Vitoria'
            resultado_visitante = 'Derrota'
        else:
            resultado = 'Visitante'
            resultado_mandante = 'Derrota'
            resultado_visitante = 'Vitoria'
    else:
        resultado = 'WO Duplo'
        resultado_mandante = 'WO'
        resultado_visitante = 'WO'
    listaResult = [resultado, resultado_mandante, resultado_visitante]
    return listaResult

##Esta função retorna o placar do jogo (padronizado sempre do maior para o menor número de gols)
def placarJogo(golMandante, golVisitante):
    if (golMandante == -1):
        placar = 'W-O'
    elif (golMandante == golVisitante):
        placar = str(golMandante)+'-'+str(golVisitante)
    elif (golMandante > golVisitante):
        placar = str(golMandante)+'-'+str(golVisitante)
    else:
        placar = str(golVisitante)+'-'+str(golMandante)
    return placar

def listaGols(ano, serie, numJogo, time, golJog, MandVisi): # 0 - Mandante, 1 - Visitante
    lstFinalGols = []
    deQuem = ('Mandante' if MandVisi == 0 else 'Visitante')

    if len(golJog) == 0:
        return lstFinalGols
    else:
        lstGolJog = golJog[MandVisi].get_text().strip()  ##Captura lista dos gols feitos
        lstItemsGolJog = lstGolJog.replace('\n','').strip().replace('ºT)', '\n').strip().splitlines()
        for i in lstItemsGolJog:
            lstGol = i.split('\' (')
            for n in lstGol:
                lstJogador = lstGol[0].rsplit(" ", 1)[0].strip()  ##Extrai o jogador que fez o Gol
                lstMinuto = 0
                captMinuto = lstGol[0].rsplit(" ", 1)[1]    ##Extrai o Minuto em que o Gol foi feito
                if len(captMinuto) <= 2:
                    lstMinuto = int(captMinuto)
                else:
                    tmpNormal = captMinuto.split('+')[0]
                    tmpAcrescimo = captMinuto.split('+')[1]
                    lstMinuto = int(tmpNormal)+int(tmpAcrescimo)
                lstTempo = lstGol[1]
            lstGols = [ano, serie, numJogo, time, lstJogador, lstMinuto, lstTempo, deQuem]
            lstFinalGols.append(lstGols)
        return lstFinalGols

def buscaJogos():
    ##Lista para armazenar as séries que serão pesquisadas
    lstSerie = ['a']
    ##Variável para armazenar o início do link que será utilizado para extrair os dados.
    linkRaiz = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-'
    ##Lista para armazenar todos os jogos pesquisados.
    listaFinal = []

    for i in lstSerie:                ##Este loop foi criado, para varrer a lista a ser pesquisada (permite buscar a Série B).
        serie = i                     ##Esta variável será utilizada para compor o link do jogo.
        for j in range(2022, 2023):         ##Range com as temporadas a serem pesquisadas. A temporada inicial disponível é 201
            if (j == 0):
                break
            ano = j         #1,381          ##Esta variável será utilizada para compor o link do jogo.
            for nj in range (1, 5):  ##range de jogos a ser pesquisada. Não pode ser maior do que 380.
                linkJogo = linkRaiz+serie+'/'+str(ano)+'/'+str(nj)                 ##Link completo do jogo a ser capturado
                requisicao = requests.get(linkJogo)
                print(linkJogo)
                                
                soupJogo = BeautifulSoup(requisicao.content, 'html.parser')

                # dados iniciais do jogo
                dadosInicJogo = getDadosInicJogo(soupJogo) ;
                num_jogo = dadosInicJogo[0]
                num_rodada = dadosInicJogo[1]
                num_turno = dadosInicJogo[2]
                print(num_jogo, num_rodada, num_turno)
                
                # dados do local do jogo
                dadosLocalDtHrJogo = getDadosLocalJogo(soupJogo)  
                # estadio = dadosLocalDtHrJogo[0]                           
                # cidade = dadosLocalDtHrJogo[1]                            
                # uf = dadosLocalDtHrJogo[2]                                                                 
                # diasemana = dadosLocalDtHrJogo[3]                             
                # data = dadosLocalDtHrJogo[4]                                   
                # hora_jogo = dadosLocalDtHrJogo[5]                              
                print(dadosLocalDtHrJogo)

    #             dadosTimes = soup.find_all(class_='time-nome color-white')          
    #             mandante = getDadosTime(dadosTimes, 'mandante')[0]                  
    #             visitante = getDadosTime(dadosTimes, 'visitante')[0]                             
    #             ufMandante = getDadosTime(dadosTimes, 'mandante')[1]                           
    #             ufVisitante = getDadosTime(dadosTimes, 'visitante')[1]       
    #             print(mandante, visitante, ufMandante, ufVisitante)                  

    #             captGols = soup.find_all(class_='time-gols block')                 ##Variável que armazena os gols
    #             gol_mandante = retGolMandante(captGols)                            ##Gols Mandante
    #             gol_visitante = retGolVisitante(captGols)                          ##Gols Visitante
    #             gols_jogo = totalGolsJogo(captGols)                                ##Quantidade de Gols no Jogo

    #             ##Variável que indica quem foi o vencedor do jogo ou se houve empate
    #             resultado = resultJogo(captGols)[0]
    #             ##Variável que indica se o mandante venceu, empatou ou perdeu o jogo
    #             resultado_mandante = resultJogo(captGols)[1]
    #             ##Variável que indica se o visitante venceu, empatou ou perdeu o jogo
    #             resultado_visitante = resultJogo(captGols)[2]
    #             ##Placar do Jogo (padronizado sempre do maior para o menor número de gols)
    #             placar = placarJogo(gol_mandante, gol_visitante)
                            

    #             ##Este bloco visa capturar as informações sobre os gols: quem fez, quando fez, tempo que fez etc.
    #             golJog = soup.find_all(class_='hidden-sm hidden-md hidden-lg m-t-20') ##Lista de Jogadores e tempo dos Gols
                
    #             ##Captura informações sobre os Gosl do Mandante
    #             lstGolsM = listaGols(str(ano), serie.upper(), num_jogo, mandante, golJog, 0)
    #             ##Captura informações sobre os Gosl do Visitante
    #             lstGolsV = listaGols(str(ano), serie.upper(), num_jogo, visitante, golJog, 1)

    #             ##Lista para armazenar o jogo que está sendo pesquisado no momento
    #             lista = [str(ano), serie.upper(), num_jogo, num_rodada, num_turno, estadio
    #                     , cidade, uf
    #                     , data, diasemana, hora_jogo, mandante, ufMandante
    #                     , visitante, ufVisitante
    #                     , resultado, placar
    #                     , lstGolsM, lstGolsV
    #                     , linkJogo]

    #             ##Lista para armazenar todos os jogos pesquisados.
    #             listaFinal.append(lista)
    
    # df_Final = pd.DataFrame(listaFinal, columns = ['Temporada', 'Serie', 'NumJogo', 'Rodada', 'Turno', 'Estadio', 'Cidade', 'UF'
    #                                                 , 'Data', 'Dia da Semana', 'Hora', 'Mandante', 'ufMandante'
    #                                                 , 'Visitante', 'ufVisitante'
    #                                                 , 'Resultado',  'Placar'
    #                                                 , 'Gols Mandante', 'Gols Visitante'
    #                                                 , 'Link do Jogo'])
    
    return 0        

