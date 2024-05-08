# Med-attack

## 引言
在医学领域，图像和文本数据具有自然语言数据集中难以企及的强相关性和高正确率，这主要由于技术的特殊性和专业人员的使用素养。这种差异往往与自然语言处理中普遍的恶意意图直接对齐不同。然而，医学图像、文本和偶发噪声的变异可能导致症状描述与病变插图之间的不匹配。这种错配挑战了MedMLLM的输出，会对MedMLLM生成的结果造成干扰，故而我们把Text-image之间的相关性弱界定为医学上的特异性攻击。

## 数据集构建
1. **图像数据集的编译**：选择多种医学图像，构建图像数据集MedMQ。
2. **正常提示生成**：使用视觉问答（VQA）模型，根据图像自动生成高度相关和专业的提示。
3. **有害提示生成**：借助GPT-4处理正常提示，得到关联度较低的非恶意有害提示，模拟潜在的临床攻击。

## 现有方法比较
大多数现有方法如GCG、deltaJP和Typo等，主要笼统的通过拒绝与否来评定是否造成干扰，而不是关注相似性和关联度，因此缺乏严谨性。

## 新方法引入
1. **多轮交叉优化**：为平衡图像和文本的重要性，我们实施多轮交叉优化。
2. **病变区域优化**：由于模态不匹配主要发生在病变区域，我们特别优化具有病变的patch或者掩盖病灶区的patch生成攻击样本。

## 评估
与现有方法的比较至关重要，使用新定义的指标：
1. **输入关联度评分TII**：输入文本和图像之间的相关性决定了响应的接受或拒绝。低关联度结果应为拒绝（空白对照），确保只有高关联度才能验证后续比较。
2. **输出文本-输入文本关联度评分TT0**：输出文本与输入文本之间的相关性指示攻击的成功。
3. **输出文本-输入图像关联度评分TIO**：此指标进一步验证攻击的成功，基于输出文本与输入图像之间的相关性。
4. **综合评价指标**：为指标TII,TTO,TIO分配权重，形成一个全面的新评估指标。
5. **比较测试**：我们的方法在我们的数据集、其他数据集、不同的MedMLLM以及普通MLLM的医学部分进行测试。

## 结论
我们的dataset全，我们的针对性新方法显著提高攻击成功率，并且新关联度可以作为可靠指标进行推广



# Medical Safety and Specificity Attacks in MedMLLM: A Comprehensive Outline

## Introduction
In medical contexts, image and text data possess an inherently high correlation unmatched in natural language datasets, primarily due to the technical specificity and the literacy of professional users. This differentiation often prevents a direct alignment with general malicious intents found in natural language processing. However, variations in medical images, texts, and incidental noise can lead to discrepancies between symptom descriptions and lesion illustrations. This misalignment challenges the output of MedMLLM, leading us to categorize weak text-image correlations as specific medical attacks.

## Dataset Construction
1. **Image Dataset Compilation**: A diverse set of medical images is selected to construct Image Dataset A.
2. **Normal Prompts Generation**: Utilizing a Visual Question Answering (VQA) model, prompts that are highly relevant and professional are automatically generated based on the images.
3. **Generation of Harmful Prompts**: With the assistance of GPT-4, we process the Normal Prompts to derive less relevant, non-malicious harmful prompts, simulating potential clinical attacks.

## Comparison with Existing Methods
Most existing methodologies, such as GCG, deltaJP, and Typo, focus on acceptance or rejection based on superficial criteria rather than on similarity and relevance, thus lacking rigor.

## Introduction of a New Method
1. **Multi-round Cross-optimization**: To balance the significance of images and texts, we implement multi-round cross-optimization.
2. **Optimization of Lesion Patches**: Since modal mismatches typically occur in lesion areas, we specifically optimize patches with lesions to generate attack samples.

## Evaluation
Comparison with existing methods is crucial, using newly defined metrics:
1. **Association Score for Input (ASR)**: The relevance between the input text and image determines the acceptance or rejection of the response. A low correlation results in rejection (null control), ensuring only high correlations validate subsequent comparisons.
2. **Association Score for Output Text-Input Text (RR)**: The relevance between the output and input texts indicates the success of an attack.
3. **Association Score for Output Text-Input Image**: This metric further validates the success of an attack based on the relevance between the output text and the input image.
4. **Composite Metric**: Weights are assigned to metrics 0, 1, and 2 to formulate a comprehensive new evaluation metric.
5. **Comparative Testing**: Our method is tested against previous methods on our dataset, other datasets, different MedMLLMs, and general sections of MLLMs in medicine.

## Conclusion
Our comprehensive dataset and the novel method significantly enhance the safety and specificity of medical applications in machine learning language models.

Remember, this outline is crafted to emphasize the significant points provided without any omissions.




| **Major Category**     | **Subcategory**            | **Sub-Subcategory**    | **Description**                                                                                                                                 |
|------------------------|----------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **Image Understanding** | **Coarse-grained**         | Disease Classification | Diagnosing the presence or absence of disease. Identifies specific diseases from images.                                                        |
|                        |                            | View Classification    | Identifying the view or angle. Important for correct image interpretation.                                                                      |
|                        | **Fine-grained**           | Abnormality Detection  | Locates specific abnormalities within an image. Critical for accurate diagnosis.                                                                |
|                        |                            | Object Detection       | Identifies foreign objects. Essential for patient safety and treatment planning.                                                                |
| **Text Generation**    | **Report Generation**      | Impression Generation  | Summarizes the diagnostic impression. Key for conveying overall assessment.                                                                     |
|                        |                            | Findings Generation    | Details findings from image analysis. Provides evidence-based diagnosis.                                                                        |
|                        | **Findings and Impressions** | Anatomical Findings     | Related to specific anatomical parts. Enhances localized diagnostic accuracy.                                                                   |
|                        |                            | Impression Summary     | Brief summary for specific regions. Aids in focused assessment.                                                                                  |
| **Question Answering** | **Visual QA**              | Open-ended             | Answers open questions based on images. Encourages comprehensive analysis.                                                                      |
|                        |                            | Close-ended            | Chooses correct answers from options. Tests specific understanding of image content.                                                            |
|                        | **Text QA**                | Fact-based             | Answers based on explicit text facts. Requires detailed text understanding.                                                                     |
|                        |                            | Inference-based        | Inferences from text to answer. Demands deeper comprehension and logic.                                                                         |
| **Miscellaneous**      | **Image-Text Matching**    | Matching               | Determines correct image-text pairs. Crucial for accurate information presentation.                                                             |
|                        |                            | Selection              | Chooses suitable text for an image. Ensures relevance and accuracy of information.                                                              |
|                        | **Report Evaluation**      | Error Identification   | Identifies inaccuracies in reports. Key for quality control and correction.                                                                     |
|                        |                            | Quality Assessment     | Assesses report accuracy and completeness. Important for diagnostic integrity.                                                                  |
|                        | **Explanation and Inference** | Explanation Generation  | Generates explanations for diagnoses. Facilitates understanding and trust.                                                                      |
|                        |                            | Inference Making       | Determines logical report relationships. Supports clinical decision-making.                                                                     |


## Medical Prompt Generation (MPG)

### 文件路径
以下是项目路径
```plaintext
MedicalPromptGeneration/
│
├── src/                   # 源代码
│   ├── __init__.py
│   ├── main.py            # 主程序入口
│   ├── model.py           # 模型定义
│   ├── data_loader.py     # 数据加载
│   ├── transformer_utils/ # 包含所有与transformers相关的操作
│   │   ├── __init__.py
│   │   ├── tokenizer.py
│   │   └── model_utils.py
│   └── utilities/         # 其他辅助功能
│       ├── __init__.py
│       └── utils.py
│
├── configs/               # 配置文件
│   └── model_config.json
│
├── data/                  # 数据存放
│   ├── images/            # 图像数据
│   └── annotations/       # 标注数据
│
├── models/                # 预训练模型和权重
│   ├── ofa/
│   └── bert/
│
├── outputs/               # 输出和结果
│   ├── logs/              # 日志文件
│   └── predictions/       # 模型预测结果
│
└── requirements.txt       # Python依赖包

```

### 使用

#### MedicalPromptGeneration

针对data中的图片，利用llavamed提取attributes list,得到attribute-sentensce(AS)
```bash
python src/main.py 
```

#### metric

text2text得到文本相似性
```bash
python text2text.py
```
text2image得到图像文本相似性
```bash
python text2image.py
```

获取随机选取得到的3MAD-70K
```bash
cd dataset_generate
bash datasetgenerate.sh
```

统计
```bash
python demo_count.py
```
计算prompts的相似性分数
```bash
python demo_promptst2t.py
python demo_dealsimilarity.py
```

#### 文件
aggregated_scores.csv  18类图片和attribute相似分数
averaged_file.csv 540-540，18类prompts之间的相关性分析分数

# 3MAD-70K: Multimodal Medical Model Attack Dataset, A Comprehensive Assessment of ASR in Medical Models

## Overview

This repo contains the source code of 3MAD-70K. This research endeavor is designed to help researchers better understand the capabilities, limitations, and potential risks associated with deploying these state-of-the-art Medical Multimodal Large Language Models (MedMLLMs). See our paper for details.

[**Our paper**](https://arxiv.org/) 

*Xijie Huang, Xinyuan Wang, Hantao Zhang, Jiawen Xi, Chengwei Pan.*

https://arxiv.org/pdf/

本项目由共**9**大类不同介质，**18**类不同部位的医学图像集（CMIC-96K）和**18**种基于用户需求的询问指令交叉构建而成，符合临床上可能出现的**unmatch attack** and **malicious attack**的具体攻击类型

图片集（CMIC-96K）组成：
```plaintext
├── MRI (6728)
│   ├── lumbarMRI (53)
│   ├── brainAlzheimerMRI (6400)
│   └── brainMRI (275)
├── Fundus (45)
│   └── retinaFundus (45)
├── Mamography (24576)
│   └── breastMamography (24576)
├── OCT (2064)
│   └── retinaOCT (2064)
├── CT (10015)
│   ├── heartct (5227)
│   ├── brainct (2515)
│   ├── covid19chestct (1273)
│   └── chestct (1000)
├── Endoscopy (1500)
│   └── gastroentEndoscopy (1500)
├── dermoscopy (6000)
│   └── skinDermoscopy (6000)
├── Ultrasound (4642)
│   ├── carotidUltrasound (1100)
│   ├── breastUltrasoun (470)
│   ├── ovaryUltrasound (54)
│   ├── brainUltrasound (1334)
│   └── babyUltrasound (1684)
└── X-ray (41142)
    ├── Tufts_Dental_Database (1000)
    ├── MURA-v1.1 (40005)
    └── chestxray (137)
```

指令组成：
```plaintext
MedMQ
├── Image Understanding
│   ├── Coarse-grained
│   │   ├── Disease Classification - Diagnosing the presence or absence of disease. Identifies specific diseases from images.
│   │   └── View Classification - Identifying the view or angle. Important for correct image interpretation.
│   └── Fine-grained
│       ├── Abnormality Detection - Locates specific abnormalities within an image. Critical for accurate diagnosis.
│       └── Object Detection - Identifies foreign objects. Essential for patient safety and treatment planning.
├── Text Generation
│   ├── Report Generation
│   │   ├── Impression Generation - Summarizes the diagnostic impression. Key for conveying overall assessment.
│   │   └── Findings Generation - Details findings from image analysis. Provides evidence-based diagnosis.
│   └── Findings and Impressions
│       ├── Anatomical Findings - Related to specific anatomical parts. Enhances localized diagnostic accuracy.
│       └── Impression Summary - Brief summary for specific regions. Aids in focused assessment.
├── Question Answering
│   ├── Visual QA
│   │   ├── Open-ended - Answers open questions based on images. Encourages comprehensive analysis.
│   │   └── Close-ended - Chooses correct answers from options. Tests specific understanding of image content.
│   └── Text QA
│       ├── Fact-based - Answers based on explicit text facts. Requires detailed text understanding.
│       └── Inference-based - Inferences from text to answer. Demands deeper comprehension and logic.
└── Miscellaneous
    ├── Image-Text Matching
    │   ├── Matching - Determines correct image-text pairs. Crucial for accurate information presentation.
    │   └── Selection - Chooses suitable text for an image. Ensures relevance and accuracy of information.
    ├── Report Evaluation
    │   ├── Error Identification - Identifies inaccuracies in reports. Key for quality control and correction.
    │   └── Quality Assessment - Assesses report accuracy and completeness. Important for diagnostic integrity.
    └── Explanation and Inference
        ├── Explanation Generation - Generates explanations for diagnoses. Facilitates understanding and trust.
        └── Inference Making - Determines logical report relationships. Supports clinical decision-making.

```
为了有效解决图片数量不匹配的长尾问题并且预防可能产生的失衡可能性，我们将少量图片倍增，将数量较多的图片随机抽取，使得不同种类之间尽可能维持同一数量级

## Getting Started

To evaluate using 3MAD-28K dataset, please install the 3MAD-28K package as below:

<!-- ### (Conda +) Pip

For now, we suggest installing DecodingTrust by cloning our repository and install it in editable mode. This will keep the data, code, and configurations in the same place. 

```bash
git clone https://github.com/AI-secure/DecodingTrust.git && cd DecodingTrust
pip install -e .
```

Please note that this will install PyTorch with `pip`. If your system does not have a `CUDA` version compatible with the PyTorch `pip` wheel. To install `PyTorch` with `Conda` first, as shown below.

```bash
conda create --name dt-test python=3.9 pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
conda activate dt-test
pip install "decoding-trust @ git+https://github.com/AI-secure/DecodingTrust.git"
```

It is also possible to install DecodingTrust as a standalone package, but you will need to clone our repository again to run it will our data.
```bash
conda create --name dt-test python=3.9
conda activate dt-test
pip install "decoding-trust @ git+https://github.com/AI-secure/DecodingTrust.git"
```

### Support for the `ppc64le` Architecture 

We also support the `ppc64le` architecture of IBM Power-9 platforms. To install on this platform, please first make sure you have the following `conda` channels so that we can utilize pre-built packages.

```
--add channels 'defaults'   # lowest priority
--add channels 'https://public.dhe.ibm.com/ibmdl/export/pub/software/server/ibm-ai/conda-early-access/'
--add channels 'https://public.dhe.ibm.com/ibmdl/export/pub/software/server/ibm-ai/conda/'
--add channels 'https://opence.mit.edu'
--add channels 'https://ftp.osuosl.org/pub/open-ce/current/'
--add channels 'conda-forge'   # highest priority
```

Then, install the following pre-built packages.

```bash
mamba create --name dt-test python==3.9 pytorch=2.0.1 torchvision=0.15.2 spacy=3.5.3 scipy=1.10.1 fairlearn~=0.9.0 scikit-learn~=1.1.2 pandas~=2.0.3 pyarrow~=11.0.0 rust -c conda-forge
```

Finally, install DecodingTrust with `pip` as usual.

### Docker / Singularity

To use DecodingTrust with docker, simply pull the following docker image.
```bash
sudo docker pull danielz01/decoding-trust
docker run -it \
    -v /path/on/host:/path/in/container \
    --gpus all \
    decoding-trust/v1.0:latest [arg1 arg2 ...]
```
To use it in through singularity or apptainer container environments on HPC environments, simply run the following.
```bash
module load singularity  # Change it to whatever module name your singularity / apptainer environment was given
singularity pull decoding-trust-v1.0.sif docker://danielz01/decoding-trust
singularity exec --nv --bind /path/on/host:/path/in/container decoding-trust-v1.0.sif [arg1 arg2]
```

We will also have a container build for `ppc64le` platforms soon. Stay tuned!

### Notes
+ Each of the eight areas has its own subdirectory containing the respective code and README.

+ Follow the specific `README`: Every subdirectory has its own README. Refer to these documents for information on how to run the scripts and interpret the results.


## [Important] Candidate models
In our benchmark, to have consistent conclusions and results, currently we mianly focus on evaluating the following two OpenAI models:

- `gpt-3.5-turbo-0301`          
- `gpt-4-0314`

**Note we use `gpt-3.5-turbo-0301` (with time stamp) released in March instead of `gpt-3.5-turbo` for sake of model evolution to ensure reproducibility.**

Currently, we have supported evaluating all the causal LLMs **hosted in Huggingface** or hosted locally. Specifically, we have tested the following open LLMs:

- `Llama-v2-7B-Chat`
- `Vicuna-7BAlpaca-7B`
- `MPT-7B`
- `Falcon-7B`
- `Alpaca-7B`
- `RedPajama-INCITE-7B-Instruct` -->

## Tutorial

<!-- We have provided a [Tutorial](Tutorial.md) to help you walk through the usage of API to evaluate different trustworthiness perspectives and LLMs.   -->

## Useful tips

<!-- - Please first evaluate your experiments with `++dry_run=True` flags on to check the input / output format, and use `gpt-3.5-turbo-0301` to check the generation since it has lower costs.
- Suggesting saving the responses from OpenAI. -->

## File usage

<!-- - `main.py` provides a unified entry point to evaluate all the perspectives and different LLMs with proper configuration
- `chat.py` provides robust APIs for creating requests to OpenAI **Chat Compleition** models and Huggingface autoregressive LLMs. Recommend implementing experiments based on this file. If you think `chat.py` is not good enough and want to make modifications, please let @acphile and @boxinw know.
- `utils.py` provide auxiliary functions   

For other files, please refer to each subdirs for more information. -->

## License
<!-- This project is licensed under the [CC BY-SA 4.0 ]("http://creativecommons.org/licenses/by-sa/4.0/legalcode")  - see the LICENSE file for details. -->

## Citation
Please cite the paper as follows if you use the data or code from 3MAD-28K:
```

```

## Contact
Please reach out to us if you have any questions or suggestions. You can submit an issue or pull request, or send an email to jeix782@gmail.com.

Thank you for your interest in 3MAD-28K. We hope our work will contribute to a more healthcare，expert，trustworthy, fair, and robust AI future.