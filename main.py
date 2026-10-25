from pathlib import Path

from config import destination_par_defaut
from sources import (
    detecter_sources,
    trouver_sources,
    filtrer_sources,
)
from medias import choisir_media, parcourir_media_desti
from transfert import transferer

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

    chemin_destination = input(
        f"\nChemin de destination "
        f"[Entrée pour {destination_par_defaut}] : "
        ).strip().strip('"')

    destination = (
        Path(chemin_destination)
        if chemin_destination
        else destination_par_defaut
        )

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