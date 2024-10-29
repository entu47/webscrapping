from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass


class ConsoleNotification(NotificationStrategy):
    def notify(self, message: str):
        print(message)
