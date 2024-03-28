'''A main script to run attack for LLMs.'''
import time
import importlib
import numpy as np
import torch.multiprocessing as mp
from absl import app
from ml_collections import config_flags

from llm_attacks import get_goals_and_targets, get_workers

_CONFIG = config_flags.DEFINE_config_file('config')

# Function to import module at the runtime
def dynamic_import(module):
    return importlib.import_module(module)

def main(_):#控制整个流程的主函数

    mp.set_start_method('spawn')
    #让新创建的子进程使用spawn
    #在父进程中通过派生一个新的解释器进程来创建子进程
    params = _CONFIG.value
    #将配置文件读入，稍后跑

    attack_lib = dynamic_import(f'llm_attacks.{params.attack}')
    #动态导入对应的类，这里是gcg_attack.py
    print(params)

    #得到输入的话（goals） 和 期望大模型回答的目标（targets），data的路径由behavior或者string控制
    train_goals, train_targets, test_goals, test_targets = get_goals_and_targets(params)

    process_fn = lambda s: s.replace('Sure, h', 'H')
    process_fn2 = lambda s: s.replace("Sure, here is", "Sure, here's")
    #第一个匿名函数 process_fn 接受一个字符串 s，并返回将字符串中的 'Sure, h' 替换为 'H' 的结果。
    #第二个匿名函数 process_fn2 接受一个字符串 s，并返回将字符串中的 'Sure, here is' 替换为 "Sure, here's" 的结果。
    train_targets = [process_fn(t) if np.random.random() < 0.5 else process_fn2(t) for t in train_targets]
    test_targets = [process_fn(t) if np.random.random() < 0.5 else process_fn2(t) for t in test_targets]
    #train_targets 和 test_targets 的处理：这两行代码使用了列表推导式，对训练集和测试集中的目标数据进行了处理。每个目标数据都会根据一个随机的概率进行处理，这个概率是通过 np.random.random() 函数生成的随机数，如果生成的随机数小于 0.5，则使用 process_fn 函数处理目标数据，否则使用 process_fn2 函数处理目标数据。这样做的目的可能是为了在训练和测试过程中对目标数据进行一定的随机变换，以增加数据的多样性或模型的鲁棒性。
    workers, test_workers = get_workers(params)#返回装有ModelWorker实例的列表
    #每个实例有这些的信息：params.model_paths[i],params.model_kwargs[i],tokenizers[i],conv_templates[i],params.devices[i]
    #con_template指的是对话模板
    managers = {
        "AP": attack_lib.AttackPrompt,
        "PM": attack_lib.PromptManager,
        "MPA": attack_lib.MultiPromptAttack,
    }
    #from .gcg_attack import GCGAttackPrompt as AttackPrompt  实际上就是这些类的别称
    # from .gcg_attack import GCGPromptManager as PromptManager
    # from .gcg_attack import GCGMultiPromptAttack as MultiPromptAttack

    timestamp = time.strftime("%Y%m%d-%H:%M:%S")
    if params.transfer:
        attack = attack_lib.ProgressiveMultiPromptAttack(
            train_goals,
            train_targets,
            workers,
            progressive_models=params.progressive_models,
            progressive_goals=params.progressive_goals,
            control_init=params.control_init,
            logfile=f"{params.result_prefix}_{timestamp}.json",
            managers=managers,
            test_goals=test_goals,
            test_targets=test_targets,
            test_workers=test_workers,
            mpa_deterministic=params.gbda_deterministic,
            mpa_lr=params.lr,
            mpa_batch_size=params.batch_size,
            mpa_n_steps=params.n_steps,
        )
    else:
        attack = attack_lib.IndividualPromptAttack(#在attack_manager这个类里面
            train_goals,
            train_targets,
            workers,
            control_init=params.control_init,
            logfile=f"{params.result_prefix}_{timestamp}.json",
            managers=managers,
            test_goals=getattr(params, 'test_goals', []),
            test_targets=getattr(params, 'test_targets', []),
            test_workers=test_workers,
            mpa_deterministic=params.gbda_deterministic,
            mpa_lr=params.lr,
            mpa_batch_size=params.batch_size,
            mpa_n_steps=params.n_steps,
        )
    attack.run(
        n_steps=params.n_steps,
        batch_size=params.batch_size, 
        topk=params.topk,
        temp=params.temp,
        target_weight=params.target_weight,
        control_weight=params.control_weight,
        test_steps=getattr(params, 'test_steps', 1),
        anneal=params.anneal,
        incr_control=params.incr_control,
        stop_on_success=params.stop_on_success,
        verbose=params.verbose,
        filter_cand=params.filter_cand,
        allow_non_ascii=params.allow_non_ascii,
    )#返回return self.control, n_steps，但是这里好像没有接收？

    for worker in workers + test_workers:
        worker.stop()
#调用的是这个函数
if __name__ == '__main__':
    app.run(main)