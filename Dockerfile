# Image de base
FROM python:3.9-slim-buster

# Définit le répertoire de travail
WORKDIR /plotly_dash
#nom du fichier ou il ya tout les documents du projets réuni

# Copie le fichier requirements.txt dans l'image
COPY requirements.txt .

# Installe les dépendances
RUN pip install -r requirements.txt

# Copie tous les fichiers de l'application
COPY . .

# Expose le port 5000
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python3", "app.py"]



#'docker build -t velib_api .' => pour créer l'image 'velib' dans docker

#'docker run -p 5000:5000 velib' => pour exécuter l'api flask dans le conteneur 'velib' dans docker

