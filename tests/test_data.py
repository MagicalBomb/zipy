from zipy.data import dict_get


class TestDictGet:
    def test(self):
        d = {"a": {"b": {"c": 123}}}
        assert dict_get(d, "a", "b") == {"c": 123}
        assert dict_get(d, "a", "b", "c") == 123
        assert dict_get(d, "a", "b", "c", "d") is None
        assert dict_get(d, "a", "b", "c", "d", default=321) == 321
        assert dict_get(d, default=None) == d
