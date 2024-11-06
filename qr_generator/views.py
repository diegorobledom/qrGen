from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from io import BytesIO
import base64

def generate_qr(request):
    qr_code_base64 = None
    if request.method == "POST":
        data = request.POST.get("data")  # Obtener el dato ingresado en el formulario
        # Generar el código QR
        qr = qrcode.make(data)
        
        # Guardar la imagen QR en memoria para mostrarla en la página
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Guardar la imagen QR en la sesión en formato base64
        request.session['qr_image'] = qr_code_base64  # Almacenar como cadena de base64
    
    # Renderizar la plantilla con el código QR si se generó
    return render(request, "qr_generator/index.html", {"qr_code": qr_code_base64})

def download_qr(request):
    # Obtener la imagen QR de la sesión en formato base64
    qr_code_base64 = request.session.get('qr_image')
    
    if qr_code_base64:
        # Decodificar la imagen de base64 a bytes
        qr_image = base64.b64decode(qr_code_base64)
        # Configurar la respuesta para descargar la imagen
        response = HttpResponse(qr_image, content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename="qr_code.png"'
        return response
    else:
        return HttpResponse("No QR code available for download.", status=400)
