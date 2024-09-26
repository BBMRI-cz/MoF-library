import abc


class SampleDonorRepository(abc.ABC):
    """"Class for handling sample donor persistence.
        This is an abstract class, as the concrete implementation is up to the user to define"""

    @abc.abstractmethod
    def get_all(self):
        """Get all sample donors."""

