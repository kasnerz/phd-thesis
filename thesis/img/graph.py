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


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_file", type=str, default="Rel2text - Results - manual.csv", help="Input file")
    parser.add_argument("--out_file", type=str, default="graph.pdf", help="Output file")

    args = parser.parse_args()
    logger.info(args)
    random.seed(42)
    np.random.seed(42)

    experiments = [
        "rel2text/seed_1",
        "webnlg/seed_1",
        "kelm",
        "rel2text_desc_concat/seed_1",
        "rel2text_fewshot100/seed_1",
        "rel2text_mask_mask/seed_1",
    ]

    error_categories = ["DIR", "LIT", "LEX", "SEM"]

    csv = pd.read_csv(args.in_file, sep=",")
    errs = {err: {"ENT": [], "DESC": [], "ENT+DESC": [], "OK": []} for err in error_categories}

    ids = csv.query(f'`ENT`=="x" and `DESC`!="x"').id.tolist()
    print(f"ENT: {len(ids)} examples ({ids})")
    ids = csv.query(f'`ENT`!="x" and `DESC`=="x"').id.tolist()
    print(f"DESC: {len(ids)} examples ({ids})")
    ids = csv.query(f'`ENT`=="x" and `DESC`=="x"').id.tolist()
    print(f"ENT+DESC: {len(ids)} examples ({ids})")

    # the errors are marked only once, copy them out to all the related examples
    for col in ["ENT", "DESC"]:
        ids = csv.query(f'`{col}`=="x"').id.tolist()

        csv.loc[csv["id"].isin(ids), col] = "x"

    for experiment in experiments:
        for err in errs.keys():
            # count = csv[csv["experiment"]==experiment][err].count()
            # errs[err].append(count)
            exp_examples = csv[csv["experiment"] == experiment]

            errs[err]["ENT"].append(len(exp_examples.query(f'`ENT`=="x" and `DESC`!="x" and `{err}`=="x"')))
            errs[err]["DESC"].append(len(exp_examples.query(f'`DESC`=="x" and `ENT`!="x" and `{err}`=="x"')))
            errs[err]["ENT+DESC"].append(len(exp_examples.query(f'`DESC`=="x" and `ENT`=="x"  and `{err}`=="x"')))
            errs[err]["OK"].append(len(exp_examples.query(f'`DESC`!="x" and `ENT`!="x"  and `{err}`=="x"')))

    plt.rc("font", **{"family": "sans-serif", "sans-serif": ["Nimbus Sans"]})
    plt.rcParams["hatch.linewidth"] = 0.25
    # fig, axs = plt.subplots(2, 4, figsize=(14, 5), frameon=False)

    fig = plt.gcf()
    fig.set_size_inches(6, 3)
    fig.tight_layout()

    x_axis = np.arange(len(experiments))

    ax = fig.gca()

    colors = {"DIR": "#B7B7B8", "LIT": "#FED766", "LEX": "#2AB7CA", "SEM": "#FE4A49"}

    print(experiments)

    table_out = []
    table_ent_only = []
    table_desc_only = []
    table_ent_desc = []

    for i, (err, values) in enumerate(errs.items()):
        color = colors[err]

        ent_desc_cnts = np.array(values["ENT+DESC"], dtype=int)
        table_ent_desc.append(ent_desc_cnts)
        cumsum = ent_desc_cnts.copy()

        desc_cnts = np.array(values["DESC"], dtype=int)
        table_desc_only.append(desc_cnts)
        cumsum += desc_cnts
        ax.bar(x_axis - 0.3 + (0.2 * i), cumsum, color=color, width=0.2, alpha=0.99, label=err, hatch="//")

        ent_cnts = np.array(values["ENT"], dtype=int)
        table_ent_only.append(ent_cnts)

        ok_cnts = np.array(values["OK"], dtype=int)
        chart_values_ok = ent_cnts + ok_cnts
        ax.bar(x_axis - 0.3 + (0.2 * i), chart_values_ok, color=color, width=0.2, alpha=0.99, label=err, bottom=cumsum)

        table_out.append(ent_desc_cnts + desc_cnts + ent_cnts + ok_cnts)

    table_out = np.transpose(np.array(table_out))
    table_ent_only = np.transpose(np.array(table_ent_only))
    table_desc_only = np.transpose(np.array(table_desc_only))
    table_ent_desc = np.transpose(np.array(table_ent_desc))

    for x in range(len(table_out)):
        for y in range(len(table_out[0])):
            print(
                f"{table_out[x][y]} \\scriptsize{{({table_ent_only[x][y]},{table_desc_only[x][y]},{table_ent_desc[x][y]})}}",
                end="",
            )

            if y < len(table_out[0]) - 1:
                print(" & ", end="")
        print()

        # print(" & ".join([str(y) for y in x]))

    experiments_labels = {
        "rel2text/seed_1": "BART$_R$",
        "webnlg/seed_1": "BART$_W$",
        "kelm": "BART$_K$",
        "rel2text_fewshot100/seed_1": "fewshot-100",
        "rel2text_mask_mask/seed_1": "mask-all",
        "rel2text_desc_concat/seed_1": "desc-cat",
    }
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    plt.xticks(x_axis, [experiments_labels[x] for x in experiments], fontsize=8)
    # ax.xaxis.label.set_size(10)

    from matplotlib.patches import Patch

    legend = []
    for err, color in colors.items():
        p = Patch(facecolor=color, label=err)
        legend.append(p)

    legend.append(Patch(facecolor="white", alpha=0.99, label="LBL", hatch="////"))
    # legend.append(Patch(facecolor="white", label="ok"))

    plt.legend(handles=legend)

    # plt.legend()
    fig.savefig(args.out_file, bbox_inches="tight")
