import local_tokens
from transformers import pipeline
import langchain

# Your Hugging Face API token
huggingface_token = local_tokens.hf_api_keys()["INIT"][1]

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

from transformers import pipeline
print("Transformers library has been installed successfully!")


# [Do this pls]
# conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
# # Anything above 2.10 is not supported on the GPU on Windows Native
# python -m pip install "tensorflow<2.11"
# # Verify the installation:
# python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"