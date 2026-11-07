from datetime import datetime
from telethon import events
import os

async def watch(client, user, callback=None, save=False, save_path="."):
    target_id = None
    if user is not None:
        entity = await client.get_entity(user)
        target_id = entity.id

    log_file = None
    if save:
        log_file = os.path.join(save_path, f"watch_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    @client.on(events.NewMessage)
    async def handler(e):
        if not e.is_private:
            return
        if target_id is not None and e.chat_id != target_id:
            return
            
        sender = await e.get_sender()
        sender_name = getattr(sender, "first_name", None) or str(e.chat_id)
        msg_text = e.message.text or "[Media]"
        
        payload = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "chat_id": e.chat_id,
            "sender": sender_name,
            "out": bool(e.message.out),
            "text": msg_text,
        }
        
        direction = "ME" if payload["out"] else "THEM"
        print(f"[{payload['time']}] {direction} | {sender_name}: {msg_text[:50]}")
        
        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                d = "ME" if payload["out"] else "THEM"
                f.write(f"[{payload['time']}] {d} | {sender_name}: {msg_text}\n")
                
        if callback:
            try:
                callback(payload)
            except Exception:
                pass

    try:
        await client.run_until_disconnected()
    finally:
        client.remove_event_handler(handler)
