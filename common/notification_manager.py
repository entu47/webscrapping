import logging
from abc import ABC, abstractmethod
logger = logging.getLogger(__name__)


class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass


class ConsoleNotification(NotificationStrategy):
    def notify(self, message: dict):
        logger.info(message)
