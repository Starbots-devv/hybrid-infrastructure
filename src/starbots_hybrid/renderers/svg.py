"""Fixed SVG geometry built from typed nodes and edges, never imported markup."""
import html
import textwrap

def render(scenario):
    if scenario is None:return b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 100" role="img"><title>No proposed scenario</title><text x="20" y="50">No eligible provisional alternative</text></svg>'
    edges=scenario['payload']['connection_edges'];connected={e[k] for e in edges for k in ('source','destination')}
    nodes=sorted(scenario['payload']['resource_nodes'],key=lambda n:n['id'] not in connected)
    positions={n['id']:(25+(i%2)*370,100+(i//2)*155) for i,n in enumerate(nodes)}
    legend_y=130+((len(nodes)+1)//2)*155
    height=legend_y+35+25*len(edges)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 {height}" role="img" aria-label="{html.escape(scenario["id"],quote=True)} architecture"><title>{html.escape(scenario["id"])} — declared architecture</title><defs><marker id="arrow-{scenario["id"]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#7658ac"/></marker></defs><rect width="740" height="{height}" fill="#f6f4fa" rx="12"/><text x="25" y="35" font-family="sans-serif" font-size="20" fill="#211635">{html.escape(scenario["id"])} / SYNTHETIC MODEL</text><text x="25" y="62" font-family="sans-serif" font-size="12" fill="#554764">Arrows identify declared dependencies. Connectivity and resilience are unverified.</text>']
    for e in edges:
        x,y=positions[e['source']];dx,dy=positions[e['destination']]
        if y==dy:
            sx,ex=(x+320,dx) if x<dx else (x,dx+320)
            route=f'M {sx} {y+55} L {ex} {dy+55}'
        elif x==dx:
            sy,ey=(y+110,dy) if y<dy else (y,dy+110)
            route=f'M {x+160} {sy} L {dx+160} {ey}'
        else:
            sx,ex=(x+320,dx) if x<dx else (x,dx+320)
            route=f'M {sx} {y+55} L 370 {y+55} L 370 {dy+55} L {ex} {dy+55}'
        out.append(f'<path d="{route}" stroke="#7658ac" stroke-width="2" fill="none" marker-end="url(#arrow-{scenario["id"]})"><title>{html.escape(e["id"])}</title></path>')
    for n in nodes:
        x,y=positions[n['id']];out.append(f'<rect x="{x}" y="{y}" width="320" height="110" rx="9" fill="white" stroke="#c9bedb"/><text x="{x+15}" y="{y+25}" font-family="sans-serif" font-size="15" font-weight="bold" fill="#4e2b7d">{html.escape(n["id"])}</text>')
        for i,line in enumerate(textwrap.wrap(n['service'],width=35)[:3]):out.append(f'<text x="{x+15}" y="{y+49+i*18}" font-family="sans-serif" font-size="12" fill="#30283b">{html.escape(line)}</text>')
    out.append(f'<text x="25" y="{legend_y-5}" font-family="sans-serif" font-size="11" fill="#554764">Unconnected boxes are accounting resources; only declared connections have arrows.</text>')
    for i,e in enumerate(edges):
        legend=e['id']+': '+e['source']+' → '+e['destination']+' / '+e['protocol']+':'+str(e['port'])
        out.append(f'<text x="25" y="{legend_y+22+i*25}" font-family="sans-serif" font-size="12" fill="#30283b">{html.escape(legend)}</text>')
    out.append('</svg>');return ''.join(out).encode('utf-8')
