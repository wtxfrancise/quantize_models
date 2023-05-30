# quantize_models
This code repository aims to collect various implementation methods for the quantization of large models

# 量化方案

## 1.llama
<p>具体的模型说明和解释可以参考其[官网](https://github.com/facebookresearch/llama) 和 [llama.cpp](https://github.com/ggerganov/llama.cpp)</p>
这里就其量化策略进行总结:
<p>1.1.根据需要下载指定的模型,你可以在huggingface上选择你想要的模型大小版本，其中有llama-7b,llama-13b,llama-30b,llama-65b等版本</p>
<p>1.2.使用git对于需要的模型文件下载，并且放在指定文件夹下，因为是多个文件，所以可以使用如下的git命令,进行整个文件夹的下载,其中[]中的内容为你的下载的目标目录，如huggyllama/llama-7b</p>

```
git clone https://huggingface.co/[你需要下载的目录].git
```
1.3.使用llama.cpp的量化策略进行量化，具体的可以参考[llama.cpp](https://github.com/ggerganov/llama.cpp),主要步骤是,

1.3.1 克隆和编译llama.cpp,但是针对不同的平台使用的编译方法稍微有一点区别
- 使用make进行编译
Linux和MacOs,因为c的工具链比较齐全，cd 到llama.cpp,make即可;但是在windows上面，可以通过下载运行[w64devkit](https://github.com/skeeto/w64devkit/releases)，常常因为语言库的冲突导致编译失败，所以建议在windows上面直接使用cmake
- 使用cmake进行编译，如果没有cmake工具,可以直接通过pip install cmake安装,安装完成后,cd到llama.cpp文件夹下后，具体命令如下,
```shell
mkdir build
cd build
cmake ..
cmake --build . --config Release
```
这个时候生成一个build文件夹，里面有quantize,main 等文件

1.3.2 量化模型
- 安装llama.cpp的依赖库
```shell
python3 -m pip install -r requirements.txt
```
- 将上面步骤2中下载的llama模型转换为FP16的格式.使用如下命令,[]内需要修改为你的模型路径
```shell
python3 convert.py [your model path]
```
- 将生成的FP16格式的模型文件进行4-bits的量化，使用如下命令，

如果是Linux 或是 MacOS 第一个[]内输入，例如：./models/7B/ggml-model-f16.bin ; 第二个[] 内输入你生成模型的目标路径,例如:./models/7B/ggml-model-q4_0.bin
```shell
./quantize [your f16 file path] [your q4 model path] 2
```
如果是windows,两个[]中的内容同上
```shell
build\bin\Release\quantize [your f16 file path] [your q4 model path] 2
```

1.4.运行你的量化模型

1.4.1 在命令行中执行

- 在Linux 或是 MacOS 运行:
```shell
./main -m [your q4 model path] -n 128
```
- 在windows 运行:
```shell
\build\bin\Release\main -m [your q4 model path] -n 128
```
1.4.2 使用llama_cpp库来载入模型,如使用如下python代码:

先使用pip 安装llama_cpp库
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
因为[Chimera](https://github.com/FreedomIntelligence/LLMZoo)是基于llama框架搭建的训练模型，所以其量化方案可以参考llama的quantization的方案，具体步骤如下：

2.1.1下载Chimera的增量化模型，对应的链接可以在LLMZoo中进行[下载](https://github.com/FreedomIntelligence/LLMZoo)，

如，我需要下载7b的增量模型，可以在指定的文件夹下，打开git控制台，输入如下指令进行模型下载： 
```git
git clone https://huggingface.co/FreedomIntelligence/chimera-chat-7b-delta.git
```
2.1.2.下载llama模型，具体下载方式见上文llama中第二条，

2.2.使用[LLMZoo](https://github.com/FreedomIntelligence/LLMZoo)项目中的[apply_delta.py](https://github.com/FreedomIntelligence/LLMZoo/tree/main/tools)参数合并函数，进行参数合并,
具体指令如下：
```shell
python tools/apply_delta.py  --base [llama模型的下载路径]  --target [生成的Chimera目标路径]  --delta [Chimera的下载路径]
```
2.3.可以使用上文llama中的量化策略,具体的可以参考[llama.cpp](https://github.com/ggerganov/llama.cpp),主要步骤是,
2.3.1 克隆和编译llama.cpp,但是针对不同的平台使用的编译方法稍微有一点区别
- 使用make进行编译
Linux和MacOs,因为c的工具链比较齐全，cd 到llama.cpp,make即可;但是在windows上面，可以通过下载运行[w64devkit](https://github.com/skeeto/w64devkit/releases)，常常因为语言库的冲突导致编译失败，所以建议在windows上面直接使用cmake
- 使用cmake进行编译，如果没有cmake工具,可以直接通过pip install cmake安装,安装完成后,cd到llama.cpp文件夹下后，具体命令如下,
```shell
mkdir build
cd build
cmake ..
cmake --build . --config Release
```
这个时候生成一个build文件夹，里面有quantize,main 等文件
- 也可以直接使用Chimera文件夹已经生成好的build文件目录进行编译
2.3.2 量化模型
- 安装llama.cpp的依赖库
```shell
python3 -m pip install -r requirements.txt
```
- 将上面步骤2中下载的llama模型转换为FP16的格式.使用如下命令,[]内需要修改为你的模型路径
```shell
python3 convert.py [your model path]
```
- 将生成的FP16格式的模型文件进行4-bits的量化，使用如下命令，

如果是Linux 或是 MacOS 第一个[]内输入，例如：./models/7B/ggml-model-f16.bin ; 第二个[] 内输入你生成模型的目标路径,例如:./models/7B/ggml-model-q4_0.bin
```shell
./quantize [your f16 file path] [your q4 model path] 2
```
如果是windows,两个[]中的内容同上
```shell
build\bin\Release\quantize [your f16 file path] [your q4 model path] 2
```

2.4.运行你的量化模型

2.4.1 在命令行中执行

- 在Linux 或是 MacOS 运行:
```shell
./main -m [your q4 model path] -n 128
```
- 在windows 运行:
```shell
\build\bin\Release\main -m [your q4 model path] -n 128
```
2.4.2 使用llama_cpp库来载入模型,如使用如下python代码:
先使用pip 安装llama_cpp库
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

2.5 量化文件下载，可以通过百度网盘：
链接：https://pan.baidu.com/s/1mKPiPvmO1BeZPhkwH6F1QQ  提取码：6fzy 


-----------
## 3.bloomz
3.1 下载bloomz模型，具体可以点击[链接地址](https://github.com/NouamaneTazi/bloomz.cpp)进行查看

3.2 自行编译，可以使用make工具进行编译, 具体指令为:

3.2.1 自行编译，可以使用make工具进行编译, 具体指令为:
```shell
git clone https://github.com/NouamaneTazi/bloomz.cpp && cd bloomz.cpp
make
```
3.2.2 直接使用已经在Linux编译好的文件，文件见Phoenix/Linux 文件夹，可以直接使用

3.3 使用bloom的量化方案

3.3.1 可以执行如下命令,将Phoenix转换为ggml格式，使用如下指令
```shell

python3 convert-hf-to-ggml.py [你下载的模型路径] [你希望存储ggml格式的路径] 

```
3.3.2 得到指定的ggml文件后，进行4-bits量化，具体指令如下:

```shell
./quantize [ggml格式路径] [量化后的格式路径] 2

如：./quantize ./models/ggml-model-bloomz-7b1-f16.bin ./models/ggml-model-bloomz-7b1-f16-q4_0.bin 2
```

3.4 通过编译的main文件，进行量化后的结果验证:
```
./main -m models/ggml-model-bloomz-7b1-f16-q4_0.bin  -p 'Translate "Hi, how are you?" in French:' -t 8 -n 256
```
3.5 对应的量化模型可以[点击这里下载](https://huggingface.co/Wauplin/bloomz-7b1.cpp/tree/main)

-----------
## 4.Phoenix
4.1 下载Phoenix模型，具体可以点击[链接地址](https://github.com/FreedomIntelligence/LLMZoo)进行查看

4.2 因为Phoenix是基于bloom方案，所以可以迁移其量化方案，具体的可以[点击这里](https://github.com/NouamaneTazi/bloomz.cpp)进行查看，

4.2.1 自行编译，可以使用make工具进行编译, 具体指令为:
```shell
git clone https://github.com/NouamaneTazi/bloomz.cpp && cd bloomz.cpp
make
```
4.2.2 直接使用已经在Linux编译好的文件，文件见Phoenix/Linux 文件夹，可以直接使用

4.3 使用bloom的量化方案

4.3.1 可以执行如下命令,将Phoenix转换为ggml格式，使用如下指令
```shell
python3 convert-hf-to-ggml.py [你下载的模型路径] [你希望存储ggml格式的路径] 

如：python3 Phoenix\convert-hf-to-ggml.py .\LLMModel\phoenix-chat-7b ./models
```

4.3.2 得到指定的ggml文件后，进行4-bits量化，具体指令如下:

```shell
./quantize [ggml格式路径] [量化后的格式路径] 2

如：./quantize ./models/ggml-model-bloomz-7b1-f16.bin ./models/ggml-model-bloomz-7b1-f16-q4_0.bin 2
```

4.4 通过编译的main文件，进行量化后的结果验证:
```
./main -m models/ggml-model-bloomz-7b1-f16-q4_0.bin  -p 'Translate "Hi, how are you?" in French:' -t 8 -n 256
```

4.5 可以在下面的百度网盘进行量化模型的下载，分享地址为：
链接：https://pan.baidu.com/s/1iyuREwapZLttfT6VhuKqhQ  提取码：s0us 


-----------
## 5.ChatGLM
todo

----------
## 6.Falcon
todo

