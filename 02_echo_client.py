# 02 - Client echo
import asyncio


async def main():
    # open_connection restituisce la stessa coppia (reader, writer) che riceve il server
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    messaggi = ["ciao", "come va?", "fine"]
    for testo in messaggi:
        writer.write((testo + "\n").encode())
        await writer.drain()

        risposta = await reader.readline()
        print("Server:", risposta.decode().strip())

    writer.close()
    await writer.wait_closed()


asyncio.run(main())
