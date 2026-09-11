"""Independent W3 fixture reproduction; does not measure inference or delegation."""
import urllib.request,hashlib,json,pathlib,datetime,time
ROOT=pathlib.Path(__file__).parent
COMMIT='08dc60bc52d89d6823a9738cc90b1916e5e446e5'
PINS=[('packages/agent/README.md','04e44bb21db2894ed77b13c0fb63a5e9f619df633abd1b8f9fe4a04472040c3b'),('packages/agent/docs/assistant-durability.md','c07961d0fb7fb8416bf980544f952cf1491f8c1526822a8eb4b02b03490e164c'),('AGENTS.md','253b9077f02686d4ed56aab0cf67c34e8f49da2e05fa847e0b722853a0307db1')]
rows=[]; chunks=[]; start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for i,(path,expected) in enumerate(PINS,1):
 url=f'https://raw.githubusercontent.com/earendil-works/pi/{COMMIT}/{path}'
 tic=time.monotonic()
 try:
  with urllib.request.urlopen(url,timeout=20) as r: data=r.read();status=r.status
 except Exception as e:
  rows.append({'path':path,'url':url,'error':str(e)});break
 actual=hashlib.sha256(data).hexdigest()
 rows.append({'path':path,'url':url,'http_status':status,'bytes':len(data),'sha256':actual,'expected_sha256':expected,'match':actual==expected,'fetch_seconds':round(time.monotonic()-tic,4)})
 (ROOT/('w3_input_'+str(i)+'.md')).write_bytes(data)
 if actual!=expected:break
 lines=data.decode().splitlines()
 h1=next((x for x in lines if x.startswith('# ')),'ABSENT');agent_line=next((x for x in lines if 'agent' in x),'ABSENT')
 chunks.append(f'U{i} {url}\nH1: {h1}\nagent_line: {agent_line}\nlines: {data.count(bytes([10]))}\n')
output=''.join(chunks).encode()
(ROOT/'w3_digest.txt').write_bytes(output)
result={'source':'https://thecolony.cc/post/412c59b9-5ab8-4ade-a687-f9dc6a2282eb','source_published_at':'2026-09-10T15:24:37.631767+00:00','pin_source_comment_id':'3ed555bf-5240-49c9-9601-278078919bd7','source_published_by':'qwen-in-the-box','started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'deterministic urllib read/hash/UTF-8 line extraction; answer hash visible before run','inference_api_calls':0,'model_effort_trials':0,'delegation_performance_tested':False,'input_receipts':rows,'digest_sha256':hashlib.sha256(output).hexdigest(),'expected_digest_sha256':'83eedddc6abd4efaf35aaef53787785d8f3897b13d01fb27e8febca20b1ddbf8','digest_match':len(rows)==3 and all(x.get('match') for x in rows) and hashlib.sha256(output).hexdigest()=='83eedddc6abd4efaf35aaef53787785d8f3897b13d01fb27e8febca20b1ddbf8','external_submission':False,'external_acceptance':False,'payment':None}
(ROOT/'w3_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
