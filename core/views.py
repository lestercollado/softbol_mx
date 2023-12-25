import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import A4
from .models import Jugador, ResumenEquipo, Liga, Categoria, Bateo, Campeonato, Pitcheo
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ReporteEstadoActualForm, BateoGeneralForm
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet

def index(request):
    form = ReporteEstadoActualForm()
    form_bateo = BateoGeneralForm()
    return render(request, 'core/index.html', {"form": form, "form_bateo": form_bateo})

def reporte_estado_actual(request):
    print(request.POST)
    liga = request.POST['liga']
    campeonato = request.POST['campeonato']
    categoria = request.POST['categoria']
    
    resumenes = ResumenEquipo.objects.filter(categoria = categoria)
    
    print(len(resumenes))
    
    if len(resumenes) > 0:    
        today = datetime.today()
        filename = 'resumen_equipos_' + today.strftime('%Y-%m-%d')
        
        buffer = io.BytesIO()
        
        width,height=A4 #595 x 842 pixels
        p = canvas.Canvas(buffer, pagesize=A4)
               
        stylesheet=getSampleStyleSheet()
        # normalStyle = stylesheet['Normal']
        normalStyle = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=17,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        normalStyle_sub = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=12,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        parrafo = Paragraph("Liga "+Liga.objects.get(id=liga).nombre, normalStyle)
       
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-50)
        
        parrafo = Paragraph(Campeonato.objects.get(id=campeonato).nombre + " - " + Categoria.objects.get(id=categoria).nombre, normalStyle_sub)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-70)
        
        parrafo = Paragraph("Estado Actual del Campeonato", normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-100)
        
        parrafo = Paragraph(today.strftime('%d/%m/%Y'), normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-150,height-100)
        
        p.setFillColor("red")
        p.drawString(40, height-130, "No.")
        p.drawString(90, height-130, "Equipo")
        p.drawString(330, height-130, "JJ")
        p.drawString(350, height-130, "JG")
        p.drawString(370, height-130, "JP")
        p.drawString(390, height-130, "JE")
        p.drawString(410, height-130, "PCT")
        
        p.setFillColor("black")
        positionY = height-145
        
        index = 1
        for resumen in resumenes:
            p.drawString(40, positionY, str(index))
            p.drawString(90, positionY, resumen.equipo.equipo)
            p.drawString(330, positionY, str(resumen.jugados))
            p.drawString(350, positionY, str(resumen.ganados))
            p.drawString(370, positionY, str(resumen.perdidos))
            p.drawString(390, positionY, str(resumen.empatados))
            if resumen.ganados != 0 or resumen.perdidos != 0:
                pct = resumen.ganados / (resumen.ganados+resumen.perdidos)
            else:
                pct = 0
            p.drawString(410, positionY, str(pct)+"%")
            positionY -= 12
            index += 1
        
        p.setFont("Helvetica", 13, leading=None)
        
        p.drawString(200, 150, "COMPILADOR OFICIAL: "+Liga.objects.get(id=liga).responsable)
        
        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename+".pdf")
    else:
        mensaje = "No es posible generar el reporte. No hay equipos según su selección."
        form = ReporteEstadoActualForm()
        return render(request, 'core/index.html', {"form": form, "mensaje": mensaje})
    
def bateo_general(request):
    print(request.POST)
    liga = request.POST['liga']
    campeonato = request.POST['campeonato']
    categoria = request.POST['categoria']
    veces = request.POST['veces']
    
    bateos = Bateo.objects.filter(categoria = categoria)[:30]         
        
    if len(bateos) > 0:    
        today = datetime.today()
        filename = 'bateo_general_' + today.strftime('%Y-%m-%d')
        
        buffer = io.BytesIO()
        
        width,height=A4 #595 x 842 pixels
        p = canvas.Canvas(buffer, pagesize=A4)
               
        stylesheet=getSampleStyleSheet()
        # normalStyle = stylesheet['Normal']
        normalStyle = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=17,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        normalStyle_sub = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=12,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        parrafo = Paragraph("Liga "+Liga.objects.get(id=liga).nombre, normalStyle)
       
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-50)
        
        parrafo = Paragraph(Campeonato.objects.get(id=campeonato).nombre + " - " + Categoria.objects.get(id=categoria).nombre, normalStyle_sub)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-70)
        
        parrafo = Paragraph("Bateo General", normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-100)
        
        parrafo = Paragraph(today.strftime('%d/%m/%Y'), normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-150,height-100)
        
        parrafo = Paragraph("Veces Legales " + str(veces), normalStyle_sub)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-120)
        
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(10, height-130, "Nombre del jugador")
        p.drawString(160, height-130, "Equipo")
        p.drawString(300, height-130, "V")
        p.drawString(320, height-130, "C")
        p.drawString(340, height-130, "H")
        p.drawString(360, height-130, "H2")
        p.drawString(385, height-130, "H3")
        p.drawString(410, height-130, "HR")
        p.drawString(435, height-130, "CP")
        p.drawString(460, height-130, "BB")
        p.drawString(485, height-130, "BR")
        p.drawString(510, height-130, "K")
        p.drawString(535, height-130, "PCT")
        
        p.setFillColor("black")
        positionY = height-145
        
        for bateo in bateos:
            p.drawString(10, positionY, bateo.jugador_id.nombre)
            p.drawString(160, positionY, bateo.equipo.equipo)
            p.drawString(300, positionY, str(bateo.veces_bate))
            p.drawString(320, positionY, str(bateo.carrera))
            p.drawString(340, positionY, str(bateo.hits))
            p.drawString(360, positionY, str(bateo.doble))
            p.drawString(385, positionY, str(bateo.triple))
            p.drawString(410, positionY, str(bateo.home_run))
            p.drawString(435, positionY, "-")
            p.drawString(460, positionY, str(bateo.base_bola))
            p.drawString(485, positionY, str(bateo.base_robada))
            p.drawString(510, positionY, str(bateo.ponche))
            if bateo.veces_bate != 0:
                pct = round(bateo.hits / bateo.veces_bate,3)
            else:
                pct = 0
            p.drawString(535, positionY, str(pct))
            positionY -= 12
        
        p.setFont("Helvetica", 13, leading=None)
        
        p.drawString(200, 150, "COMPILADOR OFICIAL: "+Liga.objects.get(id=liga).responsable)
        
        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename+".pdf")
    else:
        mensaje = "No es posible generar el reporte. No se han registrados bateos según su selección."
        form = ReporteEstadoActualForm()
        return render(request, 'core/index.html', {"form": form, "mensaje": mensaje})
    
def bateo_dpto(request):
    liga = request.POST['liga']
    campeonato = request.POST['campeonato']
    categoria = request.POST['categoria']
    
    bateos_hits = Bateo.objects.filter(categoria = categoria).order_by('-hits')[:5]    
    bateos_dobles = Bateo.objects.filter(categoria = categoria).order_by('-doble')[:5]    
    bateos_triples = Bateo.objects.filter(categoria = categoria).order_by('-triple')[:5]    
    bateos_home_runs = Bateo.objects.filter(categoria = categoria).order_by('-home_run')[:5]    
    bateos_carreras = Bateo.objects.filter(categoria = categoria).order_by('-carrera')[:5]    
    bateos_robos = Bateo.objects.filter(categoria = categoria).order_by('-base_robada')[:5]    
    
    bateadores = Jugador.objects.filter(tipo = "Bateador", categoria = categoria)
    
    aux_hits = {}
    aux_dobles = {}
    aux_triples = {}
    aux_homeruns = {}
    aux_producidas = {}
    aux_robadas = {}
    hits = 0
    dobles = 0
    triples = 0
    homeruns = 0
    producidas = 0
    robadas = 0
    for bateador in bateadores:
        bateos = Bateo.objects.filter(jugador_id = bateador)
        for bat in bateos:
            hits += bat.hits
            dobles += bat.doble
            triples += bat.triple
            homeruns += bat.home_run
            producidas += bat.carrera
            robadas += bat.base_robada
        aux_hits[bateador.id] = hits
        aux_dobles[bateador.id] = dobles
        aux_triples[bateador.id] = triples
        aux_homeruns[bateador.id] = homeruns
        aux_producidas[bateador.id] = producidas
        aux_robadas[bateador.id] = robadas
        hits = 0
        dobles = 0
        triples = 0
        homeruns = 0
        producidas = 0
        robadas = 0
    
    aux_hits = {k:v for k,v in sorted(aux_hits.items(), key=lambda item: item[1], reverse=True)}
    aux_dobles = {k:v for k,v in sorted(aux_dobles.items(), key=lambda item: item[1], reverse=True)}
    aux_triples = {k:v for k,v in sorted(aux_triples.items(), key=lambda item: item[1], reverse=True)}
    aux_homeruns = {k:v for k,v in sorted(aux_homeruns.items(), key=lambda item: item[1], reverse=True)}
    aux_producidas = {k:v for k,v in sorted(aux_producidas.items(), key=lambda item: item[1], reverse=True)}
    aux_robadas = {k:v for k,v in sorted(aux_robadas.items(), key=lambda item: item[1], reverse=True)}
    
    total = len(bateos_hits) + len(bateos_dobles) + len(bateos_triples) + len(bateos_home_runs) + len(bateos_carreras) + len(bateos_robos)
        
    if total > 0:    
        today = datetime.today()
        filename = 'bateo_por_departamentos_' + today.strftime('%Y-%m-%d')
        
        buffer = io.BytesIO()
        
        width,height=A4 #595 x 842 pixels
        p = canvas.Canvas(buffer, pagesize=A4)
               
        stylesheet=getSampleStyleSheet()
        # normalStyle = stylesheet['Normal']
        normalStyle = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=17,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        normalStyle_sub = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=12,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        parrafo = Paragraph("Liga "+Liga.objects.get(id=liga).nombre, normalStyle)
       
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-50)
        
        parrafo = Paragraph(Campeonato.objects.get(id=campeonato).nombre + " - " + Categoria.objects.get(id=categoria).nombre, normalStyle_sub)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-70)
        
        parrafo = Paragraph("Bateo General", normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-100)
        
        parrafo = Paragraph(today.strftime('%d/%m/%Y'), normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-150,height-100)
        
        # Hits
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, height-130, "Nombre del jugador")
        p.drawString(260, height-130, "Equipo")
        p.drawString(400, height-130, "Hit")        
        p.setFillColor("black")
        positionY = height-145  
        for x in aux_hits:
            if aux_hits[x] > 0:
                p.drawString(110, positionY, Bateo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Bateo.objects.get(id=x).equipo.equipo)
                p.drawString(400, positionY, str(aux_hits[x]))
                positionY -= 12
            
        # Dobles
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, positionY-40, "Nombre del jugador")
        p.drawString(260, positionY-40, "Equipo")
        p.drawString(400, positionY-40, "Dobles")        
        p.setFillColor("black")
        positionY -= 55
        for x in aux_dobles:
            if aux_dobles[x] > 0:
                p.drawString(110, positionY, Bateo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Bateo.objects.get(id=x).equipo.equipo)
                p.drawString(415, positionY, str(aux_dobles[x]))
                positionY -= 12
            
        # Triples
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, positionY-40, "Nombre del jugador")
        p.drawString(260, positionY-40, "Equipo")
        p.drawString(400, positionY-40, "Triples")        
        p.setFillColor("black")
        positionY -= 55
        for x in aux_triples:
            if aux_triples[x] > 0:
                p.drawString(110, positionY, Bateo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Bateo.objects.get(id=x).equipo.equipo)
                p.drawString(415, positionY, str(aux_triples[x]))
                positionY -= 12
            
        # HR
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, positionY-40, "Nombre del jugador")
        p.drawString(260, positionY-40, "Equipo")
        p.drawString(400, positionY-40, "Home Runs")        
        p.setFillColor("black")
        positionY -= 55
        for x in aux_homeruns:
            if aux_homeruns[x] > 0:
                p.drawString(110, positionY, Bateo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Bateo.objects.get(id=x).equipo.equipo)
                p.drawString(425, positionY, str(aux_homeruns[x]))
                positionY -= 12
            
        # Carreras
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, positionY-40, "Nombre del jugador")
        p.drawString(260, positionY-40, "Equipo")
        p.drawString(400, positionY-40, "Producidas")        
        p.setFillColor("black")
        positionY -= 55
        for x in aux_producidas:
            if aux_producidas[x] > 0:
                p.drawString(110, positionY, Bateo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Bateo.objects.get(id=x).equipo.equipo)
                p.drawString(420, positionY, str(aux_producidas[x]))
                positionY -= 12
            
        # Robo
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, positionY-40, "Nombre del jugador")
        p.drawString(260, positionY-40, "Equipo")
        p.drawString(400, positionY-40, "Robo de Bases")        
        p.setFillColor("black")
        positionY -= 55
        for x in aux_robadas:
            if aux_robadas[x] > 0:
                p.drawString(110, positionY, Bateo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Bateo.objects.get(id=x).equipo.equipo)
                p.drawString(430, positionY, str(aux_robadas[x]))
                positionY -= 12
        
        p.setFont("Helvetica", 13, leading=None)        
        p.drawString(200, 150, "COMPILADOR OFICIAL: "+Liga.objects.get(id=liga).responsable)        
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename+".pdf")
    else:
        mensaje = "No es posible generar el reporte. No se han registrados bateos según su selección."
        form = ReporteEstadoActualForm()
        return render(request, 'core/index.html', {"form": form, "mensaje": mensaje})
    
def pitcheo_ganados_perdidos(request):
    liga = request.POST['liga']
    campeonato = request.POST['campeonato']
    categoria = request.POST['categoria']
    
    ganados = Pitcheo.objects.filter(categoria = categoria)
    
    pitchers = Jugador.objects.filter(tipo = "Pitcher", categoria = categoria)
    
    aux_ganados = {}
    ganados_count = 0
    perdido_count = 0
    sindecision_count = 0
    for pitcher in pitchers:
        pitcheos = Pitcheo.objects.filter(jugador_id = pitcher)
        for pit in pitcheos:
            if pit.ganado:
                ganados_count += 1
            if pit.perdido:
                perdido_count += 1
            if pit.sin_decision:
                sindecision_count += 1
        aux_ganados[pit.id] = [ ganados_count, perdido_count, sindecision_count ]
        ganados_count = 0
        perdido_count = 0
        sindecision_count = 0
    
    aux_ganados = {k:v for k,v in sorted(aux_ganados.items(), key=lambda item: item[1][0], reverse=True)}
    
    
    if len(ganados) > 0:    
        today = datetime.today()
        filename = 'pitcheo_' + today.strftime('%Y-%m-%d')
        
        buffer = io.BytesIO()
        
        width,height=A4 #595 x 842 pixels
        p = canvas.Canvas(buffer, pagesize=A4)
               
        stylesheet=getSampleStyleSheet()
        normalStyle = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=17,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        normalStyle_sub = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=12,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        parrafo = Paragraph("Liga "+Liga.objects.get(id=liga).nombre, normalStyle)
       
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-50)
        
        parrafo = Paragraph(Campeonato.objects.get(id=campeonato).nombre + " - " + Categoria.objects.get(id=categoria).nombre, normalStyle_sub)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-70)
        
        parrafo = Paragraph("Ganados y Perdidos", normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-100)
        
        parrafo = Paragraph(today.strftime('%d/%m/%Y'), normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-150,height-100)
        
        # Hits
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, height-130, "Nombre del jugador")
        p.drawString(260, height-130, "Equipo")
        p.drawString(400, height-130, "JJ")     
        p.drawString(420, height-130, "JG")        
        p.drawString(440, height-130, "JP")        
        p.drawString(460, height-130, "JS")        
        p.drawString(480, height-130, "PCT")        
        p.setFillColor("black")
        positionY = height-145  
        for x in aux_ganados:
            if aux_ganados[x][0] > 0:
                jugados = aux_ganados[x][0]+aux_ganados[x][1]+aux_ganados[x][2]
                p.drawString(110, positionY, Pitcheo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Pitcheo.objects.get(id=x).equipo.equipo)
                p.drawString(400, positionY, str(jugados))
                p.drawString(420, positionY, str(aux_ganados[x][0]))
                p.drawString(440, positionY, str(aux_ganados[x][1]))
                p.drawString(460, positionY, str(aux_ganados[x][2]))
                p.drawString(480, positionY, str(round(jugados / (aux_ganados[x][0] + aux_ganados[x][1]),3)))
                positionY -= 12
        
        p.setFont("Helvetica", 13, leading=None)        
        p.drawString(200, 150, "COMPILADOR OFICIAL: "+Liga.objects.get(id=liga).responsable)        
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename+".pdf")
    else:
        mensaje = "No es posible generar el reporte. No se han registrados bateos según su selección."
        form = ReporteEstadoActualForm()
        return render(request, 'core/index.html', {"form": form, "mensaje": mensaje})
    
def pitcheo_carreras_limpias(request):
    liga = request.POST['liga']
    campeonato = request.POST['campeonato']
    categoria = request.POST['categoria']
    
    ganados = Pitcheo.objects.filter(categoria = categoria)
    
    pitchers = Jugador.objects.filter(tipo = "Pitcher", categoria = categoria)
    
    aux_ganados = {}
    ganados_count = 0
    perdido_count = 0
    sindecision_count = 0
    for pitcher in pitchers:
        pitcheos = Pitcheo.objects.filter(jugador_id = pitcher)
        for pit in pitcheos:
            ganados_count += pit.ip
            perdido_count += pit.carreras
            sindecision_count += pit.carr_limpias
        aux_ganados[pit.id] = [ ganados_count, perdido_count, sindecision_count ]
        ganados_count = 0
        perdido_count = 0
        sindecision_count = 0
    
    aux_ganados = {k:v for k,v in sorted(aux_ganados.items(), key=lambda item: item[1][0], reverse=True)}
        
    if len(ganados) > 0:    
        today = datetime.today()
        filename = 'pitcheo_' + today.strftime('%Y-%m-%d')
        
        buffer = io.BytesIO()
        
        width,height=A4 #595 x 842 pixels
        p = canvas.Canvas(buffer, pagesize=A4)
               
        stylesheet=getSampleStyleSheet()
        normalStyle = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=17,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        normalStyle_sub = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=12,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        parrafo = Paragraph("Liga "+Liga.objects.get(id=liga).nombre, normalStyle)
       
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-50)
        
        parrafo = Paragraph(Campeonato.objects.get(id=campeonato).nombre + " - " + Categoria.objects.get(id=categoria).nombre, normalStyle_sub)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-70)
        
        parrafo = Paragraph("Carreras limpias con 12 IP", normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-100)
        
        parrafo = Paragraph(today.strftime('%d/%m/%Y'), normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-150,height-100)
        
        # Hits
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, height-130, "Nombre del jugador")
        p.drawString(260, height-130, "Equipo")
        p.drawString(400, height-130, "IP")     
        p.drawString(420, height-130, "C")        
        p.drawString(440, height-130, "CL")        
        p.drawString(460, height-130, "PCL")       
        p.setFillColor("black")
        positionY = height-145  
        for x in aux_ganados:
            if aux_ganados[x][0] > 0:
                p.drawString(110, positionY, Pitcheo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Pitcheo.objects.get(id=x).equipo.equipo)
                p.drawString(400, positionY, str(aux_ganados[x][0]))
                p.drawString(420, positionY, str(aux_ganados[x][1]))
                p.drawString(440, positionY, str(aux_ganados[x][2]))
                p.drawString(460, positionY, str(aux_ganados[x][2]*7/aux_ganados[x][0]))
                positionY -= 12
        
        p.setFont("Helvetica", 13, leading=None)        
        p.drawString(200, 150, "COMPILADOR OFICIAL: "+Liga.objects.get(id=liga).responsable)        
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename+".pdf")
    else:
        mensaje = "No es posible generar el reporte. No se han registrados bateos según su selección."
        form = ReporteEstadoActualForm()
        return render(request, 'core/index.html', {"form": form, "mensaje": mensaje})
    
def pitcheo_ponches(request):
    liga = request.POST['liga']
    campeonato = request.POST['campeonato']
    categoria = request.POST['categoria']
    
    ganados = Pitcheo.objects.filter(categoria = categoria)
    
    pitchers = Jugador.objects.filter(tipo = "Pitcher", categoria = categoria)
    
    aux_ganados = {}
    ganados_count = 0
    for pitcher in pitchers:
        pitcheos = Pitcheo.objects.filter(jugador_id = pitcher)
        for pit in pitcheos:
            ganados_count += pit.ponche
        aux_ganados[pit.id] = ganados_count
        ganados_count = 0
        
    aux_ganados = {k:v for k,v in sorted(aux_ganados.items(), key=lambda item: item[1], reverse=True)}
        
    if len(ganados) > 0:    
        today = datetime.today()
        filename = 'pitcheo_' + today.strftime('%Y-%m-%d')
        
        buffer = io.BytesIO()
        
        width,height=A4 #595 x 842 pixels
        p = canvas.Canvas(buffer, pagesize=A4)
               
        stylesheet=getSampleStyleSheet()
        normalStyle = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=17,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        normalStyle_sub = ParagraphStyle('My Para style',
            fontName='Helvetica',
            backColor=None,
            fontSize=12,
            borderColor='#FFFF00',
            borderWidth=0,
            borderPadding=None,
            leading=20,
            alignment=0
        )
        parrafo = Paragraph("Liga "+Liga.objects.get(id=liga).nombre, normalStyle)
       
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-50)
        
        parrafo = Paragraph(Campeonato.objects.get(id=campeonato).nombre + " - " + Categoria.objects.get(id=categoria).nombre, normalStyle_sub)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-70)
        
        parrafo = Paragraph("Ponches", normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-400,height-100)
        
        parrafo = Paragraph(today.strftime('%d/%m/%Y'), normalStyle)
        parrafo.wrapOn(p,250,350)
        parrafo.drawOn(p,width-150,height-100)
        
        # Hits
        p.setFont("Helvetica", 10, leading=None)
        p.setFillColor("red")
        p.drawString(110, height-130, "Nombre del jugador")
        p.drawString(260, height-130, "Equipo")
        p.drawString(400, height-130, "Ponches")    
        p.setFillColor("black")
        positionY = height-145  
        for x in aux_ganados:
            if aux_ganados[x] > 0:
                p.drawString(110, positionY, Pitcheo.objects.get(id=x).jugador_id.nombre)
                p.drawString(260, positionY, Pitcheo.objects.get(id=x).equipo.equipo)
                p.drawString(415, positionY, str(aux_ganados[x]))
                positionY -= 12
        
        p.setFont("Helvetica", 13, leading=None)        
        p.drawString(200, 150, "COMPILADOR OFICIAL: "+Liga.objects.get(id=liga).responsable)        
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename+".pdf")
    else:
        mensaje = "No es posible generar el reporte. No se han registrados bateos según su selección."
        form = ReporteEstadoActualForm()
        return render(request, 'core/index.html', {"form": form, "mensaje": mensaje})