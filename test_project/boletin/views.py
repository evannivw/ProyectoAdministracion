import textwrap
import math
from django.http import HttpResponse
from django.shortcuts import render
from django.http import QueryDict

import random
import numpy as np
import json

def EcuacionCurvasDeAprendizaje(a,x,porcentaje):
    b = math.log(porcentaje,2)/math.log(2,2)
    y = float('%.3f'%(a*(x**b)))
    return y

def SimulacionMontecarlo(Vmin,Vmax):
   # Vmin = [10000 15000 7500 4800 20000 5000]
    #Vmax = [20000 15000 12000 6200 25000 7000]
    # print("length")
    l = int(len(Vmin))
    Tmin = sum(Vmin)
    Tmax = sum(Vmax)
    btemp = np.std([Tmin, Tmax])
    b = int(btemp)
    e = ((Tmin + Tmax) / 2) / 50
    n = (3 * b / e) ** 2
    N = int(round(n, 0))
    temp = 0
    iteraciones = N + 1
    puntosMonteCarlo1 = []
    var1 = 0
    for i in range(iteraciones):
        puntosMonteCarlo1.append(temp)
        var1 += temp
        temp = 0
        for j in range(l):
            var = random.random() * (Vmax[j] - Vmin[j]) + Vmin[j]
            temp = temp + var
    costo_esperado = (int(var1) / float(iteraciones))
    #costoEsperado = costo_esperado
    print(costo_esperado)
    return puntosMonteCarlo1,costo_esperado

def Run(request):
    puntosMonteCarlo = []
    puntosCurvaDeAprendizaje = []
    puntosCurvaDeAprendizajeAcumuladas = []
    pestañaMontecarlo = "active"
    pestañaCurvas = ""
    Aprendizaje = ""
    PrimeraIteracion = ""
    costoEsperado = 0
    Vmin = []
    Vmax = []
    if(request.method == 'POST'):

        Aprendizaje = request.POST.get('aprendizaje')
        PrimeraIteracion = request.POST.get('primera_unidad')
        Curvas = request.POST.get('Curvas')
        MonteCarlo = request.POST.get('MonteCarlo')
        if(MonteCarlo):
            print("Entro en montecarlo")
            Vmin = request.POST.get('Vmin').split()
            Vmax = request.POST.get('Vmax').split()
            pestañaCurvas = ""
            pestañaMontecarlo = "active"
            Vmin2 = list(map(int, Vmin))
            Vmax2 = list(map(int, Vmax))
            for i in range(len(Vmax)):
               if (Vmax[i] == ''):
                  return HttpResponse("")
                    #Vmax[i] = "0"
            puntosMonteCarlo,costoEsperado = SimulacionMontecarlo(Vmin2,Vmax2)
        elif(Aprendizaje != None and PrimeraIteracion != None and Curvas != None):
            print("Entro en curvas")
            pestañaCurvas = "active"
            pestañaMontecarlo = ""
            aprendizaje = float(Aprendizaje) #0.6
            tiempoPrimeraIteracion = float(PrimeraIteracion) #7.589
            puntosAcumulados = 0
            for i in range(1,20,1):
                puntos = EcuacionCurvasDeAprendizaje(tiempoPrimeraIteracion,i,aprendizaje)
                puntosAcumulados += puntos
                puntosCurvaDeAprendizaje.append(float('%.3f'%(puntos)))
                puntosCurvaDeAprendizajeAcumuladas.append(float('%.3f'%(puntosAcumulados)))
    context = {
        'puntosMonteCarlo': puntosMonteCarlo,
        'curvaAprendizaje':puntosCurvaDeAprendizaje,
        'curvaApredizajeAcumulada':puntosCurvaDeAprendizajeAcumuladas,
        'aprendizaje': Aprendizaje,
        'primera_unidad':PrimeraIteracion,
        'pestañaMonteCarlo':pestañaMontecarlo,
        'pestañaCurvas': pestañaCurvas,
        'costo': costoEsperado,
        'vmin':request.POST.get('Vmin'),
        'vmax':request.POST.get('Vmax'),

    }
    return render(request, 'inicio.html', context)

    #return HttpResponse(response_text)
