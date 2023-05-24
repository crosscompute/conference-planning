import csv
import json
from os import getenv
from pathlib import Path


output_folder = Path(getenv(
    'CROSSCOMPUTE_OUTPUT_FOLDER', 'batches/standard/output'))
datasets_folder = Path('datasets')
runs_folder = datasets_folder / 'runs'


columns = [
    'website_url',
    'subject',
    'start_date',
    'end_date'
    'location',
    'talk_deadline',
    'proposal_url']
rows = []
for run_folder in runs_folder.glob('*'):
    with (run_folder / 'input' / 'variables.dictionary').open('rt') as f:
        d = json.load(f)
    rows.append(list(d.values()))


with (output_folder / 'suggestions.md').open('wt') as f:
    lines = []
    for r in rows:
        [
            website_url,
            subject,
            start_date,
            end_date,
            location,
            talk_deadline,
            proposal_url] = r
        lines.append(
            f'[{subject}]({website_url}) is from {start_date or "?"} to '
            f'{end_date or "?"} in {location or "?"} with proposals due '
            f'{talk_deadline or "?"}')
    f.write('\n'.join(lines))


with (output_folder / 'suggestions.csv').open('wt') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(columns)
    csv_writer.writerows(rows)
