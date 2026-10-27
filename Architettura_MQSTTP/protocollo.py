import re

SEP = ":"
FINE = "\n"

#Regex
REGEX_UTENTE = r"[A-Za-z0-9_.]{3,20}"
REGEX_PASSWORD = r"[^|\n]{4,64}"
REGEX_TOPIC = r"^(BrokerSP\)([A-Za-z0-9_.]+\)*"

#CMD
LOGIN = "login"
REGISTRAZIONE = "regist"
LOGOUT = "logout"

SUBSCRIBE = "sub"
PUBLISHER = "pub"
UNSCRIBE = "usab"

TERMINA_CONNESIONE = "q"

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
        "login": True
    },
    PUBLISHER: {
        "sintassi": f"{SUBSCRIBE}{SEP}<topic>{SEP}<message>{FINE}",
        "argomenti": [("topic", REGEX_TOPIC)],
        "login": True
    },
    UNSCRIBE: {
        "sintassi": f"{UNSCRIBE}{SEP}<topic>{FINE}",
        "argomenti": [("topic", REGEX_TOPIC)],
        "login": True
    },
    TERMINA_CONNESIONE: {
        "sintassi": f"{TERMINA_CONNESIONE}{FINE}",
        "argomenti": [],
        "login": False
    },
}



