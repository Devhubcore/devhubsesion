from datetime import datetime
from telethon import events


async def watch(client, user, callback=None):
    tid = None
    if user is not None:
        tid = (await client.get_entity(user)).id

    @client.on(events.NewMessage)
    async def h(e):
        if not e.is_private:
            return
        if tid is not None and e.chat_id != tid:
            return
        s = await e.get_sender()
        p = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "chat_id": e.chat_id,
            "sender": getattr(s, "first_name", None) or str(e.chat_id),
            "out": bool(e.message.out),
            "text": e.message.text or "[media]",
        }
        if callback:
            try:
                callback(p)
            except Exception:
                pass

    try:
        await client.run_until_disconnected()
    finally:
        client.remove_event_handler(h)
