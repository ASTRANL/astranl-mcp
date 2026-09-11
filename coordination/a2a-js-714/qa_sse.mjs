import assert from 'node:assert/strict';
import fs from 'node:fs';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
const source = process.argv[2] || new URL('./interop/a2a-js/src/sse_utils.ts',import.meta.url).pathname;
const { parseSseStream } = await import(pathToFileURL(source));
function reference(text){
 const lines=text.replace(/\r\n|\r/g,'\n').split('\n'); let type='message',data='';const out=[];
 for(const line of lines){if(line===''){if(data){out.push({type,data});type='message';data='';}}else if(line.startsWith('event:'))type=line.slice(6).replace(/^ /,'');else if(line.startsWith('data:')){const value=line.slice(5).replace(/^ /,'');data=data?data+'\n'+value:value;}}
 if(data)out.push({type,data});return out;
}
function response(text,size){const bytes=new TextEncoder().encode(text);let pos=0;return new Response(new ReadableStream({pull(c){if(pos===bytes.length){c.close();return;}c.enqueue(bytes.slice(pos,pos+size));pos=Math.min(pos+size,bytes.length);}}));}
const endings=['\r','\n','\r\n'];const rows=[];
for(let n=0;n<81;n++){let v=n;const sep=[];for(let j=0;j<4;j++){sep.push(endings[v%3]);v=Math.floor(v/3);}
 const text='event: update'+sep[0]+'data: café'+sep[1]+'data: 🌍'+sep[2]+sep[3]+'data: done\r\n\r\n';
 for(const size of [1,3,4096]){const actual=[];for await (const e of parseSseStream(response(text,size)))actual.push(e);let pass=true,error;try{assert.deepEqual(actual,reference(text));}catch(e){pass=false;error=e.message;}rows.push({delimiters:sep,chunk_size:size,pass,...(error?{error}:{})});}
}
let cancel=false;const stream=new ReadableStream({start(c){c.enqueue(new TextEncoder().encode('data: live\r\r'));},cancel(){cancel=true;}});const g=parseSseStream(new Response(stream));
const result=await Promise.race([g.next(),new Promise(r=>setTimeout(()=>r({timeout:true}),1000))]);
const preEOF=result?.value?.data==='live';if(preEOF)await g.return();
const report={source,source_sha256:createHash('sha256').update(fs.readFileSync(source)).digest('hex'),cases:rows.length,passed:rows.filter(r=>r.pass).length,failures:rows.filter(r=>!r.pass),pre_eof_dispatch:preEOF,early_return_cancels:cancel,external_acceptance:false,scope:'Independent mixed-line-ending oracle across UTF-8 byte splits; local regression evidence only.'};
fs.writeFileSync(new URL('./qa_sse_result.json',import.meta.url),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
