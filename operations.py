import logging
import operator

logging.basicConfig(filename='operations.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')


class Operations(object):
    """
    Class intended to perform arithmetic operations received from a bytes
    string and return the correct result.
    """

    OPS = {'+': operator.add, '-': operator.sub, '*': operator.mul,
           '/': operator.truediv}

    def __init__(self):
        """
        Operations class cunstructor.
        """

        pass

    def operate(self, operation, operations, numbers):
        """
        It does the arithmetic operation received by operation parameter,
        remove the numbers used on the numbers list, inserts the result in
        the correct position of numbers list and remove the operation done in
        the operations list.

        :param operation: Operation to be done.
        :type operation: operator
        :param operations: List of operations pending.
        :type operations: list
        :param numbers: List of numbers pending.
        :type numbers: list
        :return: Tuple of operations and numbers.
        :rtype: tuple
        """

        operation_index = operations.index(operation)
        numbers.insert(operation_index, operation(numbers.pop(
            operation_index), numbers.pop(operation_index)))
        operations.pop(operation_index)
        return operations, numbers

    def split_numbers_operators(self, line):
        """
        It decodes the bytestring received to utf-8 and splits it in two
        different lists. One with operations and the other one with numbers.

        :param line: Bytes string with the inccoming operation.
        :type line: bytes
        :return: Tuple of two lists.
        :rtype: tuple
        """

        numbers = []
        operations = []
        input_list = line.decode('utf-8').split()

        for element in input_list:
            try:
                numbers.append(int(element))
            except ValueError as e:
                try:
                    operations.append(self.OPS[element])
                except KeyError as e:
                    break

        return operations, numbers

    def calculate(self, operations, numbers):
        """
        It decides which is the next operation to be done and calls the
        operate methed with it.

        :param operations: List of operations pending.
        :type operations: list
        :param numbers: List of numbers pending.
        :type numbers: list
        :return: The result of the operations.
        :rtype: int or float
        """

        while self.OPS['*'] in operations or self.OPS['/'] in operations:
            if self.OPS['*'] in operations and self.OPS['/'] in operations:
                operation = operations[min(operations.index(self.OPS['*']),
                                           operations.index(self.OPS['/']))]
                operations, numbers = self.operate(operation, operations,
                                                   numbers)
            elif self.OPS['*'] in operations:
                operations, numbers = self.operate(self.OPS['*'],
                                                   operations, numbers)
            elif self.OPS['/'] in operations:
                operations, numbers = self.operate(self.OPS['/'],
                                                   operations, numbers)

        while self.OPS['+'] in operations or self.OPS['-'] in operations:
            operations, numbers = self.operate(operations[0], operations,
                                               numbers)

        return numbers[0]

    def main(self, data):
        """
        It receives a bytestring with an operation and returns the result. If
        the parameter has not a correct bunch of operations it returns an error
        message.

        :param data: Bytes string with operations to be done.
        :type data: bytes
        :return: Either the result in bytes string or an error message.
        :rtype: bytes
        """

        if data:
            operations, numbers = self.split_numbers_operators(data)

            if len(numbers) > 0:
                result = self.calculate(operations, numbers)
                logging.debug('{} = {}'.format(data.decode('utf-8'), result))
                return bytes(str(result), 'utf-8')
            else:
                logging.warning('Not a valid operation: {}'.format(data))
                return b'This is not a valid operation!'
