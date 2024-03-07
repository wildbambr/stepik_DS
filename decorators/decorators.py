import time
from functools import wraps, lru_cache
import typing


# Такая структура декоратора нужна для того, чтобы при
# декорировании рекурсивной функции время вызова считалось для
# всей работы в целом, а не для каждого вызова отдельно
def benchmark(func: typing.Callable):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if wrapper.depth == 0:
            wrapper.start_time = time.time()

        wrapper.depth += 1
        res = func(*args, **kwargs)
        wrapper.depth -= 1
        if wrapper.depth <= 0:
            print(f"Время выполнения функции {func.__name__}: {time.time() - wrapper.start_time}")
            wrapper.start_time = None
        return res

    wrapper.depth = 0  # Глубина рекурсии, если декорируется рекурсивная функция

    return wrapper


# Такая структура декоратора нужна для того, чтобы при
# декорировании рекурсивной функции отображались только параметры,
# передаваемые при первом вызове, а не при каждом
def logging(func: typing.Callable):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if wrapper.depth == 0:
            wrapper.args = args
            wrapper.kwargs = kwargs

        wrapper.depth += 1
        res = func(*args, **kwargs)
        wrapper.depth -= 1

        if wrapper.depth <= 0:
            print(f"Функция вызвана с параметрами:\n{wrapper.args}, {wrapper.kwargs}")
            wrapper.args = None
            wrapper.kwargs = None
        return res

    wrapper.depth = 0

    return wrapper


# Такая структура декоратора нужна для того, чтобы при
# декорировании рекурсивной функции количество вызовов считалось для
# всей работы в целом, а не для каждого вызова отдельно
def counter(func: typing.Callable):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if wrapper.depth == 0:
            wrapper.calls = 0

        wrapper.depth += 1
        wrapper.calls += 1
        res = func(*args, **kwargs)
        wrapper.depth -= 1

        if wrapper.depth <= 0:
            print(f'Функция была вызвана: {wrapper.calls} раз')
            wrapper.calls = 0

        return res

    wrapper.depth = 0

    return wrapper


def memo(func: typing.Callable):
    """
    Декоратор, запоминающий результаты исполнения функции func
    """
    @wraps(func)
    @lru_cache
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return wrapper
