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


-------
async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()

async def download_file(session: aiohttp.ClientSession, url: str, dest: str):
    async with session.get(url) as response:
        with open(dest, "wb") as f:
            async for chunk in response.content.iter_chunked(1024):
                f.write(chunk)

async def process_curseforge(session: aiohttp.ClientSession, addon: Curseforge):
    # 1. Get files list
    files = await fetch_json(session, addon.getFilesURL())
    # 2. Parse to find most recent (you'll need to implement this logic)
    download_url = find_most_recent(files)
    # 3. Download
    await download_file(session, download_url, "/path/to/dest")

async def process_github(session: aiohttp.ClientSession, addon: GitHub):
    # 1. Get releases
    releases = await fetch_json(session, f"https://api.github.com/repos/{addon.path}/releases/latest")
    # 2. Parse to find the file
    download_url = releases["assets"][0]["browser_download_url"]
    # 3. Download
    await download_file(session, download_url, "/path/to/dest")

async def process_all(addons: list[AddonData]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for addon in addons:
            if isinstance(addon, Curseforge):
                tasks.append(process_curseforge(session, addon))
            elif isinstance(addon, GitHub):
                tasks.append(process_github(session, addon))
        await asyncio.gather(*tasks)

asyncio.run(process_all(addons))