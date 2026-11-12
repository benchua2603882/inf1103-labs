import math
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        # Each discount works out the new total in its own way.
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        # Leave the total unchanged when no discount is selected.
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        # A percentage outside this range would give an invalid discount.
        if (type(percentage) not in (int, float)
                or not math.isfinite(percentage) or not 0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        # Take the chosen percentage off the original total.
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        # Both values must be valid before we store them.
        if (type(threshold) not in (int, float)
                or not math.isfinite(threshold) or threshold < 0):
            raise ValueError("Threshold must be a finite, non-negative number.")
        if (type(amount) not in (int, float)
                or not math.isfinite(amount) or amount < 0):
            raise ValueError("Discount amount must be a finite, non-negative number.")
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def apply(self, total: float) -> float:
        # Apply the discount only when the order reaches the threshold.
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total


class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        # Students get 5% off without changing the Order class.
        return total * 0.95
