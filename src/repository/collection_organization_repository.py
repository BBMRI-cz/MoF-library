import abc


class CollectionOrganizationRepository(abc.ABC):
    """Class for handling CollectionOrganization persistence,
        this is an abstract class, as the concrete implementation is up to the user to define"""

    @abc.abstractmethod
    def get_all(self):
        """Get all collection organizations."""