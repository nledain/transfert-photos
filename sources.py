import os
from pathlib import Path

def detecter_sources():
    lecteurs = []

    lecteur_systeme = Path(
        os.environ.get("SystemDrive", "C:") + "\\"
    )
    lecteurs_exclus = {lecteur_systeme}

    for lettre in "DEFGHIJKLMNOPQRSTUVWXYZ":
        lecteur = Path(f"{lettre}:/")

        if lecteur.exists() and lecteur not in lecteurs_exclus:
            lecteurs.append(lecteur)

    return lecteurs


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
