# Convert Hugging Face fine-tuned bloom-like models to ggml format
#
# Usage:
#
#   python3 models/convert-h5-to-ggml.py 
#
# This script is similar to "convert-pt-to-ggml.py"
#

import io
import os
import sys
import struct
import json
import code
import torch
import numpy as np

from transformers import BloomModel
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, BloomForCausalLM

conv_map = {
    'word_embeddings'       : 'tok_embeddings',
    "word_embeddings_layernorm": 'norm',
        'input_layernorm'        : 'attention_norm',
        'self_attention.query_key_value': 'attention.query_key_value',
        'self_attention.dense':          'attention.wo',
        'post_attention_layernorm': 'ffn_norm',
        'mlp.dense_h_to_4h'           : 'feed_forward.w1',
        'mlp.dense_4h_to_h'           : 'feed_forward.w2',
        'ln_f'                        : 'output_norm',
        'lm_head' : 'output',
        }

# ref: https://github.com/openai/gpt-2/blob/master/src/encoder.py
def bytes_to_unicode():
    """
    Returns list of utf-8 byte and a corresponding list of unicode strings.
    The reversible bpe codes work on unicode strings.
    This means you need a large # of unicode characters in your vocab if you want to avoid UNKs.
    When you're at something like a 10B token dataset you end up needing around 5K for decent coverage.
    This is a significant percentage of your normal, say, 32K bpe vocab.
    To avoid that, we want lookup tables between utf-8 bytes and unicode strings.
    And avoids mapping to whitespace/control characters the bpe code barfs on.
    """
    bs = list(range(ord("!"), ord("~")+1))+list(range(ord("¡"), ord("¬")+1))+list(range(ord("®"), ord("ÿ")+1))
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8+n)
            n += 1
    cs = [chr(n) for n in cs]
    return dict(zip(bs, cs))

if len(sys.argv) < 3:
    print("Usage: python convert-hf-to-ggml.py model_name dir-output [use-f32]")
    print("  model_name: name of the model to convert. Example: 'bigscience/bloomz-560m'")
    print("  dir-output: directory where the output file will be written")
    print("  use-f32:    if present, use float32 instead of float16")
    sys.exit(1)

model_name = sys.argv[1]
dir_out = sys.argv[2]

# make sure the output directory exists
os.makedirs(dir_out, exist_ok=True)

# possible data types
#   ftype == 0 -> float32
#   ftype == 1 -> float16
#
# map from ftype to string
ftype_str = ["f32", "f16"]
ftype = 1
if len(sys.argv) > 3:
    ftype = 0

tokenizer = AutoTokenizer.from_pretrained(model_name)
config = AutoConfig.from_pretrained(model_name)
hparams = config.to_dict()
print("Loading model: ", model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, config=config, torch_dtype=torch.float16 if ftype == 1 else torch.float32, low_cpu_mem_usage=True)
print("Model loaded: ", model_name)


fname_out = dir_out + f"/ggml-model-{model_name.split('/')[-1]}-{ftype_str[ftype]}.bin"
fout = open(fname_out, "wb")

hparams["multiple_of"] = 1
fout.write(struct.pack("i", 0x67676d6c)) # magic: ggml in hex
fout.write(struct.pack("i", hparams["vocab_size"]))
# fout.write(struct.pack("i", hparams["seq_length"]))
fout.write(struct.pack("i", hparams["hidden_size"]))
fout.write(struct.pack("i", hparams["multiple_of"]))
fout.write(struct.pack("i", hparams["n_head"]))
fout.write(struct.pack("i", hparams["n_layer"]))
fout.write(struct.pack("i", ftype))

# Is this correct??
dot_token = tokenizer.encode(".")[0]
for i in range(hparams["vocab_size"]):
    text = tokenizer.decode([i]).encode('utf-8')
    fout.write(struct.pack("i", len(text)))
    fout.write(text)
    
list_vars = model.state_dict()
for name in list_vars.keys():
    src = name
    nn = name
    if name != "lm_head.weight":
        nn = nn.split(".")[1:]
    else:
        nn = nn.split(".")

    if nn[0] == "h":
        nn[0] = "layers"
        mapped = conv_map[".".join(nn[2:-1])]
        name = ".".join(nn[:2] + [mapped] + nn[-1:])
    else:
        mapped = conv_map[".".join(nn[:-1])]
        name = ".".join([mapped] + nn[-1:])

    if "query_key_value" in src:
        q, k, v = list_vars[src].reshape(config.n_head, 3, -1).unbind(1)
        list_vars[src] = torch.cat([q, k, v], dim=0).reshape_as(list_vars[src])

    print(src, ' -> ', name)
    data = list_vars[src].squeeze().numpy()
    data = data.astype(np.float32)

    n_dims = len(data.shape)
    print(name, n_dims, data.shape)

    # default type is fp32
    ftype_cur = 0
    if ftype == 1 and n_dims > 1:
        print("  Converting to float16")
        data = data.astype(np.float16)
        ftype_cur = 1

    # header
    str = name.encode('utf-8')
    fout.write(struct.pack("iii", n_dims, len(str), ftype_cur))
    for i in range(n_dims):
        fout.write(struct.pack("i", data.shape[n_dims - 1 - i]))
    fout.write(str);

    # data
    data.tofile(fout)

fout.close()

print("Done. Output file: " + fname_out)
print("")
