from abc import ABC, abstractmethod


class Operator(ABC):
    @abstractmethod
    def process(self, left, right):
        pass

    @abstractmethod
    def valid_for_left(self, value) -> bool:
        pass

    @abstractmethod
    def valid_for_right(self, value) -> bool:
        pass


class NumericOperator(Operator):
    def valid_for_left(self, value) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def valid_for_right(self, value) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False


class Expression(ABC):
    @abstractmethod
    def evaluate(self):
        pass
