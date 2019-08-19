import json, os
from settings import entity_filenames,\
  entity_directories,\
    selected_entity_keys,\
      entity_sort_on
from utils.file_io import\
  create_workbook,\
    create_worksheet,\
      write_column_headers,\
        write_worksheet_rows
from utils.xlsx_helpers import entity_helpers
from formulas.index import formula_pipelines

def run(entity):
  entity_filename = entity_filenames[entity]
  directory = entity_directories[entity]
  selected_keys = selected_entity_keys[entity]

  workbook = create_workbook(entity_filename)
  worksheet = create_worksheet(workbook)
  write_column_headers(workbook, worksheet, selected_keys)

  filtered_data = []
  file_results = []

  for filename in os.listdir(directory):
    with open(directory + filename) as f:
      if f.name.endswith('.json'):
        file_data = json.loads(f.read())
        file_results = file_results + file_data['results']

  filtered_data, aggregates = entity_helpers[entity](file_results)
  sorted_data = sorted(filtered_data, key=lambda k: k[entity_sort_on[entity]]) 

  row = 1
  for item in sorted_data:
    col = 0
    write_worksheet_rows(workbook, worksheet, selected_keys, item, row, col)
    row += 1

  formula_pipelines[entity](worksheet, workbook, sorted_data, aggregates)

  workbook.close()
