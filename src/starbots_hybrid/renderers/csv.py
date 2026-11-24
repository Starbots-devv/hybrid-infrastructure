"""Spreadsheet-safe CSV; raw canonical values remain in evaluation.json."""
import csv
import io
import unicodedata

def safe_cell(value):
    value=str(value);trimmed=value
    while trimmed and (trimmed[0].isspace() or unicodedata.category(trimmed[0])[0] in 'CZ'):trimmed=trimmed[1:]
    return "'"+value if trimmed.startswith(('=','+','-','@')) else value

def render(result):
    stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n',quoting=csv.QUOTE_ALL)
    writer.writerow(['row_id','scenario_id','view','line_id','resource_id','period','quantity','unit','unit_rate','amount','currency','source_uri','evidence_level'])
    for c in result['payload']['costs']:
        for l in c['lines']:
            values=['|'.join([c['scenario_id'],c['view'],l['id'],l['period']]),c['scenario_id'],c['view'],l['id'],l['resource_id'],l['period'],l['quantity'],l['unit'],l['unit_rate'] if l['unit_rate'] is not None else 'UNKNOWN',l['amount'] if l['amount'] is not None else 'UNKNOWN',c['currency'],l['source_uri'],l['evidence_level']]
            writer.writerow([safe_cell(v) for v in values])
    return stream.getvalue().encode('utf-8')

def cashflow(result):
    """Every displayed monthly amount comes from the canonical EvaluationResult."""
    stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(['scenario_id','view','month','baseline','proposed','saving','cumulative_net'])
    for comparison in result['payload']['comparable_economics']:
        for point in comparison['monthly_series']:
            writer.writerow([safe_cell(value) for value in (
                comparison['scenario_id'],comparison['view'],point['month'],
                point['baseline'],point['proposed'],point['saving'],point['cumulative_net'])])
    return stream.getvalue().encode('utf-8')
