#!/bin/bash

# 定义session名称
SESSION_NAME="MedicalPromptSession"

# 定义splits列表
splits=(
    "Dermoscopy_Skin"
    "MRI_Alzheimer"
    "MRI_Brain"
    "Fundus_Retina"
    "Mamography_Breast"
    "OCT_Retina"
    "CT_Chest"
    "CT_Heart"
    "CT_Brain"
    "Xray_Chest"
    "Xray_Skeleton"
    "Xray_Dental"
    "Endoscopy_Gastroent"
    "Ultrasound_Baby"
    "Ultrasound_Breast"
    "Ultrasound_Carotid"
    "Ultrasound_Ovary"
    "Ultrasound_Brain"
)

# 创建tmux session
tmux new-session -d -s $SESSION_NAME

# 为每个split创建window并执行命令
for split in "${splits[@]}"
do
    tmux new-window -t $SESSION_NAME -n $split
    tmux send-keys -t $SESSION_NAME:$split 'bash' C-m
    tmux send-keys -t $SESSION_NAME:$split 'conda activate MedicalPrompt' C-m
    tmux send-keys -t $SESSION_NAME:$split "python clipscore_split.py --device 0 --split $split" C-m
done

# 切换到第一个window
tmux select-window -t $SESSION_NAME:0

# 附加到tmux session
tmux attach-session -t $SESSION_NAME

