#!/bin/bash
# Usage: ./games/ground_truth/run_groundtruth.sh

echo
echo "==================================================="
echo "STARTING GROUND TRUTH GAME"
echo "==================================================="
echo

game_runs=(
  "ground_truth gpt-4o-2024-08-06"
  "ground_truth claude-3-5-sonnet-20240620"
  "ground_truth gemini-2.0-flash-exp"
  "ground_truth idefics-80b-instruct"
  "ground_truth InternVL2-Llama3-76B"
  "ground_truth InternVL2-40B"
  "ground_truth InternVL2-8B"
)

total_runs=${#game_runs[@]}
echo "Number of refgame runs: $total_runs"
current_runs=1
for run_args in "${game_runs[@]}"; do
  echo "Run $current_runs of $total_runs: $run_args"
  bash -c "./run.sh ${run_args}"
  ((current_runs++))
done
echo "==================================================="
echo "ALL GROUND TRUTH GAME RUNS COMPLETED"
echo "==================================================="