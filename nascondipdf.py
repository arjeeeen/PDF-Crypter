import os
from PyPDF2 import PdfReader, PdfWriter
from cryptography.fernet import Fernet
from colorama import init, Fore, Style
import random

init()
SECRET_KEY = b'go5ysVtkLlbv08fDAKv6ndeayNS7N5QLyFg26xBoDlc='

assert len(SECRET_KEY) == 44, "La chiave segreta deve essere una stringa base64 di 32 byte codificata."

ENCRYPTED_METADATA_KEY = '/EncryptedMetadata'

ascii_art_list = [
    """
::::::\::::::\::::::|   ,::::\                :|           
::|_::|::| ::|::::>    ::|    :::| :\:| :::\ :::| :~~/ :::|
::|~~~ ::::::/::|       '::::/:|   `::| :::/  :|  :::, :|  
                                   .,:' :|                 
""",
    """
    
  ______ ______ ______   _____                      _              
  | ___ \\|  _  \\|  ___| /  __ \\                    | |             
  | |_/ /| | | || |_    | /  \\/ _ __  _   _  _ __  | |_  ___  _ __ 
  |  __/ | | | ||  _|   | |    | '__|| | | || '_ \\ | __|/ _ \\| '__|
  | |    | |/ / | |     | \\__/\\| |   | |_| || |_) || |_|  __/| |   
  \\_|    |___/  \\_|      \\____/|_|    \\__, || .__/  \\__|\\___||_|   
                                       __/ || |                    
                                      |___/ |_|                    

    """,
    """
    
  ██████╗ ██████╗ ███████╗     ██████╗██████╗ ██╗   ██╗██████╗ ████████╗███████╗██████╗ 
  ██╔══██╗██╔══██╗██╔════╝    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
  ██████╔╝██║  ██║█████╗      ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   █████╗  ██████╔╝
  ██╔═══╝ ██║  ██║██╔══╝      ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══╝  ██╔══██╗
  ██║     ██████╔╝██║         ╚██████╗██║  ██║   ██║   ██║        ██║   ███████╗██║  ██║
  ╚═╝     ╚═════╝ ╚═╝          ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                        
 
    """
]

def print_random_ascii_art():
    ascii_art = random.choice(ascii_art_list)
    print(ascii_art)

# Funzione per cifrare i dati
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Funzione per decifrare i dati
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def add_hidden_metadata(input_pdf, output_pdf, metadata, key):
    # Cripta i metadata
    encrypted_metadata = {k: encrypt_data(v, key) for k, v in metadata.items()}
    encrypted_metadata[ENCRYPTED_METADATA_KEY] = "True" 

    # Legge il PDF esistente
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    # Aggiunge le pagine del vecchio PDF al nuovo PDF
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    # Aggiunge metadata nascosti
    pdf_writer.add_metadata(encrypted_metadata)

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

def get_hidden_metadata(input_pdf, key):
    # Leggi il PDF esistente
    pdf_reader = PdfReader(input_pdf)
    encrypted_metadata = pdf_reader.metadata

    # Verifica se il PDF ha l'identificatore speciale
    if ENCRYPTED_METADATA_KEY not in encrypted_metadata:
        raise Exception("Il PDF non contiene metadata criptati con questo tool.")

    # Per il debug: stampiamo i metadati criptati
    print("Encrypted metadata:", encrypted_metadata)

    # Decripta i metadata (escluso l'identificatore speciale)
    encrypted_metadata.pop(ENCRYPTED_METADATA_KEY)
    decrypted_metadata = {k: decrypt_data(v, key) for k, v in encrypted_metadata.items()}
    return decrypted_metadata

if __name__ == "__main__":
    print_random_ascii_art()
    while True:
        try:
            print("1. Nascondi testo all'interno del PDF e criptalo")
            print("2. Decripta eventuali PDF")
            print("3. Esci")
            choice = input(Fore.YELLOW + f"\nSeleziona un'opzione: " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            print(Fore.RED + f"\nInput interrotto dall'utente. - Arrivederci!" + Style.RESET_ALL)
            break

        if choice == '1':
            try:
                input_pdf = input("Inserisci il nome del file PDF di input (con estensione .pdf): ").strip()
                input_pdf = input_pdf.replace('"', '').replace("'", '')

                if not os.path.isfile(input_pdf):
                    print(Fore.RED + f"Errore: Il file '{input_pdf}' non esiste." + Style.RESET_ALL)
                else:
                    output_pdf = input("Inserisci il nome del file PDF di output (con estensione .pdf) (lascia vuoto per usare un nome predefinito): ").strip()
                    output_pdf = output_pdf.replace('"', '').replace("'", '')

                    if not output_pdf:
                        base, ext = os.path.splitext(input_pdf)
                        output_pdf = os.path.join(os.path.dirname(input_pdf), f"{os.path.basename(base)}_modified{ext}")

                    metadata = {
                        '/Title': input("Inserisci il titolo del documento: ").strip(),
                        '/Author': input("Inserisci l'autore del documento: ").strip(),
                        '/Subject': input("Inserisci il soggetto del documento: ").strip(),
                        '/Producer': input("Inserisci il produttore del PDF: ").strip(),
                        '/Keywords': input("Inserisci le parole chiave (separate da virgole): ").strip()
                    }

                    add_hidden_metadata(input_pdf, output_pdf, metadata, SECRET_KEY)
                    print(Fore.GREEN + f"Metadata criptati aggiunti a {output_pdf}" + Style.RESET_ALL)
            except KeyboardInterrupt:
                print(Fore.RED + f"\nErrore: Input interrotto durante la richiesta del file PDF di input." + Style.RESET_ALL)
                break

        elif choice == '2':
            try:
                input_pdf = input("\nInserisci il nome del file PDF da decriptare (con estensione .pdf): ").strip()
                input_pdf = input_pdf.replace('"', '').replace("'", '')

                if not os.path.isfile(input_pdf):
                    print(Fore.RED + f"Errore: Il file '{input_pdf}' non esiste." + Style.RESET_ALL)
                else:
                    hidden_metadata = get_hidden_metadata(input_pdf, SECRET_KEY)
                    print(Fore.YELLOW + "Metadata decrittati:", hidden_metadata + Style.RESET_ALL)
            except KeyboardInterrupt:
                print(Fore.RED + f"\nInput interrotto durante la richiesta del nome del file da decriptare. - Arrivederci!" + Style.RESET_ALL)
                break  

        elif choice == '3':
            print(Fore.CYAN + "Uscita dal programma." + Style.RESET_ALL)
            break  
        else:
            print(Fore.RED + "Scelta non valida. Riprova." + Style.RESET_ALL)