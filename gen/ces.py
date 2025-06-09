import aiohttp, asyncio, subprocess, tempfile, os, sys
""" ces = Code Execution Service
"""
async def create_notebook():
    return {"id": "local"}

async def run_code_in_notebook(nb_id, code, lang="python"):
    if lang == "python":
        return await run_python_code_locally(code)
    elif lang == "bash":
        return await run_bash_code_locally(code)
    else:
        return {"result": f"Langage non supporté : {lang}"}

async def run_python_code_locally(code, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        proc = await asyncio.create_subprocess_exec(
            "python", tmp_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            output = stdout.decode() + stderr.decode()
        except asyncio.TimeoutError:
            proc.kill()
            output = "⏰ Temps d'exécution dépassé (timeout)."
    finally:
        os.remove(tmp_path)
    return {"result": output}

async def run_bash_code_locally(code, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        proc = await asyncio.create_subprocess_exec(
            "bash", tmp_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            output = stdout.decode() + stderr.decode()
        except asyncio.TimeoutError:
            proc.kill()
            output = "⏰ Temps d'exécution dépassé (timeout)."
    finally:
        os.remove(tmp_path)
    return {"result": output}

async def delete_notebook(nb_id):
    return {"result": "Notebook supprimé (local)"}
