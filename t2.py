import functools


@functools.total_ordering
class Version:
    def __init__(self, version):
        self.version = version

    def process_version(self):
        new_version = self.version
        new_dict = {
            'alpha': "1",
            "beta": "2",
            "b": ".2",
            "rc": "3",
            "-": "."
        }
        for i in new_dict:
            new_version = new_version.replace(i, new_dict[i])
        return tuple(int(i) for i in new_version.split("."))

    def __eq__(self, other):
        return self.process_version() == other.process_version()

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        first = self.process_version()
        second = other.process_version()
        if first[0] == second[0] and first[1] == second[1] and first[2] == second[2]:
            l1 = len(self.process_version())
            l2 = len(other.process_version())
            if l2 < l1:
                return True
            elif l2 > l1:
                return False
        return self.process_version() < other.process_version()


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
