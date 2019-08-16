from sub_a import subA


class A:

    attrA = subA()

    @classmethod
    def create_subA(cls):
        return subA()
