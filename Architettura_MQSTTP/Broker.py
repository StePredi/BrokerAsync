import asyncio
import logging

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

    async def avvia(self):
        server = await asyncio.start_server(self.gestisci_client, self.host, self.porta)
        print(f"Broker in ascolto su {self.host}:{self.porta}")
        async with server:
            await server.serve_forever()

    async def gestisci_client(self, reader, writer):
        ip, porta = writer.get_extra_info("peername")[:2]
        nome = f"{ip}:{porta}"
        logger = logging.getLogger(nome)
        logger.info(f"Instaurata la connessione")
        try:
            while True:
                dati = await reader.readline()
                if not dati:                      # il client ha chiuso
                    break

        except ConnectionError:                   # il client è caduto all'improvviso
            pass
        finally:
            print(nome, "disconnesso")
            writer.close()


if __name__ == "__main__":
    try:
        asyncio.run(Broker().avvia())
    except KeyboardInterrupt:
        print("\nBroker fermato")
