image_captioner/
│
├── app/                      # Logica applicativa
│   ├── __init__.py
│   ├── captioner/            # Moduli per generazione caption
│   │   ├── __init__.py
│   │   ├── base_captioner.py         # Classe base / interfaccia
│   │   ├── blip_captioner.py         # Wrapper BLIP
│   │   ├── gpt_captioner.py          # Prompt GPT su output BLIP
│   │   └── style_adapter.py          # Gestione dello stile utente
│   ├── utils/                # Funzioni ausiliarie
│   │   ├── __init__.py
│   │   ├── image_utils.py             # Preprocessing immagini
│   │   └── prompt_utils.py            # Costruzione prompt personalizzato
│   └── config.py            # Configurazioni base (modello, paths, ecc.)
│
├── frontend/                 # Interfaccia utente
│   ├── streamlit_app.py      # Interfaccia con Streamlit
│   └── assets/               # Immagini, CSS personalizzati, ecc.
│
├── tests/                    # Test unitari
│   ├── test_blip.py
│   ├── test_prompting.py
│   └── test_api.py
│
├── notebooks/                # Esperimenti e prototipi
│   └── prompt_tuning.ipynb
│
├── models/                   # (opzionale) File modello se locali
│
├── requirements.txt
├── README.md
└── main.py                   # Entry point per run standalone / API

