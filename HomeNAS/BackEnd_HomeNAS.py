from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Chemin du dossier de stockage des fichiers
storage_path = "C:\\Partage"

# Endpoint pour télécharger un fichier
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join(storage_path, filename)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"message": "Fichier non trouvé"})

# Endpoint pour téléverser un fichier
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "Aucun fichier téléversé"})
    file = request.files["file"]
    if file and file.filename != "":
        file.save(os.path.join(storage_path, file.filename))
        return jsonify({"message": "Fichier téléversé avec succès"})
    else:
        return jsonify({"message": "Erreur lors du téléversement du fichier"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
