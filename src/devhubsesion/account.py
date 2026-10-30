from telethon.tl.functions.account import GetAuthorizationsRequest


async def list_active_sessions(client):
    r = await client(GetAuthorizationsRequest())
    out = []
    for a in r.authorizations:
        out.append({
            "device": a.device_model,
            "ip": a.ip,
            "country": a.country,
            "current": bool(getattr(a, "current", False)),
        })
    return out


async def change_bio(client, new_bio):
    await client.edit_about(about=new_bio)
    return {"ok": True, "bio": new_bio}


async def change_name(client, first, last=""):
    await client.edit_profile(first_name=first, last_name=last)
    return {"ok": True, "first": first, "last": last}
