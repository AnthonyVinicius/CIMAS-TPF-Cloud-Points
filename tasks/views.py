from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def upload_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']

        # Salva a imagem no diretório de mídia
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        file_url = fs.url(filename)

        return JsonResponse({'image_url': file_url})
    
    return render(request, 'upload_image.html')


