"""Local contract and analysis CLI. No scanner, model or cloud execution."""
import argparse
import json
from pathlib import Path
from . import __version__
from .contracts import validate, export_protocol, protocol_digest
from .io import ValidationError, load_json, verify_subject, fail, resolve_local

def main(argv=None):
    parser=argparse.ArgumentParser(prog='sb-hybrid',description='Local versioned contracts; imported data is never execution authority.')
    parser.add_argument('--version',action='version',version=__version__)
    sub=parser.add_subparsers(dest='command')
    check=sub.add_parser('validate',help='Validate a JSON contract without network access')
    inputs=check.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--input');inputs.add_argument('--bundle');check.add_argument('--kind');check.add_argument('--as-of')
    check.add_argument('--client-id');check.add_argument('--project-id')
    subject=sub.add_parser('verify-subject',help='Verify every byte bound to a subject manifest')
    subject.add_argument('--input',required=True);subject.add_argument('--client-id',required=True);subject.add_argument('--project-id',required=True)
    export=sub.add_parser('export-protocol',help='Export the pinned data-only security protocol')
    export.add_argument('--output-dir',required=True);export.add_argument('--source-commit',required=True)
    analyze=sub.add_parser('analyze',help='Evaluate a local bundle; never execute infrastructure changes')
    analyze.add_argument('--bundle',required=True);analyze.add_argument('--as-of',required=True);analyze.add_argument('--output-dir',required=True)
    analyze.add_argument('--policy',choices=['offline-demo-1.0.0','strict-analysis-1.0.0'],default='offline-demo-1.0.0')
    analyze.add_argument('--locale',choices=['en'],default='en')
    seal=sub.add_parser('seal-bundle',help='Explicitly refresh input hashes after editing; never produces approval')
    seal.add_argument('--bundle',required=True)
    dossier=sub.add_parser('dossier',help='Render an integrity-verified local result without re-evaluating prices')
    dossier.add_argument('--evaluation',required=True);dossier.add_argument('--output-dir',required=True)
    dossier.add_argument('--locale',choices=['en'],default='en');dossier.add_argument('--audience',choices=['both'],default='both')
    security=sub.add_parser('verify-security',help='Verify a Security Skills review against the original proposal and a trusted external digest')
    security.add_argument('--review-dir',required=True);security.add_argument('--proposal',required=True);security.add_argument('--assessment-sha256',required=True)
    security.add_argument('--client-id',required=True);security.add_argument('--project-id',required=True);security.add_argument('--as-of',required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='validate' and args.bundle:
            from .intake import load_bundle
            b=load_bundle(args.bundle)['bundle']
            if (args.client_id and b['client_id']!=args.client_id) or (args.project_id and b['project_id']!=args.project_id):fail('IDENTITY_MISMATCH','Bundle belongs to another identity')
            print(json.dumps({'valid':True,'scenarios':len(b['scenarios'])}))
        elif args.command in ('validate','verify-subject'):
            p=Path(args.input);doc=load_json(p.parent,p.name)
            validate(doc,expected_kind=getattr(args,'kind',None),client_id=args.client_id,project_id=args.project_id,as_of=getattr(args,'as_of',None))
            if args.command=='verify-subject':verify_subject(p.parent,doc,client_id=args.client_id,project_id=args.project_id)
            print(json.dumps({'valid':True,'kind':doc['kind'],'id':doc['id'],'protocol_sha256':protocol_digest()}))
        elif args.command=='export-protocol':
            export_protocol(args.output_dir,source_commit=args.source_commit)
            print(json.dumps({'exported':True,'protocol_sha256':protocol_digest()}))
        elif args.command=='seal-bundle':
            from .intake import seal_bundle
            seal_bundle(args.bundle);print(json.dumps({'sealed':True,'approval':False}))
        elif args.command=='analyze':
            from .engine import analyze
            from .intake import load_bundle
            from .output import export_analysis
            from .dossier import render
            result=analyze(args.bundle,as_of=args.as_of,policy=args.policy,locale=args.locale)
            export_analysis(load_bundle(args.bundle),result,args.output_dir,render=render)
            print(json.dumps({'generated':True,'output_dir':str(Path(args.output_dir).absolute()),'recommendation':result['payload']['recommendation'],'execution_eligible':False}))
        elif args.command=='dossier':
            from .output import export_analysis,verify_report
            from .intake import load_bundle
            from .dossier import render
            p=Path(args.evaluation)
            if p.name!='evaluation.json':fail('PATH_DENIED','Use evaluation.json inside its complete report directory')
            result=verify_report(p.parent)
            bundles=[a for a in result['payload']['input_manifest'] if a['role']=='input-bundle']
            if len(bundles)!=1:fail('INVALID_SCHEMA','Exactly one original input bundle is required')
            input_path=resolve_local(p.parent/'inputs',bundles[0]['path'])
            export_analysis(load_bundle(input_path),result,args.output_dir,render=render)
            print(json.dumps({'generated':True,'output_dir':str(Path(args.output_dir).absolute()),'recalculated':False}))
        elif args.command=='verify-security':
            from .security_bridge import verify_security
            print(json.dumps(verify_security(args.review_dir,args.proposal,args.assessment_sha256,client_id=args.client_id,project_id=args.project_id,as_of=args.as_of)))
        else:parser.print_help()
        return 0
    except (ValidationError,OSError) as exc:
        print(json.dumps({'valid':False,'error':getattr(exc,'code','LOCAL_IO_ERROR'),'message':str(exc) if isinstance(exc,ValidationError) else 'Local operation failed'}))
        return 2

if __name__=='__main__':raise SystemExit(main())
