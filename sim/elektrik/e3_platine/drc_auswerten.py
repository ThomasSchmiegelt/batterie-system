import json,collections,sys,subprocess,pathlib
O=pathlib.Path('/home/cae/cae_projekte/batterie/e3')
for v in sys.argv[1:]:
    subprocess.run(['/home/cae/hermes/batterie/werkzeuge/kicad-cli.sh','pcb','drc','--severity-all','--format','json','-o',str(O/f'cmu_{v}_drc.json'),str(O/f'cmu_{v}.kicad_pcb')],capture_output=True)
    d=json.load(open(O/f'cmu_{v}_drc.json'))
    print(v,{k:len(d.get(k,[])) for k in ('violations','unconnected_items')},dict(collections.Counter(x['type'] for x in d['violations'])))
    if '-v' in sys.argv:
        for x in d['violations'][:0]: pass
