import abc


class CollectionRepository(abc.ABC):
    """Class for handling Collection persistence,
        this is an abstract class, as the concrete implementation is up to the user to define"""

    @abc.abstractmethod
    def get_all(self):
        """Get all collections."""