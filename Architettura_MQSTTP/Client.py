import asyncio
import sys
import  protocollo as p

HOST = "127.0.0.1"
PORTA = 9999


def leggi_indirizzo(testo):
    host, _, porta = testo.partition(":")
    return host or HOST, int(porta) if porta else PORTA

async def ricevi(reader, writer):
    while True:
        dati = await reader.readline()
        if not dati:
            if not writer.is_closing():             # ha chiuso il broker, non noi
                print("Il broker ha chiuso la connessione (premi Invio per uscire)")
                writer.close()
            break
        print(dati.decode().strip())

