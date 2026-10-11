# Photo Transfer Project

A Python project for transferring photos and videos from a connected device to a PC archive while avoiding duplicate imports. The project is designed as a practical learning project and is being developed incrementally.

## Features

- Detects connected drives and searches recursively for folders containing media.
- Lets the user choose whether to transfer photos, videos, or both.
- Detects likely duplicates using filenames and file sizes, with fingerprint checks when needed.
- Organizes the archive into year/month folders using media dates when available.
- Reads photo metadata with Pillow and video metadata with ExifTool.
- Avoids overwriting files when a filename already exists.
- Verifies copied file sizes and reports successes and errors.

## Requirements

- Python 3.10 or newer is recommended.
- Dependencies listed in [`requirements.txt`](requirements.txt).
- ExifTool is required for reading video metadata. It is an external executable and must be installed separately; configure the script with the path to the executable if necessary.

Install the Python dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Project structure

```text
project/
├── projet_transfert_photos.py
├── fiche_revision_transfert_photos.md
├── README.md
├── requirements.txt
├── .gitignore
├── photo_appareil/       # Non-personal test data only
└── photo_pc/             # Non-personal test data only
```

The folder names above describe the intended test setup. Adapt them to match the local project structure if it changes.

## Usage

1. Install the Python dependencies.
2. Install ExifTool if video metadata extraction is needed.
3. Connect the source device or drive.
4. Run the script:

   ```bash
   python projet_transfert_photos.py
   ```

5. Follow the prompts in the terminal.

The script currently uses Windows-specific functionality for detecting and browsing connected drives, so it is intended to run on Windows.

## Privacy and test data

Personal photos and videos must not be committed to the repository. The local `photos_nael` archive is personal and should remain outside version control. The `photo_appareil` and `photo_pc` folders should contain only non-personal test files before being published.

Use `.gitignore` to exclude personal archives and any private test data. If personal files were already committed, adding them to `.gitignore` alone is not enough: they must also be removed from Git tracking.

## Current scope

This is a learning project that is still evolving. The script is intended to make media transfers more organized and reduce duplicate imports; it is not yet a general-purpose backup or synchronization system.
