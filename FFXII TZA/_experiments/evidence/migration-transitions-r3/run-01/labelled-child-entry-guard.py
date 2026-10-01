# ASTRA labelled child-entry control: normal imported original definitions below unchanged.
if __name__ == '__main__':
    import hashlib,json,os,sys
    from pathlib import Path
    op=json.load(open(sys.argv[sys.argv.index('--file')+1],encoding='utf-8'))
    bp=Path(sys.argv[sys.argv.index('--board')+1]);before=bp.read_bytes();mode=os.environ['ASTRA_PRIVATE_BOARD_CONTROL']
    if mode != 'none':
        import copy,team
        b=json.loads(before);added=copy.deepcopy(op)
        if mode == 'other': added['task']['id']+='-OTHER'
        team.apply(b,sys.argv[sys.argv.index('--agent')+1],added);team.validate(b)
        bp.write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
    receipt={'argv':sys.argv,'received_op':op,'exit_code':int(os.environ['ASTRA_WRITER_CONTROL_EXIT']),'stdout':os.environ['ASTRA_WRITER_CONTROL_STDOUT'],'real_writer_executed':False,'private_intervention':mode,'board_before_sha256':hashlib.sha256(before).hexdigest(),'board_after_sha256':hashlib.sha256(bp.read_bytes()).hexdigest()}
    json.dump(receipt,open(os.environ['ASTRA_WRITER_CONTROL_RECEIPT'],'w',encoding='utf-8'),indent=2)
    sys.stdout.write(receipt['stdout']);sys.exit(receipt['exit_code'])
