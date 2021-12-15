import functools


@functools.total_ordering
class Version:
    _suffixes = {
        "alpha": "1",
        "beta": "2",
        "b": ".2",
        "rc": "3",
        "-": ".",
        "release": ".5"
    }

    def __init__(self, version):
        self.version = version

    @functools.cached_property
    def as_tuple(self):
        new_version = self.version
        flag = False

        for i in self._suffixes:
            if new_version.find(i) != -1:
                flag = True
                new_version = new_version.replace(i, self._suffixes[i])

        if not flag:
            new_version += self._suffixes.get("release")
        return tuple(int(i) for i in new_version.split("."))

    def __eq__(self, other):
        return self.as_tuple is other.as_tuple

    def __lt__(self, other):
        return self.as_tuple < other.as_tuple


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0-alpha.beta", "1.0.0-beta"),
        ("1.0.0-beta.11", "1.0.0-rc.1")
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()