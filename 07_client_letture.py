import asyncio


async def main():
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    # readline(): legge fino a \n (compreso)
    riga = await reader.readline()
    print("readline()        ->", riga)

    # readuntil(sep): legge fino al separatore scelto (compreso)
    for i in range(3):
        colore = await reader.readuntil(b";")
        print("readuntil(b';')   ->", colore)

    # readexactly(n): legge esattamente n byte
    blocco1 = await reader.readexactly(4)
    blocco2 = await reader.readexactly(4)
    print("readexactly(4)    ->", blocco1)
    print("readexactly(4)    ->", blocco2)

    # read(n): legge FINO A n byte, cioè quelli disponibili in quel momento.
    # Il server ha mandato solo "primo pezzo" e poi aspetta 2 secondi:
    # read restituisce subito quegli 11 byte, non aspetta di arrivare a 100.
    pezzo = await reader.read(100)
    print("read(100)         ->", pezzo, f"({len(pezzo)} byte)")

    # read(): legge tutto finché l'altro lato non chiude la connessione
    print("read() in attesa della chiusura...")
    resto = await reader.read()
    print("read()            ->", resto)

    writer.close()
    await writer.wait_closed()


asyncio.run(main())
