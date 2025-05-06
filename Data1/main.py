import time
from functools import wraps


def rate_limit(min_interval_seconds):
    def decorator(func):
        last_called = [0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            elapsed = now - last_called[0]
            if elapsed >= min_interval_seconds:
                last_called[0] = now
                return func(*args, **kwargs)
            else:
                print(f"function locked for {round(min_interval_seconds - elapsed)}s")

        return wrapper

    return decorator


def up1(x):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*tuple(arg + x for arg in args), **kwargs)

        return wrapper

    return decorator


@rate_limit(2)
def testfunc():
    print(f"time NOW: {time.strftime('%X')}")


@up1(3)
def testfunc2(x, y):
    print(f"x + y = {x + y:.2f}")


if __name__ == '__main__':

    start_time = time.time()
    while time.time() - start_time < 6:
        testfunc()
        time.sleep(1)

    testfunc2(2.5, 3)
