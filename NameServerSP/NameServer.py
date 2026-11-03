import asyncio
import logging
import json

HOST = "127.0.0.1"
PORT = 6000

SERVIZI = {
    "time": ("127.0.0.1", 6001),
    "echo": ("127.0.0.1", 6002),
}

async def gestisci_client(reader, writer):
    ip, porta = writer.get_extra_info("peername")[:2]

    nome = f"NameServer_Client({ip}:{porta})"
    logger = logging.getLogger(nome)
    logger.info("Instaurata la connessione")


    try:
        dati = await reader.readline()
        if dati:
            try:
                cmd = json.loads(dati)
            except (json.JSONDecodeError, UnicodeDecodeError):
                res = {"status": "error", "message": "Errore di decodifica"}
            else:
                if not isinstance(cmd, dict):
                    res = {"status": "error", "message" : "formato dati errato"}
                elif cmd.get("cmd") != "lookup":
                    res = {"status": "error", "message": "comando inesistente"}
                elif cmd.get("service") == "time":
                    res = {"status": "ok", "service" : "time", "host" : SERVIZI["time"][0], "port" : SERVIZI["time"][1]}
                elif cmd.get("service") == "echo":
                    res = {"status": "ok", "service" : "echo", "host" : SERVIZI["echo"][0], "port" : SERVIZI["echo"][1]}
                else:
                    res = {"status": "error", "message": "comando non valido"}

                writer.write((json.dumps(res) + "\n").encode())
                await writer.drain()

    except ConnectionResetError:
        logger.info("Connessione interrotta dal client")

    except Exception:
            logger.exception("Errore inatteso")
    finally:
        writer.close()
        await writer.wait_closed()
        logger.info("Connessione chiusa")


async def avvia_server(socket = (HOST, PORT)):
    server_log = logging.getLogger("Name_Server")
    try:
        server = await asyncio.start_server(gestisci_client, socket[0], socket[1])
        server_log.info(f"Server in ascolto: {socket}")
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        server_log.info("Chiusura server")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(message)s",
    )
    try:
        asyncio.run(avvia_server())
    except KeyboardInterrupt:
        print("\nServer chiusi")