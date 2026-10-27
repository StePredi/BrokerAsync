import re

SEP = ":"
FINE = "\n"

#Regex (da usare con re.fullmatch)
REGEX_UTENTE = r"[A-Za-z0-9_.]{3,20}"
REGEX_PASSWORD = r"[^:\n]{4,64}"
REGEX_TOPIC = r"[A-Za-z0-9_.]+"
REGEX_MESSAGGIO = r"[\x20-\x7E]+"       # ASCII stampabile, niente \n

#CMD
LOGIN = "login"
REGISTRAZIONE = "regist"
LOGOUT = "logout"

SUBSCRIBE = "sub"
PUBLISHER = "pub"
UNSCRIBE = "unsub"

TERMINA_CONNESSIONE = "q"

SINTASSI = {
    LOGIN: {
        "sintassi": f"{LOGIN}{SEP}<utente>{SEP}<password>{FINE}",
        "argomenti": [("utente", REGEX_UTENTE), ("password", REGEX_PASSWORD)],
        "login": False
    },
    REGISTRAZIONE: {
        "sintassi": f"{REGISTRAZIONE}{SEP}<utente>{SEP}<password>{FINE}",
        "argomenti": [("utente", REGEX_UTENTE), ("password", REGEX_PASSWORD)],
        "login": False
    },
    LOGOUT: {
        "sintassi": f"{LOGOUT}{FINE}",
        "argomenti": [],
        "login": True
    },
    SUBSCRIBE: {
        "sintassi": f"{SUBSCRIBE}{SEP}<topic>{FINE}",
        "argomenti": [("topic", REGEX_TOPIC)],
        "login": False
    },
    PUBLISHER: {
        "sintassi": f"{PUBLISHER}{SEP}<topic>{SEP}<message>{FINE}",
        "argomenti": [("topic", REGEX_TOPIC), ("message", REGEX_MESSAGGIO)],
        "login": False
    },
    UNSCRIBE: {
        "sintassi": f"{UNSCRIBE}{SEP}<topic>{FINE}",
        "argomenti": [("topic", REGEX_TOPIC)],
        "login": False
    },
    TERMINA_CONNESSIONE: {
        "sintassi": f"{TERMINA_CONNESSIONE}{FINE}",
        "argomenti": [],
        "login": False
    },
}
