import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import A4
from .models import Jugador, ResumenEquipo, Liga, Categoria, Grupo

def resumen_equipos(request):
    resumenes = ResumenEquipo.objects.all()
    today = datetime.today()
    filename = 'resumen_equipos_' + today.strftime('%Y-%m-%d')
    
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=A4)
    
    p.setFont("Helvetica", 15, leading=None)
    p.setFillColorRGB(0.29296875,0.453125,0.609375)
    
    p.drawString(60, 810, "Resumen de Equipos")
    p.setFont("Helvetica", 10, leading=None)
    
    p.drawString(60, 795, "Liga  "+Liga.objects.get(id=1).nombre)
    p.drawString(300, 795, "Fundada en "+str(Liga.objects.get(id=1).anno))
    p.drawString(60, 785, "Estado actual de Campeonato - Fecha "+today.strftime('%d/%m/%Y'))
    p.drawString(60, 775, Categoria.objects.get(id=1).nombre)
    p.drawString(60, 765, Grupo.objects.get(id=1).nombre)
    
    p.setFillColor("red")
    p.drawString(60, 750, "Equipo")
    p.drawString(300, 750, "JJ")
    p.drawString(320, 750, "JG")
    p.drawString(340, 750, "JP")
    p.drawString(360, 750, "JE")
    p.drawString(380, 750, "PCT")
    
    p.setFillColor("black")
    positionY = 735
    
    for resumen in resumenes:
        p.drawString(60, positionY, resumen.equipo.equipo)
        p.drawString(300, positionY, str(resumen.jugados))
        p.drawString(320, positionY, str(resumen.ganados))
        p.drawString(340, positionY, str(resumen.perdidos))
        p.drawString(360, positionY, str(resumen.empatados))
        p.drawString(380, positionY, str(resumen.pct))
        positionY -= 10
    
    p.setFont("Helvetica", 13, leading=None)
    
    p.drawString(200, 150, "COMPILADOR OFICIAL: "+Liga.objects.get(id=1).responsable)
    
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename+".pdf")