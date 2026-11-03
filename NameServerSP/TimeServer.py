import asyncio
import logging
import json
from datetime import datetime


HOST = "127.0.0.1"
PORT = 6001

async def gesticsci_client(reader, writer):
    ip, porta = writer.get_extra_info("peername")[:2]

    nome = f"Time_Client({ip}:{porta})"
    logger = logging.getLogger(nome)
    logger.info("Instaurata la connessione")

    try:
        while True:
            dati = await reader.readline()
            if not dati:
                break
            try:
                cmd = json.loads(dati)
            except (json.JSONDecodeError, UnicodeDecodeError):
                res = {"status": "error", "message" : "Errore di decodifica"}
            else:
                if not isinstance(cmd, dict):
                    res = {"status": "error", "message" : "formato dati errato"}
                elif cmd.get("cmd") != "time":
                    res = {"status": "error", "message" : "comando inesistente"}
                else:
                    ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    res = {"status": "ok", "time" : ora}

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
    server_log = logging.getLogger("Time_Server")
    try:
        server = await asyncio.start_server(gesticsci_client, socket[0], socket[1])
        server_log.info(f"Server in ascolto: {socket}")
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        server_log.info("Chiusura server")