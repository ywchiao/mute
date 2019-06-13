
class S:
    def __init__(self):
        print('this is s')

class T(S):
    def hello(self):
        print('hello from T')

class U(S):
    def __init__(self):
        super().__init__()
        print('this is U')


class V(S):
    def __init__(self):
        print('this is V')


S()
T()
U()
V()
