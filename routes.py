from main import app
from flask import render_template, request, redirect, url_for, send_file, flash
from utils import process_and_visualize_las
import os

# rotas
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Verificar se um arquivo foi enviado
        if 'file' not in request.files:
            flash("Nenhum arquivo foi enviado.")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash("Nenhum arquivo selecionado.")
            return redirect(request.url)

        # Salvar o arquivo na pasta temporária
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)

        # Processar o arquivo
        try:
            process_and_visualize_las(file_path)
            flash("Arquivo processado com sucesso!")
        except Exception as e:
            flash(f"Erro ao processar o arquivo: {e}")
        return redirect(request.url)

    return render_template("upload.html")