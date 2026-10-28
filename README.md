# \# Transfert de photos et vidéos

# 

# \## Présentation

# 

# Ce projet Python permet de transférer des photos et des vidéos depuis un appareil ou un dossier source vers un dossier de destination sur le PC.

# 

# L'objectif est d'éviter de recopier inutilement des fichiers déjà présents, tout en permettant de les organiser chronologiquement à partir de leurs dates.

# 

# Le projet est personnel et sert aussi à travailler sur la manipulation de fichiers, la gestion des métadonnées et l'organisation d'un programme Python en plusieurs modules.

# 

# \## Fonctionnalités

# 

# \- Détection des photos et vidéos à transférer.

# \- Sélection des photos, des vidéos ou des deux.

# \- Recherche des fichiers déjà présents dans la destination, avec comparaison du contenu pour identifier les doublons.

# \- Copie des nouveaux fichiers et gestion des conflits de noms.

# \- Récupération des dates des médias à partir des métadonnées lorsque celles-ci sont disponibles.

# \- Organisation chronologique des médias.

# \- Affichage d'un bilan du transfert, avec les fichiers traités et les éventuelles erreurs.

# 

# Les extensions actuellement prises en charge sont :

# 

# \- Photos : `.jpg`, `.jpeg`, `.png`, `.jfif`

# \- Vidéos : `.mp4`, `.mov`, `.avi`, `.mkv`

# 

# Certaines fonctionnalités dépendent des métadonnées présentes dans les fichiers. Si aucune date exploitable n'est trouvée, le programme peut utiliser la date de modification du fichier.

# 

# \## Organisation du projet

# 

# ```text

# transfert-photos/

# ├── main.py

# ├── config.py

# ├── sources.py

# ├── medias.py

# ├── transfert.py

# ├── requirements.txt

# ├── README.md

# └── tests/

# &#x20;   ├── source\_test/

# &#x20;   │   ├── karma.mp4

# &#x20;   │   ├── test\_01.png

# &#x20;   │   ├── test\_03.png

# &#x20;   │   └── test\_2.jpg

# &#x20;   └── destination\_test/

# &#x20;       └── test\_01.png

# ```

# 

# Les différents modules ont chacun un rôle :

# 

# \- `main.py` : lancement du programme et déroulement du transfert.

# \- `config.py` : extensions prises en charge, destination par défaut et configuration d'ExifTool.

# \- `sources.py` : détection et recherche des sources contenant des médias.

# \- `medias.py` : traitement des médias et récupération de leurs dates.

# \- `transfert.py` : détection des nouveaux fichiers, copie et organisation dans la destination.

# \- `tests/` : fichiers d'exemple pour essayer le programme sans utiliser directement ses propres photos.

# 

# \## Installation

# 

# Le projet utilise Python et des dépendances listées dans `requirements.txt`.

# 

# Récupérer le projet :

# 

# ```bash

# git clone https://github.com/nledain/transfert-photos.git

# cd transfert-photos

# ```

# 

# Installer les dépendances :

# 

# ```bash

# python -m pip install -r requirements.txt

# ```

# 

# \### Configuration d'ExifTool

# 

# ExifTool est un outil externe utilisé pour lire certaines métadonnées, notamment celles des vidéos. Il n'est pas installé par `pip`.

# 

# Télécharger la version Windows autonome depuis le site officiel :

# 

# https://exiftool.org/install.html

# 

# Le chemin vers l'exécutable peut être renseigné localement dans un fichier `config\_local.py`, placé à la racine du projet :

# 

# ```python

# CHEMIN\_EXIFTOOL = r"C:\\chemin\\vers\\exiftool.exe"

# ```

# 

# Ce fichier est ignoré par Git car son contenu dépend de la configuration de chaque utilisateur. Il n'est pas nécessaire de partager son chemin personnel.

# 

# \## Utilisation

# 

# Lancer le programme depuis le dossier du projet :

# 

# ```bash

# python main.py

# ```

# 

# Suivre les indications affichées dans le terminal pour choisir la source, le type de média et les options de rangement proposées.

# 

# La destination par défaut est définie dans `config.py`. Elle peut être adaptée à l'utilisation souhaitée.

# 

# \## Tester le programme avec les fichiers d'exemple

# 

# Avant de tester le programme avec ses propres photos, il est préférable de commencer avec le jeu de test fourni dans `tests/`.

# 

# \### 1. Préparer une destination de test

# 

# Pour éviter de mélanger les fichiers d'exemple avec ses propres photos, utiliser une destination temporaire distincte.

# 

# Dans `config.py`, remplacer temporairement la destination par défaut par :

# 

# ```python

# destination\_par\_defaut = Path.home() / "TransfertPhotos\_test"

# ```

# 

# Cette destination sera créée à l'extérieur du dépôt.

# 

# \### 2. Lancer le programme

# 

# Depuis la racine du projet :

# 

# ```bash

# python main.py

# ```

# 

# Lorsque le programme demande le chemin d'un dossier source, indiquer le chemin du dossier `tests/source\_test`.

# 

# Par exemple, si le dépôt se trouve dans `C:\\Photos` :

# 

# ```text

# C:\\Photos\\tests\\source\_test

# ```

# 

# Choisir ensuite les médias à transférer.

# 

# \### 3. Vérifier le résultat

# 

# Le jeu de test contient plusieurs images et une vidéo. Il permet de vérifier le déroulement du transfert et le traitement de différents types de fichiers.

# 

# Le dossier `tests/destination\_test` contient également une image déjà présente, utile pour préparer des essais de détection des doublons. Il sert de référence pour les tests et n'est pas automatiquement utilisé comme destination par le programme.

# 

# Après l'essai, vérifier les fichiers présents dans `TransfertPhotos\_test` et le bilan affiché dans le terminal.

# 

# Une fois les vérifications terminées, remettre la destination par défaut dans `config.py`.

# 

# \*\*Attention :\*\* ce jeu de fichiers est destiné à des essais manuels. Il ne constitue pas encore une suite de tests automatisés.

# 

# \## Limites actuelles

# 

# Le projet reste en développement. Le fonctionnement dépend notamment des accès aux dossiers, des métadonnées disponibles et de la configuration de l'ordinateur.

# 

# La détection automatique de tous les appareils et la gestion directe de la galerie d'un iPhone ne sont pas encore considérées comme des fonctionnalités finalisées.

# 

# L'objectif est d'améliorer progressivement la fiabilité du transfert et de faciliter son utilisation sur différentes configurations.



