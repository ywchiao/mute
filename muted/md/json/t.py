


def test(k):
    try:
        k = cache[k]
    except KeyError:
        pass

    return k

cache = {
    "b": "1",
    "c": "2"
}

print(test("b"))
print(test("d"))

