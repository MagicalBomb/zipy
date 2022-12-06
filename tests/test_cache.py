import asyncio
import time
from zipy.cache import cache


class TestCache:
    def test_normal_func(self):
        @cache(ttl=0.2)
        def func():
            time.sleep(0.2)
            return 112233

        starttime = time.time()
        assert func() == 112233
        elapsedtime = time.time() - starttime
        assert elapsedtime > 0.1

        starttime = time.time()
        assert func() == 112233
        elapsedtime = time.time() - starttime
        assert elapsedtime < 0.1

        time.sleep(0.2)
        starttime = time.time()
        assert func() == 112233
        elapsedtime = time.time() - starttime
        assert elapsedtime > 0.1

    async def test_coroutine_func(self):
        @cache(ttl=0.2)
        async def func():
            await asyncio.sleep(0.1)
            return 112233

        starttime = time.time()
        assert (await func()) == 112233
        elapsedtime = time.time() - starttime
        assert elapsedtime > 0.1

        starttime = time.time()
        assert (await func()) == 112233
        elapsedtime = time.time() - starttime
        assert elapsedtime < 0.1

        await asyncio.sleep(0.2)
        starttime = time.time()
        assert (await func()) == 112233
        elapsedtime = time.time() - starttime
        assert elapsedtime > 0.1

    async def test_asyncgen_func(self):
        @cache(ttl=0.2)
        async def func():
            await asyncio.sleep(0.1)
            for i in range(3):
                yield i

        starttime = time.time()
        lst = []
        async for ele in func():
            lst.append(ele)
        assert lst == [0, 1, 2]
        elaspedtime = time.time() - starttime
        assert elaspedtime > 0.1

        starttime = time.time()
        lst = []
        async for ele in func():
            lst.append(ele)
        assert lst == [0, 1, 2]
        elaspedtime = time.time() - starttime
        assert elaspedtime < 0.1

        await asyncio.sleep(0.2)
        starttime = time.time()
        lst = []
        async for ele in func():
            lst.append(ele)
        assert lst == [0, 1, 2]
        elaspedtime = time.time() - starttime
        assert elaspedtime > 0.1
