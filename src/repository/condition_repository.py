import abc


class ConditionRepository(abc.ABC):
    """Class for handling Condition persistence"""

    @abc.abstractmethod
    def get_all(self) -> List[Condition]:
        """Get all conditions."""