from main import app
from flask import render_template, request, redirect, flash
import utils
import os

# rotas
@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("home.html")


@app.route("/las", methods=["GET", "POST"])
def las_view():
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
            utils.process_and_visualize_las(file_path)
            flash("Arquivo processado com sucesso!")
        except Exception as e:
            flash(f"Erro ao processar o arquivo: {e}")
        return redirect(request.url)

    return render_template("las.html")


@app.route("/ply", methods=["GET", "POST"])
def ply_view():
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

        # Processar de acordo com a ação selecionada
        action = request.form.get('action')
        try:
            if action == "visualize":
                utils.process_and_visualize_ply(file_path)
                flash("Arquivo .ply visualizado com sucesso!")
            elif action == "ransac":
                utils.process_and_visualize_automatize_segmentation_RANSAC_ply(file_path)
                flash("Segmentação automatizada com RANSAC realizada com sucesso!")
            elif action == "dbscan":
                utils.process_and_visualize_automatize_segmentation_RANSAC_Euclidean_Grouping_ply(file_path)
                flash("Segmentação automatizada com DBSCAN realizada com sucesso!")
            else:
                flash("Ação inválida.")
        except Exception as e:
            flash(f"Erro ao processar o arquivo: {e}")
        return redirect(request.url)

    return render_template("ply.html")