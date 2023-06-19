[**🇨🇳中文**](./README.md) | [**English**](./README_EN.md) |

# quantize_models
This code repository aims to collect various implementation methods for the quantization of large models

# Quantization scheme

## 1.llama
<p>Detail model descriptions and explanations can be referred to its [official website](https://github.com/facebookresearch/llama) and [llama.cpp](https://github.com/ggerganov/llama.cpp)</p>
Here's a summary of its quantification strategy:
<p>1.1 Download the specific model as needed, you can choose the size of the model you want on Huggingface, including versions like llama-7b, llama-13b, llama-30b, llama-65b, etc.</p>
<p>1.2 Use Git to download the necessary model files and place them in the specified folder. As there are multiple files, you can use the following Git command to download the entire folder. The content in the [] is your target download directory, such as huggyllama/llama-7b.</p>

```
git clone https://huggingface.co/[The directory you need to download].git
```
1.3.Quantify using llama.cpp's quantification strategy, the specifics can be referred to[llama.cpp](https://github.com/ggerganov/llama.cpp),The main steps are:

1.3.1 Clone and compile llama.cpp, but the compilation method used varies slightly for different platforms
- Compile using make
For Linux and MacOS, since the C toolchain is quite complete, simply cd to llama.cpp and use make; however, on Windows, you can download and run[w64devkit](https://github.com/skeeto/w64devkit/releases),Compilation often fails due to conflicts in language libraries, so it's recommended to use cmake directly on Windows.
- Compile using cmake. If you don't have the cmake tool, you can install it directly with pip install cmake. After installation, cd to the llama.cpp folder, and the specific commands are as follows:
```shell
mkdir build
cd build
cmake ..
cmake --build . --config Release
```
At this point, a build folder is generated, containing files like quantize, main, etc.

1.3.2 Quantify the model
- Install the dependencies of llama.cpp
```shell
python3 -m pip install -r requirements.txt
```
- Convert the llama model downloaded in the above step 2 to FP16 format. Use the following command, [] needs to be changed to your model path
```shell
python3 convert.py [your model path]
```
- Quantify the generated FP16 format model file into 4-bits using the following command,

For Linux or MacOS, enter the following in the first [] for example: ./models/7B/ggml-model-f16.bin ; in the second [] enter the target path for your generated model, for example: ./models/7B/ggml-model-q4_0.bin
```shell
./quantize [your f16 file path] [your q4 model path] 2
```
For windows, the contents of the two [] are the same as above
```shell
build\bin\Release\quantize [your f16 file path] [your q4 model path] 2
```

1.4.Run your quantified model

1.4.1 Execute in the command line

- Run on Linux or MacOS:
```shell
./main -m [your q4 model path] -n 128
```
- Run on Windows:
```shell
\build\bin\Release\main -m [your q4 model path] -n 128
```
1.4.2 Load the model using the llama_cpp library, such as using the following python code:

use pip to install the llama_cpp library.

```shell
pip install llama_cpp
```
```python
from llama_cpp import Llama
path = "your q4 model path"
llm = Llama(model_path=path)
output = llm("Q: what is your name? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)
```

-----------

## 2.Chimera
Since[Chimera](https://github.com/FreedomIntelligence/LLMZoo)is a training model built based on the llama framework, its quantization scheme can refer to the llama's quantization scheme, and the specific steps are as follows:

2.1.1 Download Chimera's incremental model, the corresponding link can be[downloaded](https://github.com/FreedomIntelligence/LLMZoo)from LLMZoo,

For example, if I need to download the 7b incremental model, I can open the git console in the specified folder and enter the following command to download the model:
```git
git clone https://huggingface.co/FreedomIntelligence/chimera-chat-7b-delta.git
```
2.1.2 Download the llama model, the specific download method see the second point in the llama section above,

2.2. Use the parameter merge function in the [apply_delta.py](https://github.com/FreedomIntelligence/LLMZoo/tree/main/tools) of the [LLMZoo](https://github.com/FreedomIntelligence/LLMZoo) project for parameter merging,
The detail command is as follows:
```shell
python tools/apply_delta.py  --base [download path of llama model]  --target [target path of generated Chimera]  --delta [download path of Chimera]
```
2.3.You can use the quantization strategy mentioned in the llama section above, the specifics can refer to[llama.cpp](https://github.com/ggerganov/llama.cpp),The main steps are,
2.3.1 Clone and compile llama.cpp, but the compilation method used varies slightly for different platforms
- Compile using make
For Linux and MacOS, since the C toolchain is quite complete, cd to llama.cpp and use make; however, on Windows, you can download and run[w64devkit](https://github.com/skeeto/w64devkit/releases),Compilation often fails due to conflicts in language libraries, so it's recommended to use cmake directly on Windows.
- Compile using cmake, if you do not have the cmake tool, you can install it directly with pip install cmake, after installation, cd to the llama.cpp folder, the specific command is as follows,
```shell
mkdir build
cd build
cmake ..
cmake --build . --config Release
```
At this point, a build folder is generated, containing files like quantize, main, etc.
- You can also directly use the build file directory that has already been generated in the Chimera folder for compilation
2.3.2  Quantify the model
- Install the dependencies of llama.cpp
```shell
python3 -m pip install -r requirements.txt
```
- Convert the llama model downloaded in the above step 2 to FP16 format. Use the following command, [] needs to be changed to your model path
```shell
python3 convert.py [your model path]
```
- Quantify the generated FP16 format model file into 4-bits using the following command,

For Linux or MacOS, enter the following in the first [] for example: ./models/7B/ggml-model-f16.bin ; in the second [] enter the target path for your generated model, for example: ./models/7B/ggml-model-q4_0.bin
```shell
./quantize [your f16 file path] [your q4 model path] 2
```
For windows, the contents of the two [] are the same as above
```shell
build\bin\Release\quantize [your f16 file path] [your q4 model path] 2
```

2.4.Run your quantified model

2.4.1 Execute in the command line

- Run on Linux or MacOS:
```shell
./main -m [your q4 model path] -n 128
```
- Run on Windows:
```shell
\build\bin\Release\main -m [your q4 model path] -n 128
```
2.4.2 Load the model using the llama_cpp library, such as using the following python code:
Use pip to install the llama_cpp library.
```shell
pip install llama_cpp
```

```python
from llama_cpp import Llama
path = "your q4 model path"
llm = Llama(model_path=path)
output = llm("Q: what is your name? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)
```

2.4.3 Memory/Disk Requirements
You need sufficient disk space to store them, and enough RAM to load them. The memory and disk requirements are the same. Below are the specific requirements.

| Model            | Original size | Quantized size (4-bit) |
|------------------|---------------|------------------------|
| chimera-chat-7B  | 12.5 GB       | 3.9GB                  |
| chimera-inst-chat-7B | 12.5 GB   | 3.9GB                  |

2.4.4 inference speed

| Model                | Measure      | F16   |Q4|
|----------------------|--------------|-------|-----------|
| chimera-chat-7B      | perplexity   | todo  | todo  |
| chimera-chat-7B      | file size    | todo  | todo  |
| chimera-chat-7B      | ms/tok       |  todo  | todo  |


2.5 Quantified files can be downloaded through Baidu Netdisk:
Link：https://pan.baidu.com/s/1mKPiPvmO1BeZPhkwH6F1QQ  code：6fzy 


-----------
## 3.bloomz
3.1 Download the bloomz model, you can click this [link](https://github.com/NouamaneTazi/bloomz.cpp) to view.

3.2 Compile 

3.2.1 Compile it yourself, you can use the make tool to compile, the specific instructions are:
```shell
git clone https://github.com/NouamaneTazi/bloomz.cpp && cd bloomz.cpp
make
```
3.2.2 Directly use the files that have been compiled on Linux, you can see the files in the Phoenix/Linux folder, which can be used directly.

3.3 Use the quantization scheme of bloom

3.3.1 You can execute the following command to convert Phoenix to ggml format, use the following command
```shell

python3 convert-hf-to-ggml.py [your downloaded model path] [the path you want to store the ggml format] 

```
3.3.2 After getting the specified ggml file, perform 4-bits quantization, the specific command is as follows:

```shell
./quantize [ggml format path] [path after quantization] 2

如：./quantize ./models/ggml-model-bloomz-7b1-f16.bin ./models/ggml-model-bloomz-7b1-f16-q4_0.bin 2
```

3.4 Verify the results after quantization through the compiled main file:
```
./main -m models/ggml-model-bloomz-7b1-f16-q4_0.bin  -p 'Translate "Hi, how are you?" in French:' -t 8 -n 256
```
3.5 The corresponding quantized model can be[downloaded here](https://huggingface.co/Wauplin/bloomz-7b1.cpp/tree/main).

-----------
## 4.Phoenix
4.1 Download the Phoenix model, you can click[this link](https://github.com/FreedomIntelligence/LLMZoo)to view.

4.2 Since Phoenix is based on the bloom scheme, its quantization scheme can be transferred. For details, you can[click here](https://github.com/NouamaneTazi/bloomz.cpp) to view.

4.2.1 Compile it yourself, you can use the make tool to compile, the specific instructions are:
```shell
git clone https://github.com/NouamaneTazi/bloomz.cpp && cd bloomz.cpp
make
```
4.2.2 Directly use the files that have been compiled on Linux, you can see the files in the Phoenix/Linux folder, which can be used directly.

4.3 Use the quantization scheme of bloom

4.3.1 You can execute the following command to convert Phoenix to ggml format, use the following command
```shell
python3 convert-hf-to-ggml.py [your downloaded model path] [the path you want to store the ggml format]

如：python3 Phoenix\convert-hf-to-ggml.py .\LLMModel\phoenix-chat-7b ./models
```

4.3.2 After getting the specified ggml file, perform 4-bits quantization, the specific command is as follows:

```shell
./quantize [ggml format path] [path after quantization] 2

eg：./quantize ./models/ggml-model-bloomz-7b1-f16.bin ./models/ggml-model-bloomz-7b1-f16-q4_0.bin 2
```

4.3.4 Memory/Disk Requirements
You need sufficient disk space to store them, and enough RAM to load them. The memory and disk requirements are the same. Below are the specific requirements.

| Model            | Original size | Quantized size (4-bit) |
|------------------|---------------|------------------------|
| phoenix-chat-7b  | 15 GB         | 4.7GB                 |

4.4.4 inference speed

| Model                | Measure      | F16   |Q4|
|----------------------|--------------|-------|-----------|
| phoenix-chat-7b      | perplexity   | todo  | todo  |
| phoenix-chat-7b     | file size    | todo  | todo  |
| phoenix-chat-7b    | ms/tok       |  todo  | todo  |


4.4 Verify the results after quantization through the compiled main file:
```
./main -m models/ggml-model-bloomz-7b1-f16-q4_0.bin  -p 'Translate "Hi, how are you?" in French:' -t 8 -n 256
```

4.5  You can download the quantized model from the Baidu Netdisk link below, the sharing address is:
link：https://pan.baidu.com/s/1iyuREwapZLttfT6VhuKqhQ  code：s0us 


-----------
## 5.ChatGLM
todo

----------
## 6.Falcon
todo
