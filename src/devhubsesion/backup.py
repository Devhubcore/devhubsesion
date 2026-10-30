import os
from .utils import clean, mkdir, now


async def _targets(client, user):
    if user is not None:
        return [await client.get_entity(user)]
    me = await client.get_me()
    out = []
    async for d in client.iter_dialogs():
        if d.is_user and d.entity.id != me.id:
            out.append(d.entity)
    return out


async def backup_voices(client, user, save_path):
    root = mkdir(os.path.join(save_path, f"voices_{now()}"))
    total = 0
    for e in await _targets(client, user):
        n = clean(getattr(e, "first_name", None) or "chat")
        folder = mkdir(os.path.join(root, f"{n}_{e.id}"))
        c = 0
        try:
            async for m in client.iter_messages(e, limit=500):
                if m.voice:
                    c += 1
                    await client.download_media(m, os.path.join(folder, f"{c}.ogg"))
        except Exception:
            continue
        total += c
    return {"folder": root, "total": total}


async def backup_photos(client, user, save_path):
    root = mkdir(os.path.join(save_path, f"photos_{now()}"))
    total = 0
    for e in await _targets(client, user):
        n = clean(getattr(e, "first_name", None) or "chat")
        folder = mkdir(os.path.join(root, f"{n}_{e.id}"))
        c = 0
        try:
            async for m in client.iter_messages(e, limit=500):
                if m.photo:
                    c += 1
                    await client.download_media(m, os.path.join(folder, f"{c}.jpg"))
        except Exception:
            continue
        total += c
    return {"folder": root, "total": total}


async def backup_full(client, save_path):
    root = mkdir(os.path.join(save_path, f"full_{now()}"))
    me = await client.get_me()
    total = 0
    async for d in client.iter_dialogs():
        if not (d.is_user and d.entity.id != me.id):
            continue
        n = clean(getattr(d.entity, "first_name", None) or "chat")
        folder = mkdir(os.path.join(root, f"{n}_{d.entity.id}"))
        c = 0
        with open(os.path.join(folder, "messages.txt"), "w", encoding="utf-8") as f:
            try:
                async for m in client.iter_messages(d.entity, limit=500):
                    c += 1
                    t = m.date.isoformat() if m.date else "-"
                    f.write(f"[{t}] {'me' if m.out else n}: {m.text or ''}\n")
            except Exception:
                continue
        total += c
    return {"folder": root, "total": total}
