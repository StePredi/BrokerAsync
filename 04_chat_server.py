# 04 - Chat server (versione semplice)
# Ogni messaggio ricevuto da un client viene inoltrato a tutti gli altri.

import asyncio

clienti = []   # lista dei writer di tutti i client connessi


async def invia_a_tutti(messaggio, mittente):
    for writer in clienti:
        if writer is not mittente:
            try:
                writer.write(messaggio.encode())
                await writer.drain()
            except ConnectionError:         # quel client si è appena disconnesso
                pass


async def gestisci_client(reader, writer):
    ip, porta = writer.get_extra_info("peername")
    nome = f"{ip}:{porta}"                
    clienti.append(writer)
    print(nome, "è entrato")

    try:
        while True:
            dati = await reader.readline()
            if not dati:
                break
            testo = dati.decode().strip()
            await invia_a_tutti(f"[{nome}] {testo}\n", writer)
    except ConnectionError:
        pass                                 # il client è caduto all'improvviso
    finally:
        clienti.remove(writer)               # in ogni caso lo togliamo dalla lista
        print(nome, "è uscito")
        writer.close()


async def main():
    server = await asyncio.start_server(gestisci_client, "127.0.0.1", 8888)
    print("Chat in ascolto sulla porta 8888")
    async with server:
        await server.serve_forever()


asyncio.run(main())
