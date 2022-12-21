import contextlib
import time
from pytest import raises
from zipy.retry import retry


class TestRetryFunc:
    async def test_paramter_check(self):
        retry(wait=888)
        retry(wait=1)
        retry(wait=0)
        with raises(ValueError):
            retry(wait=-1)

        async def co_f():
            ...

        async def asyn_gen_f():
            yield

        def normal_f():
            ...

        retry(times=888, wait=0.3)(co_f)
        retry(times=11, wait=3.2)(normal_f)
        with raises(ValueError):
            retry(times=1, wait=1)(asyn_gen_f)

        with raises(TypeError):
            retry(exceptions=Exception)

    async def test_paramter_wait(self):
        def func():
            raise KeyError

        start = time.time()
        with contextlib.suppress(Exception):
            # 重试 3 次， 只会等待 2 次
            # 因为 3 次也失败的话，会直接抛出异常
            retry(times=3, wait=0.1)(func)()
        elasped = time.time() - start
        assert elasped > 0.2

        async def func():
            raise KeyError

        start = time.time()
        with contextlib.suppress(Exception):
            # 重试 3 次， 只会等待 2 次
            # 因为第 3 次也失败的话，会直接抛出异常
            await retry(times=3, wait=0.1)(func)()
        elasped = time.time() - start
        assert elasped > 0.2

    async def test_paramter_exceptions(self):
        # Normal func
        def func():
            raise TabError

        start = time.time()
        with contextlib.suppress(Exception):
            # 重试 3 次， 只会等待 2 次
            # 因为 3 次也失败的话，会直接抛出异常
            retry(times=3, wait=0.1, exceptions=[KeyError])(func)()
        elasped = time.time() - start
        assert elasped < 0.1

        start = time.time()
        with contextlib.suppress(Exception):
            # 重试 3 次， 只会等待 2 次
            # 因为 3 次也失败的话，会直接抛出异常
            retry(times=3, wait=0.1, exceptions=[TabError])(func)()
        elasped = time.time() - start
        assert elasped > 0.2

        # Async func
        async def func():
            raise TabError

        start = time.time()
        with contextlib.suppress(Exception):
            # 重试 3 次， 只会等待 2 次
            # 因为 3 次也失败的话，会直接抛出异常
            await retry(times=3, wait=0.1, exceptions=[KeyError])(func)()
        elasped = time.time() - start
        assert elasped < 0.1

        start = time.time()
        with contextlib.suppress(Exception):
            # 重试 3 次， 只会等待 2 次
            # 因为 3 次也失败的话，会直接抛出异常
            await retry(times=3, wait=0.1, exceptions=[TabError])(func)()
        elasped = time.time() - start
        assert elasped > 0.2

    async def test_with_normal_func(self):
        count = 1

        def func():
            nonlocal count
            if count < 3:
                count += 1
                raise KeyError("count < 3")
            else:
                return

        func_ = retry(times=2, wait=0.1)(func)
        with raises(KeyError):
            func_()

        func_ = retry(times=3, wait=0.1)(func)
        func_()

        # test if times < 0 works
        count = 0

        def func():
            nonlocal count
            if count < 100:
                count += 1
                raise KeyError("count < 100")

        func_ = retry(times=0, wait=0)(func)
        func_()

    async def test_with_async_func(self):
        count = 1

        async def func():
            nonlocal count
            if count < 3:
                count += 1
                raise KeyError("count < 3")
            else:
                return

        func_ = retry(times=2, wait=0.1)(func)
        with raises(KeyError):
            await func_()

        func_ = retry(times=3, wait=0.1)(func)
        await func_()

        # test if times < 0 works
        count = 0

        async def func():
            nonlocal count
            if count < 100:
                count += 1
                raise KeyError("count < 100")

        func_ = retry(times=0, wait=0)(func)
        await func_()
