#!/bin/bash
# Usage: ./games/multimodal_referencegame/run_refgame.sh

echo
echo "==================================================="
echo "STARTING MULTIMODAL REFERENCE GAME"
echo "==================================================="
echo

game_runs=(
    # Both players are the same model
  "multimodal_referencegame gpt-4o-2024-08-06"
  "multimodal_referencegame claude-3-5-sonnet-20240620"
  "multimodal_referencegame gemini-2.0-flash-exp"
  "multimodal_referencegame idefics-80b-instruct"
  "multimodal_referencegame InternVL2-Llama3-76B"
  "multimodal_referencegame InternVL2-40B"
  "multimodal_referencegame InternVL2-8B"
    # P1=Human Expression, P2=Model
  "multimodal_referencegame programmatic gpt-4o-2024-08-06"
  "multimodal_referencegame programmatic claude-3-5-sonnet-20240620"
  "multimodal_referencegame programmatic gemini-2.0-flash-exp"
  "multimodal_referencegame programmatic idefics-80b-instruct"
  "multimodal_referencegame programmatic InternVL2-Llama3-76B"
  "multimodal_referencegame programmatic InternVL2-40B"
  "multimodal_referencegame programmatic InternVL2-8B"
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
echo "ALL REFERENCE GAME RUNS COMPLETED"
echo "==================================================="