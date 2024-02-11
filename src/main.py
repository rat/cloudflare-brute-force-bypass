import asyncio
import aiohttp
import time

_path_file = '/home/rat/Google Drive/Projetos/Python/cloudflare-brute-force-bypass/output/output.txt'

async def verifica_dominio(ip, portas, dominios, session):
    for porta in portas:
        try:
            async with session.get(f"http://{ip}:{porta}") as response:
                text = await response.text()

                for dominio in dominios:
                    if dominio in text:
                        print(f"O domínio {dominio} foi encontrado no IP {ip} na porta {porta} (HTTP).")
                        
                        with open(_path_file, 'a+') as f:
                                f.write(f'{dominio} encontrado - {ip}:{porta}\n')
        
        except Exception as e:
            pass

        try:
            async with session.get(f"https://{ip}:{porta}", ssl=False) as response:
                text = await response.text()

                for dominio in dominios:
                    if dominio in text:
                        print(f"O domínio {dominio} foi encontrado no IP {ip} na porta {porta} (HTTPS).")
                        
                        with open(_path_file, 'a+') as f:
                                f.write(f'{dominio} encontrado - {ip}:{porta}\n')
        
        except Exception as e:
            pass

async def main(dominios, portas):
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        start = time.time()

        for i in range(1, 256):
            for j in range(1, 256):
                for k in range(1, 256):
                    for l in range(1, 256):
                        ip = f"{i}.{j}.{k}.{l}"
                        tasks.append(verifica_dominio(ip, portas, dominios, session))
        
        end = time.time()
        print(f'Created task list. Total time: {end - start} seconds')

        await asyncio.gather(*tasks)

portas = [80, 443]  # Portas HTTP e HTTPS

dominios = []

asyncio.run(main(dominios, portas))
