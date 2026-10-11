# FICHE DE REVISION — PROJET TRANSFERT DE PHOTOS
# Python / pathlib / fichiers / Anaconda / Spyder

============================================================
1. STRUCTURE ACTUELLE DU PROJET
============================================================

Objectif :
1. Brancher un appareil photo à l'ordinateur.
2. Chercher les photos de l'appareil qui ne sont pas déjà sur le PC.
3. Copier uniquement les nouvelles photos vers le PC.
4. Faire ensuite la même chose du PC vers le téléphone.
5. Produire un bilan du transfert.

Pipeline visé :

    source
      ↓
  detection()
      ↓
 photos nouvelles
      ↓
ajouter_nouvelles()
      ↓
      bilan
      ↓
 transferer()

Version actuelle :
- extensions acceptées : .jpg, .jpeg, .png, .jfif
- les photos sont comparées par leur nom
- les nouvelles photos sont stockées dans un set de Path
- shutil.copy() réalise la copie
- un dictionnaire global bilan est construit dans transferer()


============================================================
2. PATHLIB — CHEMINS ET DOSSIERS
============================================================

from pathlib import Path

Créer un objet chemin :
    dossier = Path("D:/Photos_pc")

Vérifier qu'un chemin existe :
    dossier.exists()

Vérifier que c'est un dossier :
    dossier.is_dir()

Vérifier que c'est un fichier :
    fichier.is_file()

Parcourir le contenu direct d'un dossier :
    dossier.iterdir()

Exemple :
    for element in dossier.iterdir():
        print(element)

Obtenir le nom :
    element.name

Obtenir l'extension :
    element.suffix

Extension en minuscules :
    element.suffix.lower()

Construire un chemin :
    destination / photos.name

Exemple :
    Path("D:/Photos_pc") / "IMG_001.jpg"

Créer un dossier :
    dossier.mkdir()

Créer aussi les dossiers parents :
    dossier.mkdir(parents=True)

Ne pas provoquer d'erreur si le dossier existe déjà :
    dossier.mkdir(exist_ok=True)

Les deux :
    dossier.mkdir(parents=True, exist_ok=True)


============================================================
3. SET — ENSEMBLES
============================================================

Créer un set vide :
    nouvelles = set()

Ajouter un élément :
    nouvelles.add(element)

Taille :
    len(nouvelles)

Parcourir :
    for photo in nouvelles:
        print(photo)

Différence entre deux sets :
    nouvelles = photos_appareil - photos_pc

Intérêt dans le projet :
- éviter les doublons
- comparer facilement deux ensembles de noms


============================================================
4. DICTIONNAIRE
============================================================

Créer :
    bilan = {}

Ajouter une information :
    bilan["erreurs"] = 2

Lire :
    bilan["erreurs"]

Parcourir :
    for cle, valeur in bilan.items():
        print(cle, valeur)

Dans le projet :
    bilan = {
        "reussite_detection": ...,
        "erreur_detection": ...,
        "reussite_ajout": ...,
        "erreur_ajout": ...,
        "photos_erreur_ajout": ...
    }

Choix actuel :
un seul dictionnaire global est suffisant pour la taille du projet.


============================================================
5. CONDITIONS
============================================================

ET :
    condition1 and condition2

OU :
    condition1 or condition2

NON :
    not condition

Exemple du projet :
    if (
        photos.suffix.lower() in extensions
        and not (destination / photos.name).exists()
        and photos.is_file()
    ):

Test d'appartenance :
    extension in extensions

Test inverse :
    extension not in extensions


============================================================
6. FONCTIONS
============================================================

Définir :
    def ma_fonction(argument):
        ...

Retourner une valeur :
    return resultat

Plusieurs valeurs :
    return valeur1, valeur2

Récupérer plusieurs valeurs :
    a, b = ma_fonction()

Exemple :
    nouvelles, erreur, reussi = detection(source, destination)

Attention :
    print() affiche une information.
    return transmet une information à la partie du programme
    qui a appelé la fonction.

Dans ce projet, transferer() affiche actuellement le bilan
directement : pas besoin de return tant qu'on ne réutilise pas
le bilan ailleurs.


============================================================
7. TRY / EXCEPT
============================================================

Structure :
    try:
        operation_risquee
    except Exception as e:
        print("Erreur :", e)

Pourquoi ?
Certaines opérations liées aux fichiers dépendent du système
de fichiers, des droits, du périphérique, etc.

Dans une boucle, placer le try au bon niveau permet de continuer
avec les autres photos si une seule échoue.

Exemple :
    for photo in nouvelles:
        try:
            shutil.copy(photo, destination / photo.name)
        except Exception as e:
            print("Erreur :", e)

Eviter autant que possible :
    except:

Préférer :
    except Exception as e:

Cela permet de voir le message réel de l'erreur.


============================================================
8. SHUTIL — COPIE DE FICHIERS
============================================================

Importer :
    import shutil

Copier :
    shutil.copy(source, destination)

Dans le projet :
    shutil.copy(photos, destination / photos.name)

Ici :
- photos = Path du fichier source
- destination / photos.name = chemin de destination


============================================================
9. NOTIONS ACTUELLES DU PROJET
============================================================

extensions = {".jpg", ".jpeg", ".png", ".jfif"}

Pourquoi un set ?
- appartenance rapide
- pas de doublons
- syntaxe :
      extension in extensions

detection(source, destination)
→ parcourt la source
→ garde uniquement les extensions autorisées
→ vérifie que la photo n'existe pas déjà dans destination
→ ajoute les nouveaux Path dans un set
→ retourne nouvelles, erreur, reussi

ajouter_nouvelles(source, destination, nouvelles)
→ tente la copie de chaque photo
→ compte les réussites et erreurs
→ mémorise les noms des photos en erreur

transferer(source, destination)
→ orchestre les fonctions
→ récupère leurs résultats
→ construit le bilan global
→ affiche le bilan


============================================================
10. CONCEPTION DU PIPELINE
============================================================

Principe important :

Chaque fonction a une responsabilité.

detection()
    → trouver les photos à transférer

ajouter_nouvelles()
    → effectuer les copies

transferer()
    → coordonner les étapes et produire le bilan

On évite pour l'instant de créer un dictionnaire pour chaque étape :
un seul bilan global est suffisant.

Si le projet devient beaucoup plus gros, on pourra structurer
le bilan par étape.


============================================================
11. PROCHAINE NOTION À APPRENDRE
============================================================

Vérifier et préparer les dossiers.

Source :
    doit exister
    doit être un dossier
    sinon → erreur

Destination :
    si elle existe → vérifier que c'est un dossier
    si elle n'existe pas → la créer

Syntaxe à apprendre :
    dossier.mkdir()
    dossier.mkdir(parents=True)
    dossier.mkdir(exist_ok=True)
    dossier.mkdir(parents=True, exist_ok=True)


============================================================
12. ANACONDA — LEXIQUE DE BASE
============================================================

ENVIRONNEMENT
Un environnement contient une version de Python et des paquets
indépendants des autres environnements.

Voir les environnements :
    conda env list

ou :
    conda info --envs

Créer un environnement :
    conda create -n mon_env python=3.10

Activer :
    conda activate mon_env

Désactiver :
    conda deactivate

Supprimer un environnement :
    conda remove -n mon_env --all

Voir les paquets installés :
    conda list

Installer un paquet avec conda :
    conda install nom_du_paquet

Installer avec pip :
    pip install nom_du_paquet

Mettre à jour un paquet :
    conda update nom_du_paquet

Voir la version de Python :
    python --version

Voir où se trouve Python :
    where python

IMPORTANT :
- conda gère les environnements et les paquets.
- pip est le gestionnaire de paquets Python.
- éviter de mélanger les installations au hasard.
- quand un environnement fonctionne, noter sa configuration.


============================================================
13. SPYDER ET ENVIRONNEMENTS
============================================================

Spyder doit utiliser le bon environnement Python.

Avant de chercher un problème dans le code, vérifier :
1. quel environnement est utilisé ;
2. quelle version de Python est utilisée ;
3. si les paquets nécessaires sont installés dans CET
   environnement.

Dans un script Spyder, tu peux tester :

    import sys
    print(sys.executable)

Cela indique quel Python exécute réellement le script.

Tu peux aussi faire :

    import sys
    print(sys.version)

Très utile si tu as plusieurs installations Python.


============================================================
14. DIAGNOSTIC RAPIDE D'UN PROBLEME D'ENVIRONNEMENT
============================================================

Si un import ne fonctionne pas :

    import nom_du_module

et que Python indique que le module n'existe pas :

1. vérifier l'interpréteur :
       import sys
       print(sys.executable)

2. vérifier l'environnement dans Anaconda :
       conda env list

3. activer l'environnement voulu :
       conda activate mon_env

4. vérifier le paquet :
       conda list

ou :
       pip show nom_du_paquet

Ne pas installer immédiatement un paquet sans vérifier
quel Python Spyder utilise.


============================================================
15. CHEAT SHEET ULTRA-RAPIDE
============================================================

Path :
    Path("D:/Photos")
    .exists()
    .is_dir()
    .is_file()
    .iterdir()
    .name
    .suffix
    .mkdir()
    .mkdir(parents=True, exist_ok=True)

Set :
    set()
    .add(x)
    len(set)
    x in set
    setA - setB

Dict :
    {}
    d["cle"] = valeur
    d["cle"]
    d.items()

Boucle :
    for x in collection:

Condition :
    and
    or
    not
    in
    not in

Fonction :
    def f(x):
        ...
        return resultat

Erreur :
    try:
        ...
    except Exception as e:
        print(e)

Copie :
    shutil.copy(source, destination)

Anaconda :
    conda env list
    conda activate ENV
    conda deactivate
    conda list
    conda install PACKAGE
    python --version
    where python

Spyder :
    import sys
    print(sys.executable)
    print(sys.version)
