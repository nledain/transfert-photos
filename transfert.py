import shutil

from medias import (
    calculer_empreinte_rapide,
    trouver_dossier_chrono,
    trouver_nom_disponible,
)

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