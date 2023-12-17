import requests
import json
import smtplib
from email.mime.text import MIMEText
import time

def pobierz_pierwsze_5_cyfr(symbol):
    try:
        url = f"https://api.binance.com/api/v3/avgPrice?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            cena = data.get('price', None)
            if cena:
                # Pobierz tylko pierwsze 5 cyfr i przekonwertuj na liczbę całkowitą
                pierwsze_5_cyfr = int(cena.replace('.', '')[:5])
                return pierwsze_5_cyfr
            else:
                print("Nie udało się znaleźć wartości ceny w odpowiedzi API.")
        else:
            print("Nie udało się pobrać danych z API Binance. Kod statusu:", response.status_code)
    except Exception as e:
        print("Wystąpił błąd:", str(e))

def wyslij_email(temat, tresc):
    # Ustawienia serwera SMTP
    smtp_host = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_login = 'vuxore@outlook.com'
    smtp_haslo = 'MARlon123!'

    # Tworzenie obiektu serwera SMTP
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_login, smtp_haslo)

    # Tworzenie wiadomości e-mail
    msg = MIMEText(tresc)
    msg['Subject'] = temat
    msg['From'] = smtp_login
    msg['To'] = 'bazinga26@gmail.com'

    # Wysyłanie wiadomości e-mail
    server.sendmail(smtp_login, 'bazinga26@gmail.com', msg.as_string())

    # Zamykanie połączenia z serwerem SMTP
    server.quit()

# Przykładowe użycie z odświeżaniem co 5 sekund
symbol_btcusdt = "BTCUSDT"
while True:
    wartosc = pobierz_pierwsze_5_cyfr(symbol_btcusdt)
    if wartosc:
        if wartosc > 41950:
            wyslij_email("Przekroczyło 42 tys.", f"Wartość przekroczyła 42 tys. i wynosi teraz {wartosc}.")
        elif wartosc < 41936:
            wyslij_email("Spadło poniżej 41 tys.", f"Wartość spadła poniżej 41 tys. i wynosi teraz {wartosc}.")
        print("Pierwsze 5 cyfr wartości:", wartosc)
    time.sleep(5)

