import local_tokens
from transformers import pipeline
import langchain
langchain.verbose = False
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


# Your Hugging Face API token
huggingface_token = local_tokens.api_keys()["HF"]["INIT_READ"]

# Initialize the model pipeline
model_name = "gpt2"  # or any other suitable model
question_generator = pipeline('text-generation', model=model_name, token=huggingface_token)

# Set up LangChain
prompt = langchain.prompts.FixedPrompt("Generate logical and coding questions based on the following text:")
postprocessor = langchain.postprocessors.QuestionPostprocessor()

chain = langchain.prompts.langchain.chains.ComposableChain([prompt, question_generator, postprocessor])

def generate_questions(text):
  # Generate questions based on the input text
  return chain.run(text)

# Example usage
input_text = "Your input paragraph here."
questions = generate_questions(input_text)
print(questions)
