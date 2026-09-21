# The HAMbino Files

A local terminal game for demonstrating prompt injection. The player talks to a
sequence of fictional, Ollama-powered information custodians and tries to make each
one disclose its protected clue before the global 15-prompt limit expires. Five clues
lead from the Godfather's internal codename to their true identity.

## Run

Ollama must be running and the configured model must be installed. This project is
already configured for `qwen3:4b`.

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

At startup, enter the murdered friend's name and choose one of two narrative paths:

- **The Law:** investigate seized HAMbino systems as a junior detective.
- **The Family:** infiltrate the syndicate as an aspiring wire specialist.

For scripted demonstrations, skip those questions with:

```powershell
python app.py --route law --friend-name Maya
```

The interface hides private reasoning blocks that some local thinking models emit.
For `qwen3`, it uses an escaped raw ChatML prompt because some Ollama releases place
reasoning in visible content when `think=False` is used. If the hidden reasoning is
cut off before its closing boundary, the app continues it once from the cutoff; an
unfinished thought is never displayed or scored.
`/help`, `/hint`, `/status`, and `/quit` do not consume the prompt budget. `/hint`
shows the intended injection technique for the active clue without revealing its
value. Oversized prompts
and failed Ollama requests also do not consume a prompt.

## Security model and stages

Only the active clue is placed in the model context. When that value is extracted,
the entire conversation is discarded and a fresh system context is created for the
next secret. A single successful injection therefore cannot dump the full dossier.

Scoring checks only the active clue. Inactive values echoed or hallucinated by the
model are blocked before display, and a value already present in the player's prompt
does not earn credit if the model merely repeats it. The model receives a concise,
high-priority security policy on every new stage.

These boundaries make the activity more resistant, but system prompts are not a
real secret-storage mechanism. This remains an intentionally attackable game.

To keep the activity solvable, every clue has a private, configurable gameplay
weakness. Requests matching that weakness override the character's guard rules. The
default five-stage configuration allows a well-formed prompt to solve each stage in
one attempt.

## Customize the activity

Edit `game.json` to change:

- `player_briefing`: the opening story shown to the player.
- `plot_template`: concise story context sent to the model.
- `secrets`: each protected fact, its internal id, display label, value, hint,
  optional aliases, player-facing attack hint, and private release condition.
- `max_prompts`: the total number of player attempts.
- `guard_instructions`: how difficult and theatrical the AI character should be.
- `model` and `temperature`: the Ollama model and response variability.
- `max_response_tokens`: total generation ceiling, including hidden Qwen reasoning.
- `max_prompt_chars`: player input-length ceiling used to prevent context flooding.

The detector compares normalized assistant output with the active secret, so minor
punctuation or formatting cannot bypass scoring. Secrets typed by the player do not
count; the model must introduce the protected value in its own response.

For a group activity, keep `game.json` away from players because it necessarily
contains the answers. This is an educational, entirely fictional scenario; avoid
using real people, organizations, or operational wrongdoing in the final plot.

## Validate

```powershell
python -m unittest discover -s tests -v
```
