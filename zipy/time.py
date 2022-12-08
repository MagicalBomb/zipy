import datetime


__all__ = ["time_range"]


def time_range(
    start: datetime.datetime, end: datetime.datetime, step: datetime.timedelta
):
    """
    :raise ValueError: raises if step is timedelta(0, 0, 0, 0, 0, 0)
    :return: an iterable object with time points within the [start, end) interval with a step of 'step'
    """
    if step == datetime.timedelta():
        raise ValueError("step can't be timedelta(0)")
    current = start
    while current < end:
        yield current
        current = current + step
