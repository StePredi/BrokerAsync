import asyncio


async def gestisci_client(reader, writer):
    print("Client connesso, invio i dati...")

    writer.write(b"Ciao, sono il server\n")      # per readline()
    writer.write(b"rosso;verde;blu;")            # per readuntil(b";")
    writer.write(b"12345678")                    # per readexactly(4)
    writer.write(b"primo pezzo")                 # per read(100)
    await writer.drain()

    await asyncio.sleep(2)                       # pausa: il resto arriva dopo

    writer.write(b"secondo pezzo, ultimi dati")  # per read()
    await writer.drain()

    writer.close()                               # chiusura: read() termina qui
    await writer.wait_closed()
    print("Dati inviati, connessione chiusa")


async def main():
    server = await asyncio.start_server(gestisci_client, "127.0.0.1", 8888)
    print("Server in ascolto sulla porta 8888")
    async with server:
        await server.serve_forever()


asyncio.run(main())
