# The Omerta Protocol

A local terminal game for demonstrating simple prompt injection. The player talks
to a fictional organization's Ollama-powered AI assistant and tries to make it
disclose all configured secrets before the prompt limit expires.

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
`/help`, `/status`, and `/quit` do not consume the prompt budget. A failed Ollama
request also does not consume a prompt.

## Customize the activity

Edit `game.json` to change:

- `plot_template`: the final story setup when it is ready.
- `secrets`: each protected fact, its internal id, display label, value, and hint.
- `max_prompts`: the total number of player attempts.
- `guard_instructions`: how difficult and theatrical the AI character should be.
- `model` and `temperature`: the Ollama model and response variability.

The detector compares normalized assistant output with each configured secret, so
minor punctuation or formatting cannot bypass scoring. Secrets typed by the player
do not count; the model has to disclose them in its own response.

For a group activity, keep `game.json` away from players because it necessarily
contains the answers. This is an educational, entirely fictional scenario; avoid
using real people, organizations, or operational wrongdoing in the final plot.

## Validate

```powershell
python -m unittest discover -s tests -v
```
