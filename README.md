# 医学安全性及特异性攻击在医学机器学习语言模型中的应用：详细提纲

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
