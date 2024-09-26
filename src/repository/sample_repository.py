import abc


class SampleRepository(abc.ABC):
    """Class for handling sample persistence.
        This is an abstract class, as the concrete implementation is up to the user to define"""

    @abc.abstractmethod
    def get_all(self):
        """Get all samples."""
