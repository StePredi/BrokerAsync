import asyncio
import logging
import re
import protocollo as p

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler()
    ]
)

class Broker:
    def __init__(self, host="127.0.0.1", porta=9999):
        self.host = host
        self.porta = porta
        self.sottoscrizioni = {}
        self.logger = logging.getLogger("Broker")

    async def avvia(self):
        server = await asyncio.start_server(self.gestisci_client, self.host, self.porta)
        self.logger.info(f"Broker in ascolto su {self.host}:{self.porta}")
        async with server:
            await server.serve_forever()

    async def gestisci_client(self, reader, writer):
        ip, porta = writer.get_extra_info("peername")[:2]
        nome = f"{ip}:{porta}"
        logger = logging.getLogger(nome)
        logger.info("Instaurata la connessione")

        try:
            while True:
                dati = await reader.readline()
                if not dati:
                    break
                chiudi = False
                try:
                    riga = dati.decode("ascii").rstrip("\r\n")
                except UnicodeDecodeError:
                    risposta = "ERR solo ASCII"
                else:
                    logger.debug(f"-> {riga}")
                    risposta = await self.elabora(riga, writer)
                    chiudi = (riga == p.TERMINA_CONNESSIONE and risposta == "OK")
                writer.write((risposta + "\n").encode())
                await writer.drain()
                if chiudi:
                    break
        except ConnectionError:
            pass
        finally:
            self.rimuovi_client(writer)
            logger.info("Disconnesso")
            writer.close()

    async def elabora(self, riga, writer):
        comando = riga.split(p.SEP, 1)[0]


        if comando not in p.SINTASSI:
            return "ERR comando sconosciuto"

        cmd = p.SINTASSI[comando]
        parametri = cmd["argomenti"]  # lista di (nome, regex)

        parti = riga.split(p.SEP, len(parametri))
        args = parti[1:]

        if len(args) != len(parametri) or (not parametri and riga != comando):
            return f"ERR sintassi: {cmd['sintassi'].strip()}"

        for valore, (nome, regex) in zip(args, parametri):
            if not re.fullmatch(regex, valore):
                return f"ERR argomento '{nome}' non valido"
        if comando == p.SUBSCRIBE:
            self.sottoscrivi(args[0], writer)
        elif comando == p.UNSCRIBE:
            self.disiscrivi(args[0], writer)
        elif comando == p.PUBLISHER:
            await self.pubblica(args[0], args[1])
        elif comando == p.TERMINA_CONNESSIONE:
            pass
        else:
            return "ERR comando non ancora implementato"
        return "OK"

    def sottoscrivi(self, topic, writer):
        self.sottoscrizioni.setdefault(topic, set()).add(writer)

    def disiscrivi(self, topic, writer):
        iscritti = self.sottoscrizioni.get(topic)
        if iscritti:
            iscritti.discard(writer)
            if not iscritti:  # topic vuoto: lo elimino
                del self.sottoscrizioni[topic]

    async def pubblica(self, topic, messaggio):
        riga = f"{topic}{p.SEP}{messaggio}{p.FINE}".encode()
        for writer in list(self.sottoscrizioni.get(topic, ())):
            try:
                writer.write(riga)
                await writer.drain()
            except ConnectionError:
                self.disiscrivi(topic, writer)

    def rimuovi_client(self, writer):
        for topic in list(self.sottoscrizioni):
            self.disiscrivi(topic, writer)

if __name__ == "__main__":
    try:
        asyncio.run(Broker().avvia())
    except KeyboardInterrupt:
        print("\nBroker fermato")
