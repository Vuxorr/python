import sys
import pystray
import PIL.Image
import requests
import zipfile
import os

# Adres URL do archiwum ZIP z kodem aplikacji na GitHub
github_archive_url = "https://github.com/Vuxorr/python/archive/refs/heads/updater.zip"

# Odczytaj obecną wersję z pliku lokalnego
local_version = "1.0"  # Przykładowa lokalna wersja, możesz odczytać z pliku

# Pobierz numer wersji z GitHub
response = requests.get(github_archive_url)

if response.status_code == 200:
    # Pobierz archiwum ZIP i zapisz je w pliku tymczasowym
    with open("temp_repo.zip", "wb") as zip_file:
        zip_file.write(response.content)

    # Rozpakuj archiwum ZIP do tymczasowego katalogu
    with zipfile.ZipFile("temp_repo.zip", "r") as zip_ref:
        zip_ref.extractall("temp_dir")

    remote_version = "1.1"  # Przykładowa wersja z archiwum ZIP, możesz odczytać z pliku

    if remote_version > local_version:
        print("Dostępna jest nowa wersja:", remote_version)

        # Zastąp pliki w Twojej aplikacji najnowszą wersją
        for root, dirs, files in os.walk("temp_dir/repo-master"):
            for file in files:
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, "temp_dir/repo-master")
                destination_path = os.path.join(".", relative_path)
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                with open(source_path, "rb") as source_file, open(destination_path, "wb") as dest_file:
                    dest_file.write(source_file.read())

        print("Zaktualizowano do wersji:", remote_version)
        # Uaktualnij plik z numerem wersji
        local_version = remote_version
        # Tutaj możesz dodać kod do uruchamiania zaktualizowanej aplikacji
    else:
        print("Twoja wersja jest aktualna.")

    # Usuń plik archiwum ZIP i katalog tymczasowy
    os.remove("temp_repo.zip")
    for file in os.listdir("temp_dir/repo-master"):
        os.remove(os.path.join("temp_dir/repo-master", file))
    os.rmdir("temp_dir/repo-master")

else:
    print("Nie można pobrać informacji o numerze wersji z GitHub.")

image = PIL.Image.open("Karakas.png")

def on_clicked(icon, item):
    if str(item) == "Hello":
        print("hello")
    elif str(item) == "exit":
       icon.stop()

icon = pystray.Icon("wilq2", image, menu=pystray.Menu(
    pystray.MenuItem("Hello2", on_clicked),
    pystray.MenuItem("exit", on_clicked),
    pystray.MenuItem("sub2", pystray.Menu(
        pystray.MenuItem("abc2", on_clicked)
    ))
))

icon.run()
