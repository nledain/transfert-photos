import hashlib
import shutil
import subprocess
from datetime import datetime
from config import trouver_exiftool

from PIL import Image
from PIL.ExifTags import TAGS

from config import extensions_photos, extensions_videos

def choisir_media():
    print("Quel média veux-tu transférer? \n 1:Photos ; 2:Vidéos ; 3:Les deux")
    while True:
        choix=input("Réponse (1, 2 ou 3):")
        if choix=='1':
            extensions=extensions_photos
            break
        elif choix=='2':
            extensions=extensions_videos
            break
        elif choix=='3':
            extensions=extensions_photos | extensions_videos
            break
        else:
            print("Réponse invalide, rep par 1,2 ou 3")
    return extensions

#extensions_test=choisir_media()
#print(extensions_test)

def calculer_empreinte_rapide(chemin):
    taille_bloc = 64 * 1024  # 64 Ko

    hash_objet = hashlib.sha256()

    with open(chemin, "rb") as fichier:
        taille = fichier.seek(0, 2)

        # Taille du fichier
        hash_objet.update(str(taille).encode())

        # Début du fichier
        fichier.seek(0)
        debut = fichier.read(taille_bloc)
        hash_objet.update(debut)

        # Fin du fichier
        if taille > taille_bloc:
            fichier.seek(-taille_bloc, 2)
            fin = fichier.read(taille_bloc)
            hash_objet.update(fin)

    return hash_objet.hexdigest()

def calculer_hash(chemin):
    with open(chemin, 'rb') as fichier:
        morceau=fichier.read(4096)
        hash_objet = hashlib.sha256()       
        while morceau:
            hash_objet.update(morceau)
            morceau=fichier.read(4096)
    return hash_objet.hexdigest()


def trouver_hash(dossier,extensions):
    hashs=set()
    for fichier in dossier.rglob("*"):
        if fichier.is_file() and fichier.suffix.lower() in extensions:
            hashs.add(calculer_hash(fichier))
    return hashs

def trouver_dossier_chrono(media,destination):
    date2=trouver_date_media(media)
    annee=str(date2.year)
    mois=date2.month
    calendrier={1:'janvier', 2:'fevrier', 3:'mars', 4:'avril', 5:'mai', 6:'juin',
                7:'juillet', 8:'aout', 9:'septembre', 10:'octobre', 11:'novembre',
                12:'decembre'}
    mois2=calendrier[mois]
    chemin=destination/annee/mois2
    chemin.mkdir(parents=True, exist_ok=True)
    return chemin

def afficher_exif(photo):
    exif=Image.open(photo).getexif()
    return exif

#exif=afficher_exif(fake_dossier_pc)
#for clé,valeur in exif.items():
#    print(TAGS.get(clé),":",valeur)
    
def trouver_date_photo(photo):
    exif=afficher_exif(photo)
    if exif:
        new_exif={}
        for cle,valeur in exif.items():
            new_exif[TAGS.get(cle)]=valeur
        if "DateTimeOriginal" in new_exif:
            date1=new_exif["DateTimeOriginal"]
            date2= datetime.strptime(date1,"%Y:%m:%d %H:%M:%S")
            return date2
        elif "DateTime" in new_exif:
            date1=new_exif["DateTime"]
            date2= datetime.strptime(date1,"%Y:%m:%d %H:%M:%S")
            return date2
        else:
            print("Des metadonnes mais pas de date")
            print("on prends la date classique du fichier")
            date1=photo.stat().st_mtime
            date2=datetime.fromtimestamp(date1)
            return date2
    else:
        print("Pas de metadonnées pour cette photo")
        print("on prend la date classique du fichier")
        date1=photo.stat().st_mtime
        date2=datetime.fromtimestamp(date1)
        return date2
    
#print(trouver_date_photo(fake_dossier_pc))


def type_media(chemin):
    if chemin.suffix.lower() in extensions_photos:
        return "photo"
    elif chemin.suffix.lower() in extensions_videos:
        return "video"
    else:
        return "autre"
    
#print(type_media(fake_dossier_pc))
def trouver_date_fichier_sans_meta(chemin):
    date=datetime.fromtimestamp(chemin.stat().st_mtime)
    return date


def trouver_date_video(chemin):
    exiftool = trouver_exiftool()

    if exiftool is None:
        print(
            "ExifTool est introuvable. "
            "Utilisation de la date de modification du fichier."
        )
        return trouver_date_fichier_sans_meta(chemin)

    try:
        sortie = subprocess.run(
            [
                exiftool,
                "-time:all",
                "-G1",
                "-a",
                "-s",
                str(chemin)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"Erreur lors du lancement d'ExifTool : {e}")
        return trouver_date_fichier_sans_meta(chemin)

    priorite = [
        "DateTimeOriginal",
        "CreationDate",
        "MediaCreateDate",
        "CreateDate"
    ]

    if sortie.returncode == 0:
        for nom_date in priorite:
            for ligne in sortie.stdout.splitlines():
                morceaux = ligne.split(None, 1)

                if len(morceaux) != 2:
                    continue

                nom_tag = morceaux[0].split("]")[-1]

                if nom_tag != nom_date:
                    continue

                valeur_date = morceaux[1].strip()

                try:
                    return datetime.strptime(
                        valeur_date,
                        "%Y:%m:%d %H:%M:%S"
                    )
                except ValueError:
                    continue

        print(
            f"Aucune date exploitable trouvée pour {chemin.name}. "
            "Utilisation de la date de modification."
        )
    else:
        print(
            f"ExifTool n'a pas pu lire les métadonnées de "
            f"{chemin.name} : {sortie.stderr.strip()}"
        )

    return trouver_date_fichier_sans_meta(chemin)


def trouver_date_media(chemin):
    nature_fichier=type_media(chemin)
    if nature_fichier=="photo":
        date=trouver_date_photo(chemin)
        return date
    elif nature_fichier=="video":
        date=trouver_date_video(chemin)
        return date
    elif nature_fichier=="autre":
        date=trouver_date_fichier_sans_meta(chemin)
        return date
    
#print(trouver_dossier_chrono(video_random2, dossier_pc))

def parcourir_media_desti(destination, extensions):
    n = 0
    aucun_deplacement = True
    medias = [media 
              for media in destination.rglob("*")
        if media.is_file() and media.suffix.lower() in extensions
    ]
    for media in medias:
        dossier_ideal=trouver_dossier_chrono(media, destination)
        fichier_ideal=dossier_ideal/media.name
        clé_media=calculer_hash(media)
        clé_fichiers=set()
        for fichier in dossier_ideal.rglob("*"):
            #check qu'il existe pas en doublon
            if fichier.is_file():
                clé_fichier=calculer_hash(fichier)
                clé_fichiers.add(clé_fichier)
        if clé_media  not in clé_fichiers:
            aucun_deplacement = False
            #check que le nom soit dispo (vrai doublon ou pas)
            if not fichier_ideal.exists(): #le nom est dispo on déplace
                try:
                    shutil.move(media, dossier_ideal)
                except Exception as e:
                    print("Erreur:", e)
                    n += 1
            elif fichier_ideal.exists(): #le nom est pas dispo on change de nom et on déplace
                nouveau_media=trouver_nom_disponible(media, dossier_ideal)
                try:
                    shutil.move(media.name, nouveau_media)
                except Exception as e:
                    print("Erreur:", e)
                    n += 1
    if aucun_deplacement:
        print("Tout était déjà bien rangé, pas de changement")
    elif n == 0:
        print(f"Aucun souci dans le rangement des fichiers de {destination}")
    elif n >= 1:
        print(f"Il y a eu {n} souci(s) lors du déplacement des fichiers")


def trouver_nom_disponible(media,destination):
    nom_original=media.name
    noms_existants = {f.name for f in destination.rglob("*") if f.is_file()}

    if  nom_original not in noms_existants:
        return media
    n = 2
    while True:
        nouveau_nom = f"{media.stem}-{n}{media.suffix}"
        print("nouveau nom :", nouveau_nom)
        
        if nouveau_nom not in noms_existants:
            return media.with_name(nouveau_nom)
        
        n += 1