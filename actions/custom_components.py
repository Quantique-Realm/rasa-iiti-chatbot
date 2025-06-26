from rasa.engine.graph import GraphComponent
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from typing import Dict, Text, Any, List
from actions.preprocessor import SemanticInputNormalizer

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER, is_trainable=False
)
class SemanticInputNormalizerComponent(GraphComponent):
    """
    Custom Rasa NLU component that preprocesses user input by normalizing it to
    the closest intent example from `nlu.yml` using SBERT-based semantic matching.
    """

    def __init__(self, config: Dict[Text, Any], model_storage: ModelStorage, resource: Resource) -> None:
        super().__init__()
        self.normalizer = SemanticInputNormalizer()

    def process(self, messages: List[Message]) -> List[Message]:
        """
        Processes a list of messages by normalizing their text.

        :param messages: List of incoming messages.
        :return: Modified messages.
        """
        for message in messages:
            original_text = message.get("text")
            normalized_text = self.normalizer.get_best_match(original_text)
            message.set("text", normalized_text, add_to_output=True)
        return messages

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """
        Ensures training data is normalized before model training.

        :param training_data: The training dataset.
        :return: Processed training dataset with normalized text.
        """
        for example in training_data.training_examples:
            original_text = example.get("text")
            normalized_text = self.normalizer.get_best_match(original_text)
            example.set("text", normalized_text)
        return training_data

    @classmethod
    def create(
        cls, config: Dict[Text, Any], model_storage: ModelStorage, resource: Resource, execution_context: Any
    ) -> "SemanticInputNormalizerComponent":
        return cls(config, model_storage, resource)
