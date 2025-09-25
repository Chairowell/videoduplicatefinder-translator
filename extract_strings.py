from pathlib import Path
import re
import csv
import json
import argparse
from colorama import init, Back

init(autoreset=True)

base_dir = Path(__file__).resolve().parent.parent
PATTERNS = [
	"VDF.GUI/Views/**/*.xaml",
	"VDF.GUI/Styles/**/*.xaml",
	"VDF.GUI/ViewModels/**/*.cs",
	"VDF.GUI/Utils/**/*.cs",
]

def get_files():
	files = []
	for pattern in PATTERNS:
		files.extend(base_dir.glob(pattern))
	return files

def extract_content(file_path):
	file_ext = file_path.suffix
	content = file_path.read_text(encoding='utf-8', errors='ignore').splitlines()
	extracted = []
	if file_ext == '.xaml':
		regex = re.compile(r'(Title|Text|Content|Header|Description|ToolTip\.Tip|Validation\.ErrorTemplate)="([^"]{1,120})"')
		for idx, line in enumerate(content, 1):
			for m in regex.finditer(line):
				extracted.append({
					'file': str(file_path.relative_to(base_dir)),
					'line': idx,
					'type': m.group(1),
					'content': m.group(2)
				})
	elif file_ext == '.cs':
		regexes = [
			re.compile(r'\b(MessageBoxService\.Show|Logger\.Instance\.Info|SetText|SetTitle|SetHeader)\s*\(\s*(@"?)([^"\']{1,120})\2'),
			re.compile(r'(\.Text|\s+Text\s*=\s*)\s*("|\')([^"\']{1,120})\2')
		]
		for idx, line in enumerate(content, 1):
			for regex in regexes:
				for m in regex.finditer(line):
					extracted.append({
						'file': str(file_path.relative_to(base_dir)),
						'line': idx,
						'type': m.group(1).strip(),
						'content': m.group(3)
					})
	return extracted

def load_existing_translations(csv_path):
	translation_dict = {}
	if csv_path.exists():
		with open(csv_path, encoding='utf-8-sig') as f:
			reader = csv.DictReader(f)
			for row in reader:
				if row.get('key') and row.get('translation'):
					translation_dict[row['key']] = row['translation']
	return translation_dict

def main():
	parser = argparse.ArgumentParser(description='Extract string content from project files')
	parser.add_argument('-o', '--output', choices=['csv', 'json', 'both'], default='both', help='Output format: csv, json or both (default: both)')
	parser.add_argument('--load', help='Load existing translation CSV for incremental translation sync', default='translated_content.csv')
	args = parser.parse_args()
	
	files = get_files()
	all_results = []
	csv_rows = []

	existing_trans = load_existing_translations(Path(args.load))

	for file in files:
		print(Back.LIGHTBLACK_EX + f" Processing {file.relative_to(base_dir)} ")
		results = extract_content(file)
		if results:
			for r in results:
				key = f"{r['file']}:{r['line']}:{r['type']}"
				translation = existing_trans.get(key, "")
				row_data = {
					'key': key,
					'file': r['file'],
					'line': r['line'],
					'type': r['type'],
					'content': r['content'],
					'translation': translation
				}
				csv_rows.append([
					row_data['key'],
					row_data['file'],
					row_data['line'],
					row_data['type'],
					row_data['content'],
					row_data['translation']
				])
				all_results.append(row_data)
			print(Back.GREEN + f" Total: {len(results)} ")
		else:
			print(Back.RED + " No match. ")
		print()

	if args.output in ['csv', 'both']:
		csv_path = Path(__file__).parent / "translate_content.csv"
		with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
			writer = csv.writer(f)
			writer.writerow(['key', 'file', 'line', 'type', 'content', 'translation'])
			writer.writerows(csv_rows)
		print(f"CSV saved: {csv_path}")

	if args.output in ['json', 'both']:
		json_path = Path(__file__).parent / "translate_content.json"
		json.dump(all_results, open(json_path, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=2)
		print(f"JSON saved: {json_path}")

	print(f"\nExtraction completed! Format: {args.output}")

if __name__ == "__main__":
	main()