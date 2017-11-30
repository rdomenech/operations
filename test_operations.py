import operator
import unittest

from operations import Operations


class TestOperations(unittest.TestCase):
    """docstring for TestOperations"""

    def test_operate_add(self):

        operations = [operator.add]
        numbers = [1, 2]
        blueliv = Operations()
        operations, result = blueliv.operate(operator.add, operations, numbers)
        self.assertEqual(operations, [])
        self.assertEqual(result[0], 3)

    def test_operate_subtract(self):

        operations = [operator.sub]
        numbers = [1, 2]
        blueliv = Operations()
        operations, result = blueliv.operate(operator.sub, operations, numbers)
        self.assertEqual(operations, [])
        self.assertEqual(result[0], -1)

    def test_operate_multiply(self):

        operations = [operator.mul]
        numbers = [1, 2]
        blueliv = Operations()
        operations, result = blueliv.operate(operator.mul, operations, numbers)
        self.assertEqual(operations, [])
        self.assertEqual(result[0], 2)

    def test_operate_divide(self):

        operations = [operator.truediv]
        numbers = [1, 2]
        blueliv = Operations()
        operations, result = blueliv.operate(operator.truediv, operations,
                                             numbers)
        self.assertEqual(operations, [])
        self.assertEqual(result[0], 0.5)

    def test_calculate(self):

        input_string = b'26 * 99 - 37 * 38 + 50 + 48 / 45 + 90 + 22 - 44'
        blueliv = Operations()
        self.assertEqual(blueliv.main(input_string), b'1287.0666666666666')


if __name__ == '__main__':
    unittest.main()
