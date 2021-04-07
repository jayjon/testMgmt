import unittest

from EasyTest.demo import add


class TestGw(unittest.TestCase):

    def test_add(self):
        res = add("测试", 1)
        print(res)
        self.assertEqual("true", res)

    def test_add_1(self):
        res = add('', 1)
        print(res)
        self.assertEqual("true", res)

    @unittest.skip("跳过")
    def test_add_2(self):
        res = add("", 1)
        print(res)
        self.assertEqual("a", res)

    @unittest.skip("跳过")
    def test_add_3(self):
        res = add(None, 1)
        print(res)
        self.assertEqual("a", res)


if __name__ == '__main__':
    unittest.main()
