<div align="center">

<img src="https://raw.githubusercontent.com/Devhubcore/devhubsesion/main/Library_python.png" width="180"/>

# devhubsesion

**Telegram account manager with session strings — no Telethon code needed.**

[![PyPI](https://img.shields.io/pypi/v/devhubsesion?style=for-the-badge&logo=pypi&color=blue)](https://pypi.org/project/devhubsesion/)
[![Downloads](https://img.shields.io/pypi/dm/devhubsesion?style=for-the-badge&logo=pypi&color=green)](https://pypi.org/project/devhubsesion/)
[![Python](https://img.shields.io/pypi/pyversions/devhubsesion?style=for-the-badge&logo=python&color=yellow)](https://pypi.org/project/devhubsesion/)
[![License](https://img.shields.io/badge/License-Apache--2.0-red?style=for-the-badge)](https://github.com/Devhubcore/devhubsesion)

[![Telegram](https://img.shields.io/badge/Telegram-@Dev__hube-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/Dev_hube)
[![GitHub](https://img.shields.io/badge/GitHub-devhubsesion-181717?style=for-the-badge&logo=github)](https://github.com/Devhubcore/devhubsesion)
[![PyPI](https://img.shields.io/badge/PyPI-devhubsesion-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/devhubsesion/)

</div>

---

## Install

    pip install devhubsesion

---

## Quick start

    from devhubsesion import DevHubSession

    with DevHubSession(
        session_string="your-session-string",
        api_id=123456,
        api_hash="your-api-hash",
    ) as tg:
        print("logged in as:", tg.me.first_name, tg.me.id)

        for c in tg.list_private_chats()[:5]:
            print(c["id"], c["name"])

---

## Update v0.2.0

**New features added:**

1. **Terminal Chat History:** View the latest messages of any chat directly in your terminal.
2. **Advanced Chat Search:** Search for a keyword (e.g., "hello") across all private chats and get the results along with the chat names.

**Upgrade library:**

    pip install --upgrade devhubsesion

**Usage:**

    from devhubsesion import DevHubSession

    API_ID = api_id_here
    API_HASH = 'api_hash_here'
    SESSION = "session_here"

    with DevHubSession(session_string=SESSION, api_id=API_ID, api_hash=API_HASH) as tg:
        tg.print_chat_history("target_id", limit=3)
        
        print()
        print("Search results:")
        
        for r in tg.search("keyword", limit=5):
            print(r['chat_name'])
            print(r['text'])
            print()

---

## Methods

Chats:
- list_private_chats
- list_groups_channels
- dump_history
- last_message
- print_chat_history
- search

Backup:
- backup_voices
- backup_photos
- backup_full

Monitor:
- watch

Contacts:
- list_contacts
- extract_numbers

Account:
- list_active_sessions
- change_bio
- change_name

Send:
- send_message

---

## Security

Never share your session string — it is a full account credential.

- api_id and api_hash are passed by you, never hardcoded.
- The library stores nothing on any server.

---

## Requirements

- Python 3.9+
- Telethon 1.34+

---

<div align="center">

### Links

[![PyPI](https://img.shields.io/badge/PyPI-devhubsesion-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/devhubsesion/)
[![GitHub](https://img.shields.io/badge/GitHub-devhubsesion-181717?style=for-the-badge&logo=github)](https://github.com/Devhubcore/devhubsesion)
[![Issues](https://img.shields.io/badge/Issues-Report-red?style=for-the-badge&logo=github)](https://github.com/Devhubcore/devhubsesion/issues)
[![Telegram](https://img.shields.io/badge/Telegram-@Dev__hube-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/Dev_hube)

</div>

---

<div align="center">

## Developer

### **𝐀𝐬𝐭𝐫𝐚𝐞𝐚**

[![Telegram](https://img.shields.io/badge/Telegram-@Dev__hube-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/Dev_hube)

</div>

---

<div align="center">

**Licensed under Apache-2.0**

Star the project on GitHub if it helps you!

</div>
