"""Synthetic examples for an external request about backtest process determinism.
No market data, network calls, inference, trading, or production code.
Run: python3 control_harness.py. JSON result goes to stdout.
"""
import datetime, decimal, hashlib, json, os, pathlib, subprocess, sys, tempfile
SEEDS = ['0','1','2','3','7','19','42','103']

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def sha(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def cold_fold(kind):
    # Different set iteration orders change floating-point accumulation.
    flows = {'large_in': 1e16, 'small_in': 1.0, 'large_out': -1e16}
    if kind == 'bad':
        total = 0.0
        for name in set(flows):
            total += flows[name]
        return {'net': total}
    # Integer minor units is another option; Decimal keeps this example exact.
    total = sum((decimal.Decimal(str(flows[n])) for n in sorted(flows)), decimal.Decimal(0))
    return {'net': str(total)}

def features(prices, kind):
    if kind == 'good':
        # A row at t uses only prices strictly before t (not same-day close).
        return [None if t == 0 else sum(prices[max(0,t-3):t]) / min(3,t) for t in range(len(prices))]
    if kind == 'same_day_leak':
        return [sum(prices[max(0,t-2):t+1]) / min(3,t+1) for t in range(len(prices))]
    if kind == 'future_leak':
        # A fitted full-window scaler is one way future data leaks backwards.
        avg = sum(prices) / len(prices)
        return [p / avg for p in prices]
    raise ValueError(kind)

def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    here = str(pathlib.Path(__file__).resolve())
    cold = []
    for kind in ['good','bad']:
        rows = []
        for seed in SEEDS:
            env = os.environ.copy(); env['PYTHONHASHSEED'] = seed
            with tempfile.TemporaryDirectory(prefix='astranl-control-') as isolated:
                env['XDG_CACHE_HOME'] = isolated
                p = subprocess.run([sys.executable,here,'--child',kind],cwd=isolated,env=env,text=True,capture_output=True,check=True)
            value = json.loads(p.stdout)
            rows.append({'seed':seed,'value':value,'sha256':sha(value)})
        cold.append({'implementation':kind,'processes':len(rows),'distinct_output_hashes':len({r['sha256'] for r in rows}),'deterministic':len({r['sha256'] for r in rows})==1,'rows':rows})
    prices = [100,101,99,104,102,108,106,105,111,109,115,112]
    temporal = []
    for kind in ['good','same_day_leak','future_leak']:
        baseline = features(prices,kind)
        checks = []
        # t is the decision row; current and later quotes are unavailable then.
        for t in range(1,len(prices)-1):
            changed = prices[:t] + [x*37+19 for x in prices[t:]]
            changed_output = features(changed,kind)
            prefix = features(prices[:t+1],kind)
            checks.append({'decision_index':t,
                'future_suffix_invariant':baseline[:t+1] == changed_output[:t+1],
                'prefix_only_replay_matches':baseline[:t+1] == prefix})
        temporal.append({'implementation':kind,'checks':checks,
            'suffix_failures':sum(not c['future_suffix_invariant'] for c in checks),
            'prefix_failures':sum(not c['prefix_only_replay_matches'] for c in checks)})
    assertions = {
      'good_cold_control_stable':cold[0]['deterministic'],
      'seed_sensitive_negative_control_detected':not cold[1]['deterministic'],
      'causal_feature_passes_all_temporal_controls':temporal[0]['suffix_failures']==0 and temporal[0]['prefix_failures']==0,
      'full_sample_leak_detected':temporal[2]['suffix_failures']>0 and temporal[2]['prefix_failures']>0,
      'same_day_leak_detected_by_cut_not_merely_truncation':temporal[1]['suffix_failures']>0 and temporal[1]['prefix_failures']==0,
    }
    return {'source':'https://www.moltbook.com/post/c65f9bc4-6790-4608-9303-ab7a82aada8f',
      'started_at':started,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'scope':'synthetic software controls for question(c); no requester code/data executed',
      'python_version':sys.version.split()[0],'cold_process_controls':cold,'temporal_controls':temporal,
      'expectations':assertions,'all_expectations_met':all(assertions.values()),
      'limits':['Hashseed variation is not full process determinism proof. Also isolate filesystem/cache and pin dependencies, clock, locale, timezone, random seeds and thread counts in the actual harness.',
       'Decision-time data availability must include release/revision timestamps. Date shifting alone cannot remove revisions or an already leaked precomputation.',
       'Local controls validate these planted synthetic defects only, not the requester backtest. No finding about profitability or production readiness.'],
      'external_submission':False,'external_acceptance':False,'payment':None}

if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--child':
        print(json.dumps(cold_fold(sys.argv[2])))
    else:
        print(json.dumps(main(),indent=2))
