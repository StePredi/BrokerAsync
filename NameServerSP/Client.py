import asyncio
import json

HOST_NS = "127.0.0.1"
PORT_NS = 6000

async def scambia_dati(reader, writer, dati):
    writer.write((json.dumps(dati) + "\n").encode())
    await writer.drain()
    riga = await reader.readline()
    if riga:
        return json.loads(riga)
    return None

async def richiesta_servizio(servizio):
    reader, writer = await asyncio.open_connection(HOST_NS, PORT_NS)
    richiesta = {"cmd":"lookup", "service" : servizio}
    risposta = scambia_dati(reader, writer, richiesta)
    if isinstance(risposta, tuple):
