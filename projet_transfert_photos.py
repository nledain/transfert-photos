from pathlib import Path
import shutil
import hashlib
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import subprocess

# =========================
# CHEMINS
# =========================

dossier_pc = Path("C:\Photos\photo_pc")
dossier_appareil = Path("C:\Photos\photo_appareil")
fake_dossier_pc=Path("C:\Photos\photo_pc\DSC00133.JPG")
video_random1=Path("C:\Photos\photo_appareil\video_test.mov")
video_random2=Path("C:\Photos\photo_appareil\karma.mp4")

extensions_photos = {".jpg", ".jpeg", ".png", ".jfif"}
extensions_videos = {".mp4",".mov",".avi",".mkv"}


# =========================
# DETECTION
# =========================


def detection(source, destination, extensions):
    nouvelles = set()
    n = 0

    fichiers_destination = {}

    try:
        # Création d'un index des fichiers déjà présents
        for fichier in destination.rglob("*"):
            if fichier.is_file() and fichier.suffix.lower() in extensions:
                fichiers_destination.setdefault(
                    fichier.name, []
                ).append(fichier)

        # Parcours de la source
        for photos in source.rglob("*"):
            try:
                if (
                    photos.suffix.lower() in extensions
                    and photos.is_file()
                ):

                    # Aucun fichier avec ce nom dans la destination
                    if photos.name not in fichiers_destination:
                        nouvelles.add(photos)

                    else:
                        taille_source = photos.stat().st_size
                        doublon = False

                        for fichier in fichiers_destination[photos.name]:

                            taille_destination = fichier.stat().st_size

                            # Même nom mais taille différente :
                            # ce n'est pas le même fichier
                            if taille_source != taille_destination:
                                continue

                            # Même nom + même taille :
                            # empreinte rapide
                            empreinte_source = calculer_empreinte_rapide(
                                photos
                            )

                            empreinte_destination = calculer_empreinte_rapide(
                                fichier
                            )

                            if empreinte_source == empreinte_destination:
                                doublon = True
                                break

                        # Aucun doublon trouvé
                        if not doublon:
                            nouvelles.add(photos)

            except Exception as e:
                print("Erreur :", e)
                n += 1

        print(
            f"Bonne detection des médias, "
            f"il y a {len(nouvelles)} nouveaux médias"
        )

    except Exception as e:
        print("Erreur :", e)

    print(
        f"Il y a eu un problème de detection avec {n} médias"
    )

    reussi = len(nouvelles)
    erreur = n

    return nouvelles, erreur, reussi


# =========================
# AFFICHAGE
# =========================

def affichage(nouvelles):
    for photos in nouvelles:
        print(photos.name)


# =========================
# COPIE
# =========================

def ajouter_nouvelles(
    destination,
    nouvelles,
    suivre_rangement_source=False,
    racine_source=None
):
    n = 0
    d = 0
    erreur_liste = set()

    try:
        for photos in nouvelles:
            n += 1

            try:
                if suivre_rangement_source:
                    if racine_source is None:
                        raise ValueError(
                            "La racine de la source n'est pas définie."
                        )

                    chemin_relatif = photos.relative_to(racine_source)

                    new_desti = destination / chemin_relatif.parent
                    new_desti.mkdir(parents=True, exist_ok=True)

                else:
                    new_desti = trouver_dossier_chrono(
                        photos, destination
                    )

                nom_final_chemin = trouver_nom_disponible(
                    photos, destination
                )

                taille_source = photos.stat().st_size

                shutil.copy(
                    photos,
                    new_desti / nom_final_chemin.name
                )

                new_photos = new_desti / nom_final_chemin.name

                taille_desti = new_photos.stat().st_size

                if taille_source == taille_desti:
                    print("Bonne copie du média", n)

                else:
                    print(
                        "Problème dans la qualité "
                        "de la copie du média"
                    )
                    d += 1
                    erreur_liste.add(photos.name)

            except Exception as e:
                print("Erreur :", e)
                print("Problème dans la copie du média", n)
                d += 1
                erreur_liste.add(photos.name)

        print(
            n - d,
            "ont été ajoutés à la destination et",
            d,
            "problème(s) lors des copies"
        )

    except Exception as e:
        print("Erreur :", e)

    reussi = n - d
    erreur = d

    return erreur, reussi, erreur_liste


# =========================
# TRANSFERT
# =========================

def transferer(
    source,
    destination,
    extensions,
    suivre_rangement_source=False,
    racine_source=None
):
    valide, destination = verifier_dossier(source, destination)

    if valide:
        nouvelles, erreur_detec, reussite_detec = detection(
            source, destination, extensions
        )

        erreur_ajout, reussite_ajout, liste_erreur_ajout = ajouter_nouvelles(
            destination,
            nouvelles,
            suivre_rangement_source=suivre_rangement_source,
            racine_source=racine_source
        )

        return (
            reussite_detec,
            erreur_detec,
            reussite_ajout,
            erreur_ajout,
            liste_erreur_ajout
        )

    else:
        print(
            "La vérification n'a pas abouti, "
            "le transfert ne peut pas continuer"
        )

        return 0, 1, 0, 0, set()
        
# Prochaine étape du projet :
# créer verifier_dossiers(source, destination)
# - source : doit exister et être un dossier
# - destination : si absente, la créer avec mkdir()


def verifier_dossier(source, destination):
    source_valide = False
    destination_valide = False
    # =========================
    # VERIFICATION DE LA SOURCE
    # =========================
    if source.is_dir():
        print("Source valide")
        source_valide = True
    elif source.exists():
        print("La source renseignée n'est pas un dossier")
    else:
        print("La source n'existe pas")
    # =========================
    # VERIFICATION DE LA DESTINATION
    # =========================
    
    if destination.is_dir():
        print("La destination est valide")
        destination_valide = True
    
    
    # La destination n'existe pas
    elif not destination.exists():
        print("La destination n'existe pas")
        print("Création du dossier photo ?")
        
        while True:
            
            choix = input("oui/non : ")
            
            if choix == "oui":
                
                # On crée directement la destination prévue
                destination.mkdir(parents=True, exist_ok=True)
                
                print("Dossier créé")
                print(f"Dossier créé ici : {destination.absolute()}")
                
                destination_valide = True
                break
                
            elif choix == "non":
                print("Fin du programme alors")
                break
                
            else:
                print(
                    "Réponse invalide, "
                    "il faut répondre par 'oui' ou 'non'."
                )
    
    
    # La destination existe mais c'est un fichier
    else:
        
        print("La destination n'est pas un dossier, c'est un fichier")
        print("Création d'un dossier à côté ?")
        
        while True:
            
            choix = input("oui/non : ")
            
            if choix == "oui":
                
                nom_doss = input(
                    "Nom du dossier de photos pour la destination : "
                )
                
                # Création à côté du fichier renseigné
                destination = destination.parent / nom_doss
                
                destination.mkdir(
                    parents=True,
                    exist_ok=True
                )
                
                print(f"Dossier '{nom_doss}' créé")
                print(f"Dossier créé ici : {destination.absolute()}")
                
                destination_valide = True
                break
                
                
            elif choix == "non":
                
                print(
                    "On met les photos à côté du fichier renseigné alors ?"
                )
                
                while True:
                    
                    choix = input("oui/non : ")
                    
                    if choix == "oui":
                        
                        destination = destination.parent
                        destination_valide = True
                        break
                        
                    elif choix == "non":
                        
                        print("Bon bah on avance pas")
                        break
                        
                    else:
                        print(
                            "Réponse invalide, "
                            "il faut répondre par 'oui' ou 'non'."
                        )
                
                break
                
                
            else:
                print(
                    "Réponse invalide, "
                    "il faut répondre par 'oui' ou 'non'."
                )
    
    
    # =========================
    # BILAN FINAL
    # =========================
    
    print("\nBilan vérification :")
    
    if source_valide and destination_valide:
        print("Tout est bon, passage au transfert")
        return True, destination
        
    else:
        print("Problème de fichier")
        return False, destination
        
#_,desti=verifier_dossier(dossier_appareil,dossier_pc)
#print("la destination des photos est:\n",desti)

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
    sortie=subprocess.run([r"C:\INSA\Miniconda\envs\sandbox\bin\exiftool.bat",
    "-time:all","-G1","-a","-s", str(chemin)],
    capture_output=True,
    text=True)
    date=""
    priorite=["DateTimeOriginal", "CreationDate","MediaCreateDate", "CreateDate"]
    if sortie.returncode==0:
        for nom_date in priorite:
            for line in sortie.stdout.strip().splitlines():
                nom_tag=line.split()[1]
                if nom_date==nom_tag:
                    pre_date1=line
                    pre_date2=pre_date1.split(": ", 1)[1]
                    try:
                        date=datetime.strptime(pre_date2,"%Y:%m:%d %H:%M:%S")
                    except Exception as e:
                        date=""
                    break
            if date:
                break
        if not date:
            date=trouver_date_fichier_sans_meta(chemin)
    else:
        print("souci pour trouver la date de la vidéo {chemin.name}, l'extraction des metadonnées a eu un soucis")
    return date

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
        
# =========================
# SOURCES 
# =========================

def detecter_sources():
    lecteurs_exclus = {
        Path("C:\\"),
    }

    sources = []

    for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        lecteur = Path(f"{lettre}:\\")

        if lecteur.exists() and lecteur not in lecteurs_exclus:
            sources.append(lecteur)

    return sources 


def trouver_sources(stockages, extensions):
    sources = []

    for stockage in stockages:
        for fichier in stockage.rglob("*"):
            if fichier.is_file() and fichier.suffix.lower() in extensions:
                dossier = fichier.parent

                if dossier not in sources:
                    sources.append(dossier)

    return sources


def filtrer_sources(sources):
    sources = sorted(
        set(Path(source) for source in sources),
        key=lambda chemin: len(chemin.parts)
    )

    sources_filtrees = []

    for source in sources:
        # Vérifier si un parent est déjà retenu
        parent_deja_present = any(
            source.is_relative_to(parent)
            for parent in sources_filtrees
        )

        if not parent_deja_present:
            sources_filtrees.append(source)

    return sources_filtrees


# =========================
# MAIN
# =========================

def main():

    print("===== TRANSFERT DE MÉDIAS =====")

    # Choix de la nature de la source
    print("\nNature de la source :")
    print("1 - Tous les disques externes détectés")
    print("2 - Un dossier précis")

    choix_source = input("Choix (1 ou 2) : ").strip()

    while choix_source not in {"1", "2"}:
        print("Réponse invalide.")
        choix_source = input("Choix (1 ou 2) : ").strip()

    if choix_source == "1":
        stockages = detecter_sources()

        if not stockages:
            print("Aucun stockage détecté.")
            return

        print("\nStockages détectés :")
        for stockage in stockages:
            print("-", stockage)

    else:
        chemin_source = input(
            "\nChemin du dossier source : "
        ).strip().strip('"')

        dossier_source = Path(chemin_source)

        if not dossier_source.exists() or not dossier_source.is_dir():
            print("Le dossier indiqué n'existe pas ou n'est pas valide.")
            return

        stockages = [dossier_source]

        print("\nDossier source sélectionné :", dossier_source)

    # Choix du type de média pour tout le transfert
    extensions = choisir_media()

    # Recherche de tous les dossiers contenant des médias
    sources = trouver_sources(stockages, extensions)
    sources = filtrer_sources(sources)

    if not sources:
        print("Aucune source contenant des médias n'a été trouvée.")
        return

    print("\nSources contenant des médias :")
    for source in sources:
        print("-", source)

    destination = Path(r"D:\Photo_Naël")

    # Choix du rangement préalable de la destination
    rangement = input(
        "\nFaut-il réorganiser les médias déjà présents "
        "dans la destination ?\n"
        "Réponse (oui ou non) : "
    ).strip().lower()

    while rangement not in {"oui", "non"}:
        print("Réponse invalide, réponds par oui ou non.")
        rangement = input(
            "Faut-il réorganiser les médias déjà présents "
            "dans la destination ?\n"
            "Réponse (oui ou non) : "
        ).strip().lower()

    if rangement == "oui":
        parcourir_media_desti(destination, extensions)

    # Choix du rangement des nouveaux médias
    choix_rangement = input(
        "\nComment ranger les nouveaux médias ?\n"
        "oui : recalculer leur date et les classer chronologiquement\n"
        "non : conserver l'arborescence de la source\n"
        "Réponse (oui ou non) : "
    ).strip().lower()

    while choix_rangement not in {"oui", "non"}:
        print("Réponse invalide, réponds par oui ou non.")
        choix_rangement = input(
            "oui : recalculer leur date\n"
            "non : conserver l'arborescence de la source\n"
            "Réponse (oui ou non) : "
        ).strip().lower()

    suivre_rangement_source = choix_rangement == "non"

    # Compteurs globaux
    total_detection = 0
    total_erreur_detection = 0
    total_ajout = 0
    total_erreur_ajout = 0
    total_erreur_liste = set()

    # Transfert de chaque source
    for source in sources:

        # Retrouver le stockage racine auquel appartient cette source
        racines_valides = [
            Path(stockage)
            for stockage in stockages
            if Path(source).is_relative_to(Path(stockage))
        ]

        if racines_valides:
            racine_source = max(
                racines_valides,
                key=lambda chemin: len(chemin.parts)
            )
        else:
            racine_source = Path(source)

        print(f"\n===== TRANSFERT DEPUIS {source} =====")

        (
            reussite_detec,
            erreur_detec,
            reussite_ajout,
            erreur_ajout,
            liste_erreur_ajout
        ) = transferer(
            source,
            destination,
            extensions,
            suivre_rangement_source=suivre_rangement_source,
            racine_source=racine_source
        )

        # Addition au bilan global
        total_detection += reussite_detec
        total_erreur_detection += erreur_detec
        total_ajout += reussite_ajout
        total_erreur_ajout += erreur_ajout
        total_erreur_liste.update(liste_erreur_ajout)

    # Bilan global
    print("\n===== BILAN GLOBAL =====")
    print("Médias détectés :", total_detection)
    print("Erreurs de détection :", total_erreur_detection)
    print("Médias ajoutés :", total_ajout)
    print("Erreurs de copie :", total_erreur_ajout)
    print("Médias en erreur :", total_erreur_liste)

    print("\n===== FIN DU PROGRAMME =====")


if __name__ == "__main__":
    main()

#%%
dossier_iphone = Path(r"Apple iPhone\Internal Storage\200801_a")

print("Dossier accessible :", dossier_iphone.exists())

if dossier_iphone.exists():
    for fichier in dossier_iphone.iterdir():
        if fichier.is_file():
            print(fichier.name, fichier.stat().st_size, "octets")
            






from pathlib import Path
import win32com.client
import time

# Dossier temporaire sur le PC
destination = Path(r"C:\Photos\test_iphone")
destination.mkdir(parents=True, exist_ok=True)

shell = win32com.client.Dispatch("Shell.Application")
ce_pc = shell.NameSpace(17)

iphone = next(
    element.GetFolder
    for element in ce_pc.Items()
    if element.Name == "Apple iPhone"
)

stockage = iphone.Items().Item("Internal Storage").GetFolder
dossier = stockage.Items().Item("200801_a").GetFolder

# Sélection du premier fichier du dossier
fichier = dossier.Items().Item(0)
print("Fichier sélectionné :", fichier.Name)

# Demander à Windows de copier le fichier vers le PC
dossier_destination = shell.NameSpace(str(destination))
dossier_destination.CopyHere(fichier, 16)

# Attendre que la copie apparaisse
for _ in range(30):
    fichiers = list(destination.iterdir())
    if fichiers:
        break
    time.sleep(1)

fichiers = list(destination.iterdir())

if fichiers:
    for copie in fichiers:
        print("Fichier copié :", copie.name)
        print("Taille :", copie.stat().st_size, "octets")

        try:
            with open(copie, "rb") as f:
                debut = f.read(16)
            print("Lecture réussie :", len(debut), "octets lus")
        except Exception as e:
            print("Erreur de lecture :", e)
else:
    print("Aucun fichier détecté après 30 secondes.")
#%%