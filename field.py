FIELD_SIZE = (
    21888242871839275222246405745257275088548364400416034343698204186575808495617
)


class Field:
    def __init__(self, val):
        self.val = val % FIELD_SIZE

    def __add__(self, other):
        return Field(self.val + other.val)

    def __mul__(self, other):
        return Field(self.val * other.val)

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return self.val == other.val
