# 05 - Chat client
# Il client deve fare due cose INSIEME:
#   - ricevere i messaggi degli altri
#   - leggere quello che scriviamo da tastiera
# input() è bloccante, quindi lo eseguiamo in un thread con asyncio.to_thread.
# Scrivi /quit per uscire.

import asyncio


async def ricevi(reader, writer):
    while True:
        dati = await reader.readline()
        if not dati:
            if not writer.is_closing():
                print("Il server ha chiuso la connessione (premi Invio per uscire)")
                writer.close()
            break
        print(dati.decode().strip())


async def invia(writer):
    while True:
        testo = await asyncio.to_thread(input)   # input() gira in un thread separato
        if testo == "/quit" or writer.is_closing():
            break
        writer.write((testo + "\n").encode())
        await writer.drain()
    writer.close()


async def main():
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
    print("Connesso alla chat. Scrivi /quit per uscire.")

    # le due coroutine girano in parallelo
    await asyncio.gather(ricevi(reader, writer), invia(writer))


asyncio.run(main())
