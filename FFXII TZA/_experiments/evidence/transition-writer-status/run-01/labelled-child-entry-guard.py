# ASTRA labelled child-entry substitution: original imported definitions below are unchanged.
if __name__ == '__main__':
    import json,os,sys
    receipt={'argv':sys.argv,'exit_code':int(os.environ['ASTRA_WRITER_CONTROL_EXIT']),'stdout':os.environ['ASTRA_WRITER_CONTROL_STDOUT'],'real_writer_executed':False}
    fp=sys.argv[sys.argv.index('--file')+1]
    receipt['received_op']=json.load(open(fp,encoding='utf-8'))
    json.dump(receipt,open(os.environ['ASTRA_WRITER_CONTROL_RECEIPT'],'w',encoding='utf-8'),indent=2)
    sys.stdout.write(receipt['stdout'])
    sys.exit(receipt['exit_code'])
