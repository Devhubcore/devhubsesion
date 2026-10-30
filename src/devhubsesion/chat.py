import os
from .utils import clean, now


async def list_private_chats(client):
    me = await client.get_me()
    out = []
    async for d in client.iter_dialogs():
        if d.is_user and d.entity.id != me.id:
            out.append({
                "id": d.entity.id,
                "name": d.name or "",
                "username": getattr(d.entity, "username", None),
            })
    return out


async def list_groups_channels(client):
    g, c = [], []
    async for d in client.iter_dialogs():
        item = {"id": d.id, "name": d.name}
        if d.is_group:
            g.append(item)
        elif d.is_channel:
            c.append(item)
    return {"groups": g, "channels": c}


async def dump_history(client, user, limit=500, save=True, out_dir="."):
    e = await client.get_entity(user)
    rows = []
    async for m in client.iter_messages(e, limit=limit):
        rows.append({
            "date": m.date.isoformat() if m.date else None,
            "out": bool(m.out),
            "text": m.text or "[media]",
        })
    rows.reverse()
    r = {"chat_id": e.id, "count": len(rows), "messages": rows}
    if save:
        n = clean(getattr(e, "first_name", None) or getattr(e, "title", None) or "chat")
        f = os.path.join(out_dir, f"{n}_{e.id}_{now()}.txt")
        with open(f, "w", encoding="utf-8") as fh:
            for x in rows:
                fh.write(f"[{x['date']}] {'me' if x['out'] else 'them'}: {x['text']}\n")
        r["file"] = f
    return r


async def last_message(client, user):
    e = await client.get_entity(user)
    async for m in client.iter_messages(e, limit=1):
        return {
            "chat_id": e.id,
            "date": m.date.isoformat() if m.date else None,
            "out": bool(m.out),
            "text": m.text or "[media]",
        }
    return None
