# Script di Cifratura e Decifrazione di PDF

![Anteprima](https://github.com/arjeeeen/PDF-Crypter/blob/main/preview.png)

Questo script Python consente di cifrare e decifrare dati all'interno di file PDF utilizzando la libreria PyPDF2 e crittografia Fernet. Offre inoltre la possibilità di nascondere metadata all'interno del PDF e criptarli per una maggiore sicurezza.

## Dipendenze
- PyPDF2
- cryptography
- colorama
 
## Installazione delle Dipendenze
Si consiglia di installare le seguenti dipendenze da un file `requirements.txt` per assicurarsi di avere tutte le librerie necessarie. Eseguire il seguente comando:

```bash
pip install -r requirements.txt
```

## Utilizzo
1. **Nascondi testo all'interno del PDF e criptalo:**
    - L'utente può inserire le informazioni desiderate (titolo, autore, soggetto, ecc.) che saranno cifrate e nascoste all'interno del PDF.

2. **Decripta eventuali PDF:**
    - Se un PDF è stato precedentemente modificato utilizzando lo script e contiene metadata criptati, è possibile decifrarli per recuperare le informazioni originali.

## Crediti

> 📫 Contatti:

> Lo script è stato creato da Arjen ed è disponibile su [www.mondohacking.com](www.mondohacking.com)

[![General badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/arjen-van-zwam-aa0b93288/)
[![Views](https://komarev.com/ghpvc/?username=arjeeeen&label=Repository+Views)](https://github.com/arjeeeen/Scan-porte)


Si consiglia di utilizzare questo script con cautela e di mantenere al sicuro la chiave segreta per la crittografia dei dati.
