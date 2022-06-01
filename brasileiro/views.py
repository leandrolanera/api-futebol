from django.shortcuts import render, redirect
from django.http import HttpResponse
from brasileiro.models import Estadio, Time
from brasileiro.importacao import buscaJogos

def importacao(request):
    if request.method == 'GET':
        dfJogos = buscaJogos()
        importaEstadios(dfJogos)        
        importaTimes(dfJogos)        

    return HttpResponse('Estadios/Times importados')

def importaEstadios(dataFrame):
    dfEstadios = dataFrame.loc[:,["Estadio","Cidade", "UF"]].drop_duplicates()
    for index, row in dfEstadios.iterrows():        
        estadioRow = Estadio(  
                        nome=row['Estadio'], 
                        nomeCompleto=row['Estadio'], 
                        cidade=row['Cidade'], 
                        estado=row['UF'])
        estadioRow.save()

def importaTimes(dataFrame):
    dfEstadios = dataFrame.loc[:,["Mandante", "Estadio"]].drop_duplicates()
    for index, row in dfEstadios.iterrows():        
        timeRow = Time( nome=row['Mandante'], 
                        nomeCompleto=row['Mandante'], 
                        estado=row['ufMandante'],
                        estadio=row['Estadio'])
        timeRow.save()