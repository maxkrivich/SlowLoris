import jk_triologging


class Logger:

    def __init__(self):
        self._log = jk_triologging.TrioConsoleLogger.create()

    async def debug(self, *args, **kwargs):
        await self._log.debug(*args, **kwargs)

    async def info(self, *args, **kwargs):
        await self._log.info(*args, **kwargs)

    async def error(self, *args, **kwargs):
        await self._log.error(*args, **kwargs)

    async def warn(self, *args, **kwargs):
        await self._log.warn(*args, **kwargs)


log = Logger()
