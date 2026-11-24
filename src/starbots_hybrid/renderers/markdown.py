"""Escaped Markdown tables. All links are fixed local artifact names."""
import html

def escape(value):
    value=html.escape(str(value),quote=False).replace('\n',' ').replace('\r',' ')
    # Entities avoid executable links/HTML without losing readable row IDs after rendering.
    for ch in ('|','[',']','(',')','`','*','_','\\'):value=value.replace(ch,'&#'+str(ord(ch))+';')
    return value

def render(result,groups,sections=None,executive=False):
    p=result['payload'];out=['# Starbots Hybrid Infrastructure','',escape(p['profile']['payload']['company_name']),'','**SYNTHETIC / ESTIMATED — execution blocked**','', '[Full dossier](dossier.html) · [Canonical JSON](evaluation.json) · [Cost lines](costs.csv)','']
    for s in p['dossier_sections']:
        if sections and s['id'] not in sections:continue
        out.extend(['## '+str(s['id'])+'. '+escape(s['title']),''])
        out.extend(escape(x)+'\n' for x in s['paragraphs'])
        for title,headers,rows in groups[s['id']]:
            if executive and s['id']==8 and 'Comparable' not in title and 'totals' not in title:continue
            out.extend(['### '+escape(title),'','| '+' | '.join(escape(h) for h in headers)+' |','| '+' | '.join('---' for h in headers)+' |'])
            out.extend('| '+' | '.join(escape(c) for c in row)+' |' for row in rows);out.append('')
        if s['id']==4:out.extend(['![Current architecture](architecture-current.svg)','![Proposed architecture](architecture-proposed.svg)',''])
    # Retain raw, safe machine row identifiers in comments for parity checks; IDs are schema constrained.
    for c in p['costs']:
        for l in c['lines']:out.append('<!-- row-id: '+'|'.join([c['scenario_id'],c['view'],l['id'],l['period']])+' -->')
    return ('\n'.join(out)+'\n').encode('utf-8')
