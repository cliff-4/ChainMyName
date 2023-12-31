import local_tokens
from langchain.llms import OpenAI
from langchain import PromptTemplate

filename = "sample_blogs/what_is_npm.txt"
modelname = "text-davinci-003"

# fetching keys
oai_key = local_tokens.api_keys()["OAI"]["CMN"]

# initializing the model
openai = OpenAI(
  model_name=modelname,
  openai_api_key=oai_key
)

with open("prompt_template.txt", "r") as f:
  template = f.read()

with open(filename, "r") as f: 
  blog_txt = f.read()

prompt_template = PromptTemplate(
  input_variables=[
    "blog_txt", 
    "num_ques",
    "ques_type"
  ],
  template=template
)

prompt = prompt_template.format(
  blog_txt = blog_txt,
  num_ques = 10,
  ques_type = "coding or logical"
)

print(f"Input File name: {filename}")
print(f"Model used: {modelname}")
print(openai(prompt))
