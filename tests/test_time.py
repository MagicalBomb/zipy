import datetime

from pytest import raises

from zipy.time import complete_timeseries, time_range


class TestTimeRange:
    def test_normal_case(self):
        start = datetime.datetime(year=2022, month=1, day=1)
        end = datetime.datetime(year=2022, month=1, day=8)

        res = []
        for t in time_range(start, end, datetime.timedelta(days=2)):
            res.append(t)

        assert len(res) == 4
        assert res[0] == datetime.datetime(2022, 1, 1)
        assert res[1] == datetime.datetime(2022, 1, 3)
        assert res[2] == datetime.datetime(2022, 1, 5)
        assert res[3] == datetime.datetime(2022, 1, 7)

    def test_start_end_equal(self):
        start = datetime.datetime(2022, 1, 5)
        end = start

        res = []
        for t in time_range(start, end, datetime.timedelta(days=2)):
            res.append(t)

        assert len(res) == 0

    def test_start_gt_end(self):
        start = datetime.datetime(2022, 1, 4)
        end = datetime.datetime(2022, 1, 2)

        res = []
        for t in time_range(start, end, datetime.timedelta(days=2)):
            res.append(t)

        assert len(res) == 0

    def test_step_is_0(self):
        with raises(ValueError):
            for _ in time_range(
                datetime.datetime(2022, 1, 1),
                datetime.datetime(2022, 1, 3),
                datetime.timedelta(),
            ):
                ...


class TestCompleteTimeseries:
    def test_normal_case(self):
        lst = [
            {"v": 1, "t": datetime.datetime(2022, 1, 1)},
            {"v": 3, "t": datetime.datetime(2022, 1, 3)},
            {"v": 5, "t": datetime.datetime(2022, 1, 5)},
        ]

        def write_time(o, dt):
            o["t"] = dt

        def write_other(o, pre):
            o["v"] = pre["v"] + 1

        res = complete_timeseries(
            lst=lst,
            read_time=lambda o: o["t"],
            write_time=write_time,
            write_other=write_other,
            step=datetime.timedelta(days=1),
        )

        assert len(res) == 5
        for i in range(1, 6):
            assert res[i - 1] == {"v": i, "t": datetime.datetime(2022, 1, i)}

    def test_over_end(self):
        lst = [
            {"v": 1, "t": datetime.datetime(2022, 1, 1)},
            {"v": 3, "t": datetime.datetime(2022, 1, 3)},
            {"v": 6, "t": datetime.datetime(2022, 1, 6)},
        ]

        def write_time(o, dt):
            o["t"] = dt

        def write_other(o, pre):
            o["v"] = pre["v"] + 1

        res = complete_timeseries(
            lst=lst,
            read_time=lambda o: o["t"],
            write_time=write_time,
            write_other=write_other,
            step=datetime.timedelta(days=2),
        )

        assert len(res) == 3
        assert res[0] == {"v": 1, "t": datetime.datetime(2022, 1, 1)}
        assert res[1] == {"v": 3, "t": datetime.datetime(2022, 1, 3)}
        assert res[2] == {"v": 4, "t": datetime.datetime(2022, 1, 5)}
