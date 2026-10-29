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
            if not writer.is_closing():
                print("Il broker ha chiuso la connessione (premi Invio per uscire)")
                writer.close()
            break
        print(dati.decode().strip())

async def invia(writer):
    while True:
        testo = await asyncio.to_thread(input)
        if writer.is_closing():
            break
        writer.write((testo + p.FINE).encode())
        await writer.drain()
        if testo == p.TERMINA_CONNESSIONE:
            break
    writer.close()

async def main():
    host, porta = leggi_indirizzo(sys.argv[1] if len(sys.argv) > 1 else "")

    try:
        reader, writer = await asyncio.open_connection(host, porta)
    except OSError as e:
        print("Impossibile connettersi al broker:", e)
        return

    print(f"Connesso a {host}:{porta}. Comandi:")
    for cmd in (p.SUBSCRIBE, p.PUBLISHER, p.UNSCRIBE, p.TERMINA_CONNESSIONE):
        print("  ", p.SINTASSI[cmd]["sintassi"].strip())

    await asyncio.gather(ricevi(reader, writer), invia(writer))
    await writer.wait_closed()


asyncio.run(main())