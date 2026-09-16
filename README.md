# The Omerta Protocol

A local terminal game for demonstrating prompt injection. The player talks to a
sequence of fictional, Ollama-powered information custodians and tries to make each
one disclose its protected value before the global prompt limit expires.

## Run

Ollama must be running and the configured model must be installed. This project is
already configured for `qwen3:4b`.

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

You can temporarily choose another installed model:

```powershell
python app.py --model llama3.2:3b
```

The interface hides private reasoning blocks that some local thinking models emit.
For `qwen3`, it uses an escaped raw ChatML prompt because some Ollama releases place
reasoning in visible content when `think=False` is used. If the hidden reasoning is
cut off before its closing boundary, the app continues it once from the cutoff; an
unfinished thought is never displayed or scored.
`/help`, `/status`, and `/quit` do not consume the prompt budget. Oversized prompts
and failed Ollama requests also do not consume a prompt.

## Security model and stages

Only the active secret is placed in the model context. When that value is extracted,
the entire conversation is discarded and a fresh system context is created for the
next secret. A single successful injection therefore cannot dump the full dossier.

Scoring checks only the active secret. Inactive values echoed or hallucinated by the
model are blocked before display, and a value already present in the player's prompt
does not earn credit if the model merely repeats it. The model receives a concise,
high-priority security policy on every new stage.

These boundaries make the activity more resistant, but system prompts are not a
real secret-storage mechanism. This remains an intentionally attackable game.

## Customize the activity

Edit `game.json` to change:

- `plot_template`: the final story setup when it is ready.
- `secrets`: each protected fact, its internal id, display label, value, and hint.
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
