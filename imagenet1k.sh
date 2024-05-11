export HF_ENDPOINT="https://hf-mirror.com"
echo $HF_ENDPOINT
# 取消代理
unset HF_ENDPOINT
chmod a+x hfd.sh
# 无需申请权限模型
# ./hfd.sh bigscience/bloom  --tool aria2c -x 4
# ./hfd.sh imagenet-1k  --tool aria2c -x 4 
# 需要权限模型
./hfd.sh imagenet-1k  --dataset --tool aria2c -x 4 --hf_username JeixHuang  --hf_token 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