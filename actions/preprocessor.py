from sentence_transformers import SentenceTransformer, util
import yaml
import torch

class SemanticInputNormalizer:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.intent_examples = []  # Load your actual intent examples from nlu.yml

    def get_best_match(self, user_input: str) -> str:
        """Finds the closest matching intent example for the user input."""
        if not user_input:
            return "Sorry, I didn't understand that."

        user_embedding = self.model.encode(user_input, convert_to_tensor=True)

        # Ensure intent_examples is not empty
        if not self.intent_examples:
            return user_input  # Return original input if no training examples

        # Encode intent examples
        intent_embeddings = self.model.encode(self.intent_examples, convert_to_tensor=True)

        # Compute similarity
        cosine_scores = torch.nn.functional.cosine_similarity(user_embedding, intent_embeddings)
        best_match_idx = torch.argmax(cosine_scores).item()

        return self.intent_examples[best_match_idx]  # Return the best match

# Example Usage
if __name__ == "__main__":
    normalizer = SemanticInputNormalizer("../data/nlu.yml")  # Load NLU training data
    user_input = "How to reach hostel?"
    normalized_input = normalizer.get_best_match(user_input)
    print("Normalized Input:", normalized_input)
