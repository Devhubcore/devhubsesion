async def print_chat_to_terminal(client, user, limit=20):
    entity = await client.get_entity(user)
    messages = await client.get_messages(entity, limit=limit)
    
    for msg in reversed(messages):
        date = msg.date.strftime("%Y-%m-%d %H:%M") if msg.date else "-"
        
        m_type = ""
        if msg.photo: m_type = "[عکس]"
        elif msg.voice: m_type = "[ویس]"
        elif msg.video: m_type = "[ویدیو]"
        
        text = msg.text if msg.text else m_type
        print(f"[{date}] {text}")


async def search_in_chats(client, keyword, chat_id=None, limit=100):
    results = []
    
    if chat_id:
        entity = await client.get_entity(chat_id)
        messages = await client.get_messages(entity, search=keyword, limit=limit)
        for msg in messages:
            results.append({
                "chat_id": entity.id,
                "chat_name": getattr(entity, 'first_name', None) or getattr(entity, 'title', None) or "chat",
                "text": msg.text or "[media]",
                "date": msg.date.isoformat() if msg.date else None
            })
    else:
        me = await client.get_me()
        async for dialog in client.iter_dialogs():
            if dialog.is_user and dialog.entity.id != me.id:
                try:
                    messages = await client.get_messages(dialog.entity, search=keyword, limit=limit)
                    for msg in messages:
                        results.append({
                            "chat_id": dialog.entity.id,
                            "chat_name": getattr(dialog.entity, 'first_name', None) or "chat",
                            "text": msg.text or "[media]",
                            "date": msg.date.isoformat() if msg.date else None
                        })
                except Exception:
                    continue
                    
    return results
