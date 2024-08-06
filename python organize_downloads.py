import os
import shutil
import re

def organize_downloads(download_folder):
    # Dictionnaire pour associer les extensions de fichier à leurs dossiers respectifs
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
        'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.flv'],
        'Music': ['.mp3', '.wav', '.aac', '.flac'],
        'Archives': ['.zip', '.rar', '.tar', '.gz'],
        'Programs': ['.exe', '.msi', '.apk', '.bat', '.sh', '.py']
    }

    # Liste des fichiers à ignorer avec des motifs regex
    ignore_patterns = [
        r'^NTUSER\.DAT.*$', r'^ntuser\.dat\.log.*$', r'^ntuser\.ini$',
        r'^\.DS_Store$', r'^thumbs\.db$', r'^desktop\.ini$'
    ]

    def should_ignore(file_name):
        for pattern in ignore_patterns:
            if re.match(pattern, file_name, re.IGNORECASE):
                return True
        return False

    print(f"Organizing files in folder: {download_folder}")
    
    for file_name in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file_name)

        if os.path.isfile(file_path):
            if should_ignore(file_name):
                print(f'Skipping: {file_name} (matches ignore pattern)')
                continue

            try:
                # Trouver le dossier correspondant à l'extension de fichier
                file_extension = os.path.splitext(file_name)[1].lower()
                destination_folder = None
                for folder, extensions in file_types.items():
                    if file_extension in extensions:
                        destination_folder = os.path.join(download_folder, folder)
                        break

                # Si l'extension est inconnue, mettre dans un dossier "Others"
                if destination_folder is None:
                    destination_folder = os.path.join(download_folder, 'Others')

                # Créer le dossier si nécessaire
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                    print(f'Created directory: {destination_folder}')

                # Déplacer le fichier dans le dossier approprié
                shutil.move(file_path, os.path.join(destination_folder, file_name))
                print(f'Moved: {file_name} to {destination_folder}')

            except PermissionError:
                print(f'Skipping: {file_name} (PermissionError)')
            except Exception as e:
                print(f'Error moving {file_name}: {e}')

# Remplacer 'C:/Users/nour-omar/Downloads' par le chemin réel de votre dossier de téléchargements
organize_downloads(r'C:\Users\nour-omar\Downloads')

