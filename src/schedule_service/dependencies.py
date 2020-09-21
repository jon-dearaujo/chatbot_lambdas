from abc import ABC, abstractmethod
from src.persistent_data import PersistentData


class ResponseBuilder(ABC):
    'Base class for creating chatbot responses'
    @abstractmethod
    def ask_for_input(self, intent_name, slots, slot_to_elicit, message, session_attributes: PersistentData):
        pass

    @abstractmethod
    def confirm_inputs(self, intent_name, slots, message, session_attributes: PersistentData):
        pass

    @abstractmethod
    def notify_completion(self, is_complete, message, session_attributes: PersistentData):
        pass
