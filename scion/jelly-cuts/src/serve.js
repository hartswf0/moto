// static server rooted at /home/user so /contaminant-jelly/... and /moto/... resolve; supports ranges
const http=require('http'),fs=require('fs'),path=require('path');const root='/home/user',port=+process.argv[2]||8766;
const T={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4','.woff2':'font/woff2'};
http.createServer((q,r)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.stat(f,(e,s)=>{if(e||!s.isFile()){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':T[path.extname(f)]||'application/octet-stream','Content-Length':s.size});fs.createReadStream(f).pipe(r);});}).listen(port);
