import aiohttp
import asyncio
from loguru import logger
from aiohttp.typedefs import StrOrURL
from typing import Type, Callable, Optional, Any, Coroutine

__all__ = ("HoMuraSession", )


class HoMuraSession:
    def __init__(
            self, client_session: Type[aiohttp.ClientSession], *, retry_time: int = 3,
            retry_interval: Optional[int] = None, retry_when: Optional[Callable] = None,
            exception_class: Optional[Any] = None, exception_kwargs: Optional[dict] = None
    ):
        self.client_session = client_session
        self.retry_time = retry_time
        self.retry_interval = retry_interval
        self.retry_when = retry_when
        self.exception_class = exception_class
        self.exception_kwargs = exception_kwargs

    async def request(
        self, method: str, url: StrOrURL, /, *, func: Callable, **kwargs
    ):
        async with self.client_session() as session:
            last_error = Exception("")
            for i in range(self.retry_time):
                try:
                    res = await session.request(method.upper(), url, **kwargs)
                    break
                except Exception as _e:
                    if self.exception_class is None or self.exception_class is Exception:
                        last_error = _e
                    else:
                        last_error = self.exception_class(
                            "error message: {}".format(repr(_e)), **self.exception_kwargs or {}
                        )
                    if self.retry_when and not self.retry_when(_e):
                        raise last_error
                    logger.error("retry to request url: {}, method: {}, now request time: {}".format(
                        url, method, i + 1
                    ))
                    if self.retry_interval is not None:
                        await asyncio.sleep(self.retry_interval)
                    continue
            else:
                raise last_error
            call_result = func(res)
            if isinstance(call_result, Coroutine):
                result = await call_result
            else:
                result = call_result
        return result

    async def get(self, url: StrOrURL, *, func: Callable, allow_redirects: bool = True, **kwargs):
        return await self.request('get', url, func=func, allow_redirects=allow_redirects, **kwargs)

    async def post(self, url: StrOrURL, *, func: Callable, data: Any = None, **kwargs):
        return await self.request('post', url, func=func, data=data, **kwargs)

    async def put(self, url: StrOrURL, *, func: Callable, data: Any = None, **kwargs):
        return await self.request('put', url, func=func, data=data, **kwargs)

    async def delete(self, url: StrOrURL, *, func: Callable, **kwargs):
        return await self.request('delete', url, func=func, **kwargs)


async def main():
    class D:
        def __init__(self, c: str):
            self.c = c

        async def callback(self, res: aiohttp.ClientResponse):
            print(self.c)
            return await res.text()

    url = "http://localhost:8088/test"
    session = HoMuraSession(
        aiohttp.ClientSession, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
    )
    r = await session.get(url, func=D("10").callback, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/99.0.4844.51 Safari/537.36"
    }, ssl=False, timeout=3)
    print(r)


if __name__ == '__main__':
    asyncio.run(main())
