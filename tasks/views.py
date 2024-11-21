from django.shortcuts import render
from tasks.utils import process_and_visualize_las
import os

def upload_view(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        # Diretório temporário para salvar arquivos
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Caminho completo do arquivo a ser salvo
        file_path = os.path.join(temp_dir, uploaded_file.name)

        # Salvar o arquivo no diretório temporário
        with open(file_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Chamar a função de processamento e visualização
        try:
            process_and_visualize_las(file_path)
        except Exception as e:
            return render(request, "upload_image.html", {"error": f"Erro ao processar: {str(e)}"})

        # Remover o arquivo temporário (opcional, se não for necessário guardá-lo)
        os.remove(file_path)

        return render(request, "upload_image.html", {"message": "Arquivo processado com sucesso!"})

    return render(request, "upload_image.html")
