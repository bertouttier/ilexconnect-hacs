import aiohttp

from asyncio import gather
from async_timeout import timeout
from http import HTTPStatus
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .ilexconnect import ILexConnectApi
from .const import API_TIMEOUT, DOMAIN, UPDATE_INTERVAL, LOGGER, API_SRN

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass, config_entry):
    """Set up Awair integration from a config entry."""
    session = async_get_clientsession(hass)
    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]
    api = ILexConnectApi(hass, username, password, session=session)
    try:
        await api.login()
    except aiohttp.ClientResponseError as loginex:
        if loginex.status == HTTPStatus.FORBIDDEN:
            raise ConfigEntryAuthFailed from loginex
    coordinator = ILexDataUpdateCoordinator(hass, api, config_entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass, config_entry):
    """Unload Awair configuration."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


class ILexDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, api, config_entry):
        self._api = api
        self._config_entry = config_entry
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def _async_update_data(self):
        async with timeout(API_TIMEOUT):
            try:
                LOGGER.debug("Fetching devices")
                devices = await self._api.get_devices(filterproducent="oceanic", filterdevicetype="Smart")
                LOGGER.debug(devices)
                await gather(
                    *(self._api.set_cmd(device["serial"], {"command": "setRCE", "deviceid": device["serial"], "value": device["enduser_extend"]["id"]}) for device in devices["results"])
                )
                results = await gather(
                    *(self._api.get_live(device["serial"]) for device in devices["results"])
                )
                LOGGER.debug(results)
                return {result[API_SRN]: result for result in results if API_SRN in result}
            except aiohttp.ClientResponseError as ex:
                if ex.status == HTTPStatus.UNAUTHORIZED:
                    LOGGER.debug("Failed to fetch data due to login expired. Logging in...")
                    try:
                        await self._api.login()
                    except aiohttp.ClientResponseError as loginex:
                        if loginex.status == HTTPStatus.FORBIDDEN:
                            raise ConfigEntryAuthFailed from loginex
                        raise UpdateFailed(loginex) from loginex
                raise UpdateFailed(ex) from ex
            except Exception as err:
                raise UpdateFailed(err) from err