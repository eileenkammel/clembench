#!/bin/bash
# Usage: ./games/multimodal_referencegame/run_refgame.sh

echo
echo "==================================================="
echo "STARTING MULTIMODAL REFERENCE GAME"
echo "==================================================="
echo

game_runs=(
    # P1+2=Model, Both players are the same model
  "multimodal_referencegame gpt-4o-2024-08-06"
  "multimodal_referencegame claude-3-5-sonnet-20240620"
  "multimodal_referencegame gemini-2.0-flash-exp"
  "multimodal_referencegame idefics-80b-instruct"
  "multimodal_referencegame InternVL2-Llama3-76B"
  "multimodal_referencegame InternVL2-40B"
  "multimodal_referencegame InternVL2-8B"
    # P1=Human Expression read from file, P2=Model
  "multimodal_referencegame programmatic gpt-4o-2024-08-06"
  "multimodal_referencegame programmatic claude-3-5-sonnet-20240620"
  "multimodal_referencegame programmatic gemini-2.0-flash-exp"
  "multimodal_referencegame programmatic idefics-80b-instruct"
  "multimodal_referencegame programmatic InternVL2-Llama3-76B"
  "multimodal_referencegame programmatic InternVL2-40B"
  "multimodal_referencegame programmatic InternVL2-8B"
)


echo
echo "==================================================="
echo "STARTING COMMERCIAL MODEL RUNS"
echo "==================================================="
echo
python scripts/cli.py run -g multimodal_referencegame -m gpt-4o-2024-08-06 -l200
python scripts/cli.py run -g multimodal_referencegame -m claude-3-5-sonnet-20240620 -l200
python scripts/cli.py run -g multimodal_referencegame -m gemini-2.0-flash-exp -l200
echo
echo "==================================================="
echo "STARTING OPEN WEIGHT MODEL RUNS"
echo "==================================================="
echo
python scripts/cli.py run -g multimodal_referencegame -m idefics-80b-instruct -l200
python scripts/cli.py run -g multimodal_referencegame -m InternVL2-Llama3-76B -l200
python scripts/cli.py run -g multimodal_referencegame -m InternVL2-40B -l200
python scripts/cli.py run -g multimodal_referencegame -m InternVL2-8B -l200
echo
echo "==================================================="
echo "STARTING COMMERCIAL HUMAN/MODEL RUNS"
echo "==================================================="
echo
python scripts/cli.py run -g multimodal_referencegame -m programmatic gpt-4o-2024-08-06 -l200
python scripts/cli.py run -g multimodal_referencegame -m programmatic claude-3-5-sonnet-20240620 -l200
python scripts/cli.py run -g multimodal_referencegame -m programmatic gemini-2.0-flash-exp -l200
echo
echo "==================================================="
echo "STARTING OPEN WEIGHT HUMAN/MODEL RUNS"
echo "==================================================="
echo
python scripts/cli.py run -g multimodal_referencegame -m programmatic idefics-80b-instruct -l200
python scripts/cli.py run -g multimodal_referencegame -m programmatic InternVL2-Llama3-76B -l200
python scripts/cli.py run -g multimodal_referencegame -m programmatic InternVL2-40B -l200
python scripts/cli.py run -g multimodal_referencegame -m programmatic InternVL2-8B -l200


echo "==================================================="
echo "ALL REFERENCE GAME RUNS COMPLETED"
echo "==================================================="