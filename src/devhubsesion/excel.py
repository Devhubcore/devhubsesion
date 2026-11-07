import os
from openpyxl import Workbook
from .contacts import list_contacts

async def save_contacts_to_excel(client, save_path, only_id=False):
    contacts_data = await list_contacts(client)
    filepath = os.path.join(save_path, "contacts.xlsx")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Contacts"
    
    if only_id:
        ws.append(["Name", "ID"])
        for c in contacts_data:
            ws.append([c.get('name', ''), c.get('id', '')])
    else:
        ws.append(["Name", "ID", "Username", "Phone"])
        for c in contacts_data:
            ws.append([
                c.get('name', ''), 
                c.get('id', ''), 
                c.get('username') or "-", 
                c.get('phone') or "-"
            ])
        
    wb.save(filepath)
    return filepath, len(contacts_data)

async def save_chat_to_excel(client, user, limit, save_path):
    entity = await client.get_entity(user)
    messages = await client.get_messages(entity, limit=limit)
    
    chat_name = getattr(entity, 'first_name', None) or getattr(entity, 'title', None) or "chat"
    safe_name = "".join([c for c in chat_name if c.isalnum() or c in " -_"]).strip()
    filepath = os.path.join(save_path, f"chat_{safe_name}_{entity.id}.xlsx")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "History"
    ws.append(["Date", "Sender", "Message"])
    
    for m in reversed(messages):
        d = m.date.strftime("%Y-%m-%d %H:%M") if m.date else "-"
        s = "Me" if m.out else "Them"
        t = m.text or "[Media]"
        ws.append([d, s, t])
        
    wb.save(filepath)
    return filepath, len(messages)
