#!/usr/bin/env python3

import os
import argparse
import logging
import json
import pandas as pd
import glob
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    shots = [25, 50, 100, 200]
    res_dir = "fewshot_results"
    metrics = ["bleu", "meteor", "bleurt", "nubia_semsim", "nubia_agree", "nubia_perpl"]
    metrics_labels = ["BLEU", "METEOR", "BLEURT", "SS", "E", "PPL"]

    font = {
            'family':'sans-serif',
            # 'family': ["Times New Roman"],
            # 'sans-serif': ['Nimbus Sans'],
            'sans-serif': ['Fira Sans'],
            # 'weight' : 'bold',
            'size'   : 12
            }

    plt.rc('font', **font)

    sns.set_palette("muted")

    # white background with black grid lines
    sns.set_style("whitegrid")

    fig, axes = plt.subplots(2,3, figsize=(10,7))
    # fig.suptitle('Few-shot results')
    fig.tight_layout()

    fig.subplots_adjust(hspace=0.4)
    
    for i, metric in enumerate(metrics):
        res_all = []
        ax = axes[i//3][i%3]

        ax.set_title(metrics_labels[i],fontweight='bold')

        for shot in shots:
            for seed in range(1,6):
                with open(f"{res_dir}/test_rel2text_fewshot{shot}_seed{seed}_beam1.out.eval.json") as f:
                    j = json.load(f)
                    res_all.append([float(j[metric]), str(shot)])
        
        for seed in range(1,6):
            with open(f"{res_dir}/test_rel2text_seed{seed}_beam1.out.eval.json") as f:
                j = json.load(f)
                res_all.append([float(j[metric]), "full"])
            
        df = pd.DataFrame(res_all, columns=[metric, "shot"]) 
        sns.boxplot(ax=ax, data=df, x="shot", y=metric, linewidth=0.8)
        sns.despine(left=True, bottom=True, right=True, top=True)

        ax.set(xlabel=None)
        ax.set(ylabel=None)

    # fig.show()
    fig.savefig("rel2text-fewshot.pdf", bbox_inches='tight')
