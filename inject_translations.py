import csv
import json
from pathlib import Path
import argparse
import re
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def load_translation_csv(csv_path):
	translations = {}
	with open(csv_path, encoding='utf-8-sig') as f:
		reader = csv.DictReader(f)
		for row in reader:
			key = row.get('key')
			translation = row.get('translation', '').strip()
			content = row.get('content', '').strip()
			if key and translation and translation != content:
				translations[key] = {
					'file': row['file'],
					'line': int(row['line']),
					'type': row['type'],
					'origin': content,
					'translation': translation
				}
	return translations

def load_translation_json(json_path):
	translations = {}
	with open(json_path, encoding='utf-8-sig') as f:
		data = json.load(f)
		for row in data:
			key = row.get('key')
			translation = row.get('translation', '').strip()
			content = row.get('content', '').strip()
			if key and translation and translation != content:
				translations[key] = {
					'file': row['file'],
					'line': int(row['line']),
					'type': row['type'],
					'origin': content,
					'translation': translation
				}
	return translations

def inject_translation_to_file(src_path, injects, backup=True):
	src_file = Path(src_path)
	if not src_file.exists():
		print(f"[Warning] File not found: {src_path}")
		return 0

	if backup:
		backup_path = src_file.with_suffix(src_file.suffix + ".bak")
		shutil.copy2(src_file, backup_path)
	with open(src_file, encoding='utf-8') as f:
		lines = f.readlines()
	modified = False
	for inj in injects:
		idx = inj['line'] - 1  # 0-based index
		if idx < 0 or idx >= len(lines):
			continue
		line = lines[idx]
		pattern = None
		replacement = None

		if src_file.suffix == '.xaml':
			pattern = fr'({inj["type"]})="([^"]*)"'
			def replacer(m):
				if m.group(1) == inj["type"] and m.group(2) == inj["origin"]:
					return f'{m.group(1)}="{inj["translation"]}"'
				else:
					return m.group(0)
			new_line = re.sub(pattern, replacer, line)
			if new_line != line:
				lines[idx] = new_line
				modified = True

		elif src_file.suffix == '.cs':
			if inj["type"] in ["MessageBoxService.Show", "Logger.Instance.Info", "SetText", "SetTitle", "SetHeader"]:
				pattern = fr'({re.escape(inj["type"])})\s*\(\s*("|\')({re.escape(inj["origin"])})("|\')'
				def replacer(m):
					return f'{m.group(1)}({m.group(2)}{inj["translation"]}{m.group(4)}'
				new_line = re.sub(pattern, replacer, line)
				if new_line != line:
					lines[idx] = new_line
					modified = True
			else:
				pattern = fr'(\.Text|\s+Text\s*=\s*)\s*("|\')({re.escape(inj["origin"])})("|\')'
				def replacer(m):
					return f'{m.group(1)}{m.group(2)}{inj["translation"]}{m.group(4)}'
				new_line = re.sub(pattern, replacer, line)
				if new_line != line:
					lines[idx] = new_line
					modified = True
	if modified:
		with open(src_file, 'w', encoding='utf-8') as f:
			f.writelines(lines)
		print(f"[OK] Translated: {src_path}")
		return 1
	else:
		return 0

def main():
	parser = argparse.ArgumentParser(description='Automatically inject translations into source files')
	parser.add_argument('-t', '--translated', default='translated_content.csv', help='Translation file (csv or json)')
	parser.add_argument('--no-backup', action='store_true', help='Do not backup original files')
	args = parser.parse_args()

	translated_path = Path(args.translated)
	if translated_path.suffix == '.csv':
		translations = load_translation_csv(translated_path)
	elif translated_path.suffix == '.json':
		translations = load_translation_json(translated_path)
	else:
		print("Only csv/json format is supported.")
		return

	groups = {}
	for key, row in translations.items():
		groups.setdefault(row['file'], []).append(row)

	total = 0
	for file_path, injects in groups.items():
		clean_path = file_path.replace("\\", "/")
		full_path = (PROJECT_ROOT / clean_path).resolve()
		print(f"Trying to inject: {full_path}   (exists={full_path.exists()})")
		cnt = inject_translation_to_file(full_path, injects, backup=not args.no_backup)
		total += cnt

	print(f"\nSuccessfully injected translations and modified {total} files.")

if __name__ == "__main__":
	main()