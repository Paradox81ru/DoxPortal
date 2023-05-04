class MetaSingleton(type):
    """
    Метакласс синглтона.

    class MyClass(BaseClass, metaclass=Singleton):
        pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # else:
        #     cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class BaseSingleton(object):
    """
    Базовый класс для синглтона.

    class MyClass(BaseSingleton, BaseClass):
        pass
    """
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


def singleton(class_):
    """
    Декоратор синглтона

    @singleton
    class MyClass(BaseClass):
        pass

    :param class_:
    :return:
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        # else:
        #     instances[class_].__init__(*args, **kwargs)
        return instances[class_]
    return getinstance


class TestClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def plus(self):
        return self.a + self.b

    def minus(self):
        return self.a - self.b


def tests_meta_singleton():
    class TestSingleton(TestClass, metaclass=MetaSingleton):
        def divide(self):
            return self.a / self.b

    print("Test meta singleton:")
    print("")
    test_meta_singleton1 = TestSingleton(10, 5)
    print("test_meta_singleton1 = TestSingleton(10, 5)")
    print("test_meta_singleton1.a =", test_meta_singleton1.a, "test_meta_singleton1.b =", test_meta_singleton1.b)
    print("test_singleton1_minus:", test_meta_singleton1.minus())
    print("test_singleton1_divide:", test_meta_singleton1.divide())

    print("")
    test_meta_singleton2 = TestSingleton(30, 10)
    print("test_meta_singleton2 = TestSingleton(30, 10)")
    print("test_meta_singleton2.a =", test_meta_singleton2.a, "test_meta_singleton2.b =", test_meta_singleton2.b)
    print("test_meta_singleton1.a =", test_meta_singleton1.a, "test_meta_singleton1.b =", test_meta_singleton1.b)
    print("test_singleton2_minus:", test_meta_singleton2.minus())
    print("test_singleton2_divide:", test_meta_singleton2.divide())
    print("")
    print("test_meta_singleton1 is test_meta_singleton2", test_meta_singleton1 is test_meta_singleton2)
    print("-------------------------------")


def test_base_singleton():
    class TestSingleton(BaseSingleton, TestClass):
        def multiply(self):
            return self.a * self.b

    print("Test base singleton:")
    print("")
    test_base_singleton1 = TestSingleton(5, 2)
    print("test_base_singleton1 = TestSingleton(5, 2)")
    print("test_base_singleton1.a =", test_base_singleton1.a, "test_base_singleton1.b =", test_base_singleton1.b)
    print("test_singleton1_plus:", test_base_singleton1.plus())
    print("test_singleton1_multiply:", test_base_singleton1.multiply())

    print("")
    test_base_singleton2 = TestSingleton(8, 5)
    print("test_base_singleton2 = TestSingleton(8, 5)")
    print("test_base_singleton2.a =", test_base_singleton2.a, "test_base_singleton2.b =", test_base_singleton2.b)
    print("test_base_singleton1.a =", test_base_singleton1.a, "test_base_singleton1.b =", test_base_singleton1.b)
    print("test_singleton2_plus:", test_base_singleton2.plus())
    print("test_singleton2_multiply:", test_base_singleton2.multiply())
    print("")
    print("test_base_singleton1 is test_base_singleton2", test_base_singleton1 is test_base_singleton2)
    print("-------------------------------")


def test_decorator_singleton():
    @singleton
    class TestSingleton(TestClass):
        def remainder(self):
            return self.a % self.b

    print("Test decorator singleton:")
    print("")
    test_decorator_singleton1 = TestSingleton(25, 12)
    print("test_decorator_singleton1 = TestSingleton(25, 12)")
    print("test_decorator_singleton1.a =", test_decorator_singleton1.a,
          "test_decorator_singleton1.b =", test_decorator_singleton1.b)
    print("test_singleton1_plus:", test_decorator_singleton1.plus())
    print("test_singleton1_remainder:", test_decorator_singleton1.remainder())

    print("")
    test_decorator_singleton2 = TestSingleton(18, 8)
    print("test_base_singleton2 = TestSingleton(18, 8)")
    print("test_decorator_singleton2.a =", test_decorator_singleton2.a,
          "test_decorator_singleton2.b =", test_decorator_singleton2.b)
    print("test_decorator_singleton1.a =", test_decorator_singleton1.a,
          "test_decorator_singleton1.b =", test_decorator_singleton1.b)
    print("test_singleton2_plus:", test_decorator_singleton2.plus())
    print("test_singleton2_remainder:", test_decorator_singleton2.remainder())
    print("")
    print("test_decorator_singleton1 is test_decorator_singleton2", test_decorator_singleton1 is test_decorator_singleton2)
    print("-------------------------------")


if __name__ == "__main__":
    tests_meta_singleton()
    test_base_singleton()
    test_decorator_singleton()
