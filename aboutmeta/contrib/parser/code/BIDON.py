from pprint import pprint

def test(data):
    def f1():
        print(f"String: {data}")

    def f2():
        print(f"Dict: {data}")

    if isinstance(dict, str):
        f1()

    else:
        data = {"f": 0}
        f2()

test("text")
test({"key": 'val'})
