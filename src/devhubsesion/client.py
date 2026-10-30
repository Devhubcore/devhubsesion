import asyncio
import os

try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

from telethon import TelegramClient
from telethon.sessions import StringSession

from .exceptions import NotConnectedError, SessionError
from .utils import mkdir
from . import chat, backup, monitor, contacts, account

SAVE = "./devhub_backup"


class DevHubSession:
    def __init__(self, session_string, api_id, api_hash, save_path=SAVE):
        if not session_string or not isinstance(session_string, str):
            raise SessionError("session_string is invalid")
        if not api_id or not api_hash:
            raise SessionError("api_id and api_hash are required")

        self._s = session_string.strip()
        self._i = int(api_id)
        self._h = str(api_hash)
        self.save_path = save_path
        self.client = None
        self.me = None
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    @classmethod
    def from_env(cls, env_file=".env", save_path=SAVE):
        if env_file and os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

        s = os.environ.get("TG_SESSION")
        i = os.environ.get("TG_API_ID")
        h = os.environ.get("TG_API_HASH")
        if not all([s, i, h]):
            raise SessionError("TG_SESSION / TG_API_ID / TG_API_HASH missing")
        return cls(session_string=s, api_id=int(i), api_hash=h, save_path=save_path)

    async def connect_async(self):
        if self.client and self.client.is_connected():
            return self
        self.client = TelegramClient(StringSession(self._s), self._i, self._h)
        await self.client.start()
        self.me = await self.client.get_me()
        mkdir(self.save_path)
        return self

    def connect(self):
        return self._loop.run_until_complete(self.connect_async())

    async def disconnect_async(self):
        if self.client:
            await self.client.disconnect()
            self.client = None

    def disconnect(self):
        return self._loop.run_until_complete(self.disconnect_async())

    def __enter__(self):
        return self.connect()

    def __exit__(self, *a):
        self.disconnect()

    async def __aenter__(self):
        return await self.connect_async()

    async def __aexit__(self, *a):
        await self.disconnect_async()

    def _c(self):
        if not self.client or not self.client.is_connected():
            raise NotConnectedError("call connect() first")
        return self.client

    def _run(self, coro):
        return self._loop.run_until_complete(coro)

    def list_private_chats(self):
        return self._run(chat.list_private_chats(self._c()))

    def list_groups_channels(self):
        return self._run(chat.list_groups_channels(self._c()))

    def dump_history(self, user, limit=500, save=True):
        return self._run(chat.dump_history(self._c(), user, limit, save, self.save_path))

    def last_message(self, user):
        return self._run(chat.last_message(self._c(), user))

    def backup_voices(self, user=None):
        return self._run(backup.backup_voices(self._c(), user, self.save_path))

    def backup_photos(self, user=None):
        return self._run(backup.backup_photos(self._c(), user, self.save_path))

    def backup_full(self):
        return self._run(backup.backup_full(self._c(), self.save_path))

    def watch(self, user=None, callback=None):
        return self._run(monitor.watch(self._c(), user, callback))

    def list_contacts(self):
        return self._run(contacts.list_contacts(self._c()))

    def extract_numbers(self, limit_per_chat=200, save=False):
        return self._run(contacts.extract_numbers(self._c(), limit_per_chat, save, self.save_path))

    def list_active_sessions(self):
        return self._run(account.list_active_sessions(self._c()))

    def change_bio(self, new_bio):
        return self._run(account.change_bio(self._c(), new_bio))

    def change_name(self, first, last=""):
        return self._run(account.change_name(self._c(), first, last))

    def send_message(self, user, text):
        return self._run(self._send(user, text))

    async def _send(self, user, text):
        e = await self._c().get_entity(user)
        await self._c().send_message(e, text)
        return {"to": e.id, "ok": True}
