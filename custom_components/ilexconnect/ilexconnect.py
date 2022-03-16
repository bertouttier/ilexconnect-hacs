from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    LOGGER
)

URL = "https://i-lexconnect.com"

class ILexConnectApi:

    def __init__(self, hass, username, password, session=None):
        self._hass = hass
        self._username = username
        self._password = password
        if session is None:
            self._session = async_get_clientsession(hass)
        else:
            self._session = session

    async def login(self):
        url = f"{URL}/login"
        payload = {
          "username": self._username,
          "password": self._password
        }

        await self._session.post(url, json=payload, raise_for_status=True)

    async def set_cmd(self, serial, payload):
        url = f"{URL}/api/devices/{serial}/set"
        r = await self._session.post(url, json=payload, raise_for_status=True)
        return await r.json()

    async def get_device_types(self):
        url = f"{URL}/api/lists/devicetypes"

        r = await self._session.get(url, raise_for_status=True)
        return await r.json()

    async def get_producers(self):
        url = f"{URL}/api/lists/producers"

        r = await self._session.get(url, raise_for_status=True)
        return await r.json()

    async def get_devices(self, **kwargs):
        url = f"{URL}/api/devices"
        # valid params are:
        # filterconnect=<online|offline>
        # filterproducent=str
        # filterdevicetype=str

        r = await self._session.get(url, params=kwargs, raise_for_status=True)
        return await r.json()

    async def get_device(self, serial):
        url = f"{URL}/api/devices/{serial}"

        r = await self._session.get(url, raise_for_status=True)
        return await r.json()

    async def get_live(self, serial):
        url = f"{URL}/api/devices/{serial}/live"

        r = await self._session.get(url, raise_for_status=True)
        return await r.json()

    async def get_alerts(self):
        url = f"{URL}/api/alerts/count"

        r = await self._session.get(url, raise_for_status=True)
        return await r.json()
