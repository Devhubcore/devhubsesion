import json
import os
import re

from telethon.tl.functions.contacts import GetContactsRequest
from .utils import phones, mkdir, now


async def list_contacts(client):
    r = await client(GetContactsRequest(hash=0))
    out = []
    for u in r.users:
        if u.contact:
            out.append({
                "id": u.id,
                "name": f"{u.first_name or ''} {u.last_name or ''}".strip() or "",
                "username": u.username,
                "phone": u.phone,
            })
    return out


async def extract_numbers(client, limit_per_chat=200, save=False, save_path="."):
    me = await client.get_me()
    res = []
    total = 0
    async for d in client.iter_dialogs():
        if not (d.is_user and d.entity.id != me.id):
            continue
        n = f"{d.entity.first_name or ''} {d.entity.last_name or ''}".strip() or ""
        found = []
        try:
            async for m in client.iter_messages(d.entity, limit=limit_per_chat):
                if not m.text:
                    continue
                for pat in phones:
                    for num in re.findall(pat, m.text):
                        if num not in found:
                            found.append(num)
        except Exception:
            continue
        if found:
            total += len(found)
            res.append({
                "name": n,
                "id": d.entity.id,
                "username": d.entity.username,
                "numbers": found,
            })

    out = {"chats": res, "total_numbers": total}
    if save:
        root = mkdir(os.path.join(save_path, f"numbers_{now()}"))
        base = os.path.join(root, "numbers")
        with open(base + ".json", "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        with open(base + ".txt", "w", encoding="utf-8") as f:
            for r in res:
                f.write(f"{r['name']} ({r['id']})\n")
                for x in r["numbers"]:
                    f.write(f"  {x}\n")
        with open(base + ".csv", "w", encoding="utf-8") as f:
            f.write("name,id,username,numbers\n")
            for r in res:
                u = f"@{r['username']}" if r["username"] else ""
                nums = " | ".join(r["numbers"])
                f.write(f'"{r["name"]}",{r["id"]},"{u}","{nums}"\n')
        out["folder"] = root
    return out
