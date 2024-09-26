import abc


class BiobankRepository(abc.ABC):
    """Class for handling Biobank persistence,
        this is an abstract class, as the concrete implementation is up to the user to define"""

    @abc.abstractmethod
    def get_all(self):
        """Get all biobanks."""
