from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract for objects that support shipping."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this object."""
        # Each class using this interface must supply its own calculation.
        pass
