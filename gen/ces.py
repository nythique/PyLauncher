import aiohttp, asyncio
from config.settings import CES_TOKEN, CES_URL

async def create_notebook():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{CES_URL}/nb_create",
            headers={"Authorization": f"Bearer {CES_TOKEN}"}
        ) as resp:
            if resp.status == 429:
                # Trop de requêtes, on lit le texte brut pour info
                text = await resp.text()
                return {"error": "Rate limit CES atteinte. Merci de réessayer plus tard.", "details": text}
            if resp.content_type != "application/json":
                text = await resp.text()
                return {"error": "Réponse inattendue de l'API CES.", "details": text}
            return await resp.json()

async def run_code_in_notebook(nb_id, code, lang="python"):
    timeout = aiohttp.ClientTimeout(total=15)  # 15 secondes max
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post(
                f"{CES_URL}/nb_run",
                headers={"Authorization": f"Bearer {CES_TOKEN}", "Content-Type": "application/json"},
                json={"ID": nb_id, "lang": lang, "code": code}
            ) as resp:
                if resp.status == 429:
                    return {"result": "Limite de requêtes atteinte. Merci de réessayer plus tard."}
                if resp.content_type != "application/json":
                    text = await resp.text()
                    return {"result": f"Réponse inattendue de l'API CES (cas de boucle):\n{text}"}
                return await resp.json()
        except asyncio.TimeoutError:
            return {"result": "⏰ Temps d'exécution dépassé (timeout)."}
        except Exception as e:
            return {"result": f"Erreur réseau : {e}"}
""""
async def run_code_in_notebook(nb_id, code, lang="python"):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{CES_URL}/nb_run",
            headers={"Authorization": f"Bearer {CES_TOKEN}", "Content-Type": "application/json"},
            json={"ID": nb_id, "lang": lang, "code": code}
        ) as resp:
            return await resp.json()
"""
async def pause_notebook(nb_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{CES_URL}/nb_pause",
            headers={"Authorization": f"Bearer {CES_TOKEN}", "Content-Type": "application/json"},
            json={"ID": nb_id}
        ) as resp:
            return await resp.json()

async def resume_notebook(nb_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{CES_URL}/nb_resume",
            headers={"Authorization": f"Bearer {CES_TOKEN}", "Content-Type": "application/json"},
            json={"ID": nb_id}
        ) as resp:
            return await resp.json()

async def delete_notebook(nb_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{CES_URL}/nb_delete",
            headers={"Authorization": f"Bearer {CES_TOKEN}", "Content-Type": "application/json"},
            json={"ID": nb_id}
        ) as resp:
            return await resp.json()