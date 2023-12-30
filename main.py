import local_tokens
from langchain.llms import OpenAI
from langchain import PromptTemplate

oai_key = local_tokens.api_keys()["OAI"]["CMN"]

# initializing the model
openai = OpenAI(
  model_name="text-davinci-003",
  openai_api_key=oai_key
)

with open("prompt_template.txt", "r") as f:
  template = f.read()

with open("sample_blogs/Do_Nots.txt", "r") as f: 
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
  num_ques = 1,
  ques_type = ["coding", "logical", "coding and logical"][0]
)

# print(prompt)
print(openai(prompt))
