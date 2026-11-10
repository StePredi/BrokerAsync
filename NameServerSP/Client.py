import asyncio
import json

HOST_NS = "127.0.0.1"
PORT_NS = 6000


async def scambia_dati(reader, writer, dati):
    writer.write((json.dumps(dati) + "\n").encode())
    await writer.drain()
    riga = await reader.readline()
    if not riga:
        raise ConnectionError("il server ha chiuso la connessione")
    return json.loads(riga)


async def chiudi(writer):
    writer.close()
    try:
        await writer.wait_closed()
    except ConnectionError:
        pass


async def richiesta_servizio(servizio):
    reader, writer = await asyncio.open_connection(HOST_NS, PORT_NS)
    try:
        richiesta = {"cmd": "lookup", "service": servizio}
        risposta = await scambia_dati(reader, writer, richiesta)
    finally:
        await chiudi(writer)

    if risposta.get("status") != "ok":
        raise RuntimeError(risposta.get("message", "errore dal name server"))
    return risposta["host"], risposta["port"]


async def usa_servizio(servizio, richiesta):
    host, port = await richiesta_servizio(servizio)
    reader, writer = await asyncio.open_connection(host, port)
    try:
        return await scambia_dati(reader, writer, richiesta)
    finally:
        await chiudi(writer)


async def main():
    # time
    risposta = await usa_servizio("time", {"cmd": "time"})
    if risposta.get("status") == "ok":
        print("Ora ricevuta:", risposta["time"])
    else:
        print("Errore time:", risposta.get("message"))

    # echo
    risposta = await usa_servizio("echo", {"cmd": "echo", "text": "ciao"})
    if risposta.get("status") == "ok":
        print("Echo ricevuto:", risposta["text"])
    else:
        print("Errore echo:", risposta.get("message"))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ConnectionRefusedError:
        print("Server non raggiungibile: hai avviato server.py?")
    except (RuntimeError, ConnectionError) as e:
        print("Errore:", e)