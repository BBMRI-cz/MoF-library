import abc


class DiagnosisReportRepository(abc.ABC):
    """Class for handling DiagnosisReport persistence,
        this is an abstract class, as the concrete implementation is up to the user to define"""

    @abc.abstractmethod
    def get_all(self):
        """Get all diagnosis reports."""