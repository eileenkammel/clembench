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

echo
echo "==================================================="
echo "STARTING COMMERCIAL MODEL RUNS"
echo "==================================================="
echo
python scripts/cli.py run -g ground_truth -m gpt-4o-2024-08-06
python scripts/cli.py run -g ground_truth -m claude-3-5-sonnet-20240620
python scripts/cli.py run -g ground_truth -m gemini-2.0-flash-exp
echo
echo "==================================================="
echo "STARTING OPEN WEIGHT MODEL RUNS"
echo "==================================================="
echo
python scripts/cli.py run -g ground_truth -m idefics-80b-instruct
python scripts/cli.py run -g ground_truth -m InternVL2-Llama3-76B
python scripts/cli.py run -g ground_truth -m InternVL2-40B
python scripts/cli.py run -g ground_truth -m InternVL2-8B

echo "==================================================="
echo "ALL GROUND TRUTH GAME RUNS COMPLETED"
echo "==================================================="