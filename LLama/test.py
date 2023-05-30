from llama_cpp import Llama
path = "your q4 model path"
llm = Llama(model_path=path)
output = llm("Q: what is your name? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)