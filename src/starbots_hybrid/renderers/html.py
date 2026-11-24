"""Self-contained print-ready HTML with a fixed CSP and escaped imported text."""
from html import escape

CSS='''
:root{color-scheme:light;--ink:#241d30;--purple:#6426a3;--muted:#62596e;--line:#ded7e7;--paper:#fff;--wash:#f6f3fa}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--wash);color:var(--ink);font:15px/1.65 Segoe UI,Arial,sans-serif}a{color:var(--purple);text-underline-offset:3px}header{background:#241333;color:#fff;padding:45px max(24px,calc((100vw - 1160px)/2));border-bottom:5px solid #ac7de0}header .brand{letter-spacing:.19em;font-weight:700;font-size:13px;color:#d9bee9}h1{font-size:clamp(30px,4vw,48px);line-height:1.14;font-weight:650;margin:20px 0;max-width:950px}header p{color:#e4dce9;max-width:900px}.tag{display:inline-block;border:1px solid #b28bcc;border-radius:4px;padding:4px 10px;font-size:12px;letter-spacing:.06em}.shell{max-width:1220px;margin:auto;padding:30px;display:grid;grid-template-columns:200px minmax(0,1fr);gap:35px}nav{align-self:start;position:sticky;top:20px;font-size:13px}nav a{display:block;padding:5px 0;text-decoration:none}nav a:hover{text-decoration:underline}main{min-width:0}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0 0 28px}.card{padding:19px;background:#eee6f8;border-top:3px solid var(--purple);border-radius:3px}.card small{display:block;color:var(--muted)}.card strong{font-size:24px;color:#4c187c;overflow-wrap:anywhere}section{background:var(--paper);padding:28px;margin-bottom:22px;border:1px solid var(--line);border-radius:5px;scroll-margin-top:20px}h2{font-size:25px;line-height:1.25;margin:0 0 22px;letter-spacing:-.025em}h2 .number{font-size:13px;color:var(--purple);margin-right:12px}h3{font-size:16px;margin:25px 0 12px}p{margin:0 0 14px;overflow-wrap:anywhere}.table-wrap{width:100%;overflow-x:auto;margin-bottom:20px}table{border-collapse:collapse;width:100%;font-size:12px;table-layout:fixed}caption{text-align:left;font-weight:600;margin-bottom:10px}th{text-align:left;background:#f1ecf6;font-weight:600}td,th{padding:10px 9px;border:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere;white-space:pre-wrap}tr:nth-child(even) td{background:#fcfafd}td:first-child{font-weight:500}.diagram{margin:20px 0}.diagram svg{width:100%;height:auto;max-height:none}footer{font-size:12px;color:var(--muted);padding:10px 0 40px}.notice{border-left:4px solid var(--purple);background:#f5f0fa;padding:14px 18px;margin-bottom:26px}.links{font-size:13px}.status{font-weight:700;color:#6426a3}@media(max-width:800px){.shell{display:block;padding:16px}nav{position:static;display:flex;flex-wrap:wrap;gap:5px 15px;margin-bottom:22px}section{padding:20px}.cards{grid-template-columns:1fr}table{font-size:11px}header{padding:28px 20px}}@media print{@page{size:A4;margin:15mm 12mm}body{background:white;font:10pt/1.4 Arial,sans-serif}header{background:white;color:#211635;padding:0 0 16px;border-bottom:2px solid #6426a3}header p,header .brand{color:#4b3c58}h1{font-size:27pt}.shell{display:block;padding:20px 0}nav,.links{display:none}section{border:0;padding:12px 0;border-radius:0;margin-bottom:10px}h2,h3{break-after:avoid}h2{font-size:18pt}.cards{grid-template-columns:repeat(3,minmax(0,1fr))}.card{padding:10px}table{font-size:8pt;table-layout:fixed}thead{display:table-header-group}tr{break-inside:avoid}td,th{padding:6px;overflow-wrap:anywhere}.table-wrap{overflow:visible}svg{max-height:220mm}.diagram{break-inside:avoid}.notice{padding:9px 12px}a{color:inherit;text-decoration:none}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''
CSP="default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'"
def e(v):return escape(str(v),quote=True)

def shell(title,body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="'+e(CSP)+'"><title>'+e(title)+'</title><style>'+CSS+'</style></head><body>'+body+'</body></html>').encode('utf-8')

def render(result,groups,diagrams):
    p=result['payload'];rec=p['recommendation'];company=p['profile']['payload']['company_name'];dynamic=any(a['role']=='finops-plan' for a in p['input_manifest']);out=['<header><div class="brand">STARBOTS / HYBRID INFRASTRUCTURE</div><h1>'+e(company)+'</h1><span class="tag">'+e(rec['status'])+' · SYNTHETIC · ESTIMATED</span><p>A decision dossier for the business owner and implementation engineer. Analysis as of '+e(p['as_of'])+'.</p></header><div class="shell"><nav aria-label="Dossier sections">']
    for s in p['dossier_sections']:out.append('<a href="#section-'+str(s['id'])+'">'+str(s['id'])+'. '+e(s['title'])+'</a>')
    out.append('</nav><main><div class="notice"><strong>Execution blocked.</strong> All rates and performance observations in the demonstration are synthetic. Mandatory security, load and restoration evidence are pending.</div><div class="cards">')
    selected=rec['scenario_id'];econ=[x for x in p['comparable_economics'] if x['scenario_id']==selected]
    for label,view in [('Monthly cash saving','incremental_cash'),('Monthly TCO saving','allocated_tco')]:
        row=next((x for x in econ if x['view']==view),None)
        out.append('<div class="card"><small>'+label+' / estimated month 1</small><strong>'+e((row['monthly_saving'] or 'UNKNOWN')+' '+row['currency'] if row else 'UNKNOWN')+'</strong><small>'+('36-month modeled series' if dynamic else 'Constant assumptions')+'; review section 8</small></div>')
    row=next((x for x in econ if x['view']=='incremental_cash'),None)
    out.append('<div class="card"><small>One-time migration / training</small><strong>'+e((row['incremental_investment'] or 'UNKNOWN')+' '+row['currency'] if row else 'UNKNOWN')+'</strong><small>No execution authority</small></div></div><p class="links"><a href="executive-summary.md">Executive summary</a> · <a href="implementation-guide.md">Implementation guide</a> · <a href="evaluation.json">Canonical JSON</a> · <a href="costs.csv">Cost CSV</a> · <a href="cashflow.csv">Monthly cash flow CSV</a></p>')
    for s in p['dossier_sections']:
        out.append('<section id="section-'+str(s['id'])+'"><h2><span class="number">'+str(s['id']).zfill(2)+'</span>'+e(s['title'])+'</h2>')
        for paragraph in s['paragraphs']:out.append('<p>'+e(paragraph)+'</p>')
        if s['id']==4:
            for filename in ('architecture-current.svg','architecture-proposed.svg'):out.append('<figure class="diagram">'+diagrams[filename].decode('utf-8')+'<figcaption>'+e(filename)+'</figcaption></figure>')
        for title,headers,rows in groups[s['id']]:
            out.append('<h3>'+e(title)+'</h3><div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>')
            for row in rows:
                row_id=' data-row-id="'+e(row[0])+'"' if headers[0]=='Row ID' else ''
                out.append('<tr'+row_id+'>'+''.join('<td>'+e(c)+'</td>' for c in row)+'</tr>')
            out.append('</tbody></table></div>')
        out.append('</section>')
    out.append('<footer>Starbots · Offline analysis · Integrity is verifiable through artifact-manifest.json. Hashes do not establish authorship or deployment approval.</footer></main></div>')
    return shell('Starbots · Implementation dossier',''.join(out))

def shareable(result):
    p=result['payload'];rec=p['recommendation'];allowed_status=rec['status'] if rec['status'] in ('CONDITIONAL','DEMONSTRATED','NONE') else 'NONE'
    label='SYNTHETIC DEMONSTRATION' if p['synthetic'] else 'UNVERIFIED INPUT MODEL'
    out=['<header><div class="brand">STARBOTS / SHARED SUMMARY</div><h1>Infrastructure decision summary</h1><span class="tag">'+allowed_status+' / '+label+' / ESTIMATED</span></header><div class="shell"><main><section><h2>Limited summary</h2><p>Identifiers and imported free text are omitted by a fixed allowlist. Commercial figures may still be sensitive. Review before sharing; no publication or execution is approved.</p>']
    # Only strict numeric fields and a fixed currency allowlist cross this boundary.
    import re
    for row in p['comparable_economics']:
        if row['scenario_id']!=rec['scenario_id']:continue
        currency=row['currency'] if row['currency'] in ('USD','EUR','GTQ','JPY') else 'UNSUPPORTED'
        out.append('<h3>'+('Cash' if row['view']=='incremental_cash' else 'Allocated TCO')+' / '+currency+'</h3>')
        for field in ('monthly_saving','incremental_investment','net_12_months','net_36_months','break_even_month'):
            value=str(row[field]);value=value if re.fullmatch(r'-?\d+(\.\d+)?',value) else 'UNKNOWN'
            out.append('<p>'+field.replace('_',' ').capitalize()+': '+value+'</p>')
    out.append('</section></main></div>');return shell('Starbots · Shared summary',''.join(out))
