

class A:
    def __init__(self):
        print("Constructor of A")

class B(A):
    def __init__(self):
        super().__init__()
        print("Constructor of B")

class C(B):
    def __init__(self):
        super().__init__()
        print("Constructor of C")

obj = C()
