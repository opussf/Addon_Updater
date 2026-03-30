# Ideas:

## https://wowup.io/

https://github.com/WowUp/WowUp
Note: Found this AFTER I thought I would start this project.

Oh well.

## Startup
use a config file in ~/.addon_updater/  to save settings.

- Sites to check   (curseforge, https://addons.wago.io/)
- WoW Location(s)

## CurseForgeClient

apiHost:  "https://api.curseforge.com"
https://www.curseforge.com/api/v1/mods/311718/files/5899386/download

https://www.curseforge.com/api/v1/mods/311718/files/    (json)
https://www.curseforge.com/api/v1/mods/search


https://support.curseforge.com/en/support/solutions/articles/9000208346-about-the-curseforge-api-and-how-to-apply-for-a-key


WorldofWarcraft = 1

https://www.curseforge.com/api/v1/games/1


957044 - steps

https://www.curseforge.com/api/v1/mods/957044/files/
https://www.curseforge.com/api/v1/mods/957044/files/7660240/download



import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

asyncio.run(fetch("https://api.example.com/data"))

------
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]