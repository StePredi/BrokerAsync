import asyncio
import time
# Questa coroutine viene chiamata da asyncio ogni volta che un client si connette.
# Ogni client ha il suo task, con il suo reader (per leggere) e il suo writer (per scrivere).
async def gestisci_client(reader, writer):
    indirizzo = writer.get_extra_info("peername")   # (ip, porta) del client
    print("Connesso:", indirizzo)

    while True:
        dati = await reader.readline()
        if not dati:
            break

        testo = dati.decode().strip()
        print(f"{indirizzo} ha scritto: {testo}")

        #await asyncio.sleep(5)
        #time.sleep(5)
        risposta = testo.upper() + "\n"
        writer.write(risposta.encode())     # stringa -> bytes, messi nel buffer
        await writer.drain()                # aspetta che i dati partano davvero

    print("Disconnesso:", indirizzo)
    writer.close()                          # chiude la connessione
    await writer.wait_closed()


async def main():
    # start_server apre la porta e chiama gestisci_client per ogni nuovo client
    server = await asyncio.start_server(gestisci_client, "127.0.0.1", 8888)
    print("Server in ascolto sulla porta 8888")
    async with server:
        await server.serve_forever()


asyncio.run(main())
