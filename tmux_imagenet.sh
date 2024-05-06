#!/bin/bash

# 定义session名称
SESSION_NAME="NaturalPromptSession"

# 定义splits列表
splits=(
    "train"
    "validation"
    "test"
)

# 创建tmux session
tmux new-session -d -s $SESSION_NAME

# 为每个split创建window并执行命令
for split in "${splits[@]}"
do
    tmux new-window -t $SESSION_NAME -n $split
    tmux send-keys -t $SESSION_NAME:$split 'bash' C-m
    tmux send-keys -t $SESSION_NAME:$split 'conda activate MedicalPrompt' C-m
    tmux send-keys -t $SESSION_NAME:$split "python clipscore_split_nature.py --device 0 --split $split" C-m
done

# 切换到第一个window
tmux select-window -t $SESSION_NAME:0

# 附加到tmux session
tmux attach-session -t $SESSION_NAME

