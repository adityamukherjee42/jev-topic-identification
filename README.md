# Jev Topic Identification

Testing [TypeSafe's Jev](https://docs.typesafe.ai) (a System One model) on topic-identification.

## Setup

```bash
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python typesafe-sdk mlflow
```

Add your TypeSafe API key to `.env`:

```
TYPESAFE_API_KEY=your_key_here
```

## Usage

```bash
.venv/bin/python main.py [path/to/dataset.json]
```

Each run prints a per-topic accuracy report and mismatch list, and logs the run to MLflow under the
`jev-topic-detection` experiment (metrics, the dataset used, and mismatches as artifacts).

To compare runs:

```bash
.venv/bin/mlflow ui
```

## Project layout

- `main.py` — entry point: loads a dataset, runs it through Jev, prints the report, logs to MLflow.
- `helpers.py` — dataset loading, question building (Noul primitive), evaluation, and MLflow logging.
- `medical_topic_transcripts*.json` — 12 real doctor/patient dialogues sampled from
  [MTS-Dialog](https://github.com/abachaa/MTS-Dialog), labeled across 12 clinical-note topics
  (chief complaint, history of present illness, past medical/surgical history, etc.). Three
  variants show the effect of tuning the topic instructions:
- `medical_topic_transcripts.json` — baseline wording ("Discussed X").
- `medical_topic_transcripts_primary_focus.json` — reworded to ask whether X was the
  conversation's primary focus, not just mentioned in passing.
- `medical_topic_transcripts_criteria.json` — adds explicit Noul `criteria` (true/false
  boundary descriptions) for the three topics that stayed ambiguous after the wording change.

## Dataset format

```json
{
  "topics": {
    "topic_id": "description used to build the yes/no question"
  },
  "transcripts": [
    {
      "id": "...",
      "title": "...",
      "transcript": "Speaker A: ...\nSpeaker B: ...",
      "topics": { "topic_id": true }
    }
  ]
}
```

A topic entry can also be an object — `{"instructions": "...", "criteria": {"true": "...", "false": "..."}}` —
when the yes/no boundary needs disambiguating.

## Results

| Dataset | Overall accuracy |
|---|---|
| `medical_topic_transcripts.json` (baseline) | 81.9% |
| `medical_topic_transcripts_primary_focus.json` | 86.8% |
| `medical_topic_transcripts_criteria.json` | 90.3% |

The medical dataset's ground truth reflects MTS-Dialog's single primary-section-per-snippet
labeling, so early mismatches were mostly Jev correctly noticing topics that were genuinely
mentioned but weren't the snippet's primary label — tightening the question wording and adding
criteria closed most of that gap.
