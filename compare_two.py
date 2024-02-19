import glob
import os
import webbrowser
from datetime import time
from random import shuffle
from time import sleep

import numpy as np

from flask_app import app

import threading
import urllib.parse


def launch_compare_web(algo_0_path, algo1_path, algo2_path):
    algo_0_encoded = urllib.parse.quote(algo_0_path)
    algo1_encoded = urllib.parse.quote(algo1_path)
    algo2_encoded = urllib.parse.quote(algo2_path)

    webbrowser.open(f"http://127.0.0.1:5000/compare/{algo_0_encoded}/{algo1_encoded}/{algo2_encoded}")

def compare_two(save_as, directory, experiment1, experiment2):
    # for f in *.zip; do unzip "$f"; done
    experiment1_files = glob.glob(f"{directory}{experiment1}")
    experiment2_files = glob.glob(f"{directory}{experiment2}")
    experiment0 = glob.glob(f"{directory}piece_to_infilling_*.mid")
    # given data/5/algorithm1piano_10_5_5million_basic.mid extract 5
    experiment1_samples = {int(x.split('/')[-1].split('_')[2]): x for x in experiment1_files}
    experiment1_samples = {int(x.split('/')[-1].split('_')[2]): x for x in experiment1_files}
    experiment2_samples = {int(x.split('/')[-1].split('_')[2]): x for x in experiment2_files}
    experiment0_samples = {int(x.split('/')[-1].split('_')[3][:-4]): x for x in experiment0}
    index_data = {sample: {'ex0': experiment0_samples[sample],
                           "ex1": experiment1_samples[sample],
                           "ex2": experiment2_samples[sample]}
                  for sample in experiment1_samples.keys()}
    results = {}
    for sample, experiments in index_data.items():
        print(sample)
        case1 = experiments["ex1"]
        case2 = experiments["ex2"]
        # random list with two experiments
        cases = [(experiment1, case1), (experiment2, case2)]
        # random shufle from random library
        shuffle(cases)
        randomint = np.random.randint(0, 100000)
        os.system(f"cp {experiments['ex0']} static/piece_{randomint}.mid")
        os.system(f"cp {cases[0][1]} static/one_{randomint}.mid")
        os.system(f"cp {cases[1][1]} static/two_{randomint}.mid")
        cases = [("tie", "")] + cases + [("bad", "")]
        launch_compare_web(f"piece_{randomint}.mid", f"one_{randomint}.mid", f"two_{randomint}.mid")
        election = input("Which one is better? (0(tie)/1/2/3(bad file) to hear another time): ")
        add = ""
        if election.lower() == "q":
            election = "1"
            add = "_soft"
        elif election.lower() == "w":
            election = "2"
            add = "_soft"

        # save in results
        real_election = cases[int(election)][0] + add
        results[sample] = real_election
        print(real_election)
    # save results in a csv
    with open(f"{save_as}_results_comparing_{experiment1}_{experiment2}.csv", "w") as f:
        for sample, result in results.items():
            f.write(f"{sample},{result}\n")

    # experiment1 elections
    print(f"{experiment1}: {len([x for x in results.values() if x == experiment1])}")
    # experiment2 elections
    print(f"{experiment2}: {len([x for x in results.values() if x == experiment2])}")
    # tie elections
    print(f"Tie: {len([x for x in results.values() if x == 'tie'])}")
    # bad formatted files
    print(f"Bad files: {len([x for x in results.values() if x == 'bad'])}")


if __name__ == '__main__':
    compare_two("penha_noisy_real_random", "piano/test_noisy_buena_segment_10_random_improvements/", 'algorithm1*.mid', 'algorithm3*.mid')
