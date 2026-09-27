import os,socket,tempfile,urllib.parse,urllib.request,threading,webbrowser,json,math,time
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
PORT=8888
SHORTCUT_NAME="视频分享到小红书"
REMOTE="https://raw.githubusercontent.com/572126160-art/multi-phone-workbench/main/"
TMP=os.path.join(tempfile.gettempdir(),"xhs_multi_phone_online");os.makedirs(TMP,exist_ok=True)
STATE={"phone_count":3,"phones":[[] for _ in range(3)],"progress":[{"done":0} for _ in range(3)]}
CACHE={}
def ip():
 s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 try:s.connect(("8.8.8.8",80));return s.getsockname()[0]
 except:return socket.gethostbyname(socket.gethostname())
 finally:s.close()
LAN=ip()
def remote(name):
 try:
  with urllib.request.urlopen(REMOTE+name+"?t="+str(int(time.time()/60)),timeout=8) as r:
   text=r.read().decode("utf-8");CACHE[name]=text;return text
 except:
  return CACHE.get(name,"<h2>无法获取在线页面，请检查网络后刷新。</h2>")
def reset(n):
 STATE["phone_count"]=n;STATE["phones"]=[[] for _ in range(n)];STATE["progress"]=[{"done":0} for _ in range(n)]
def sc(pi,vi):
 u=f"http://{LAN}:{PORT}/video/{pi}/{vi}"
 return "shortcuts://run-shortcut?"+urllib.parse.urlencode({"name":SHORTCUT_NAME,"input":"text","text":u})
class H(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def out(self,b,ct="text/plain; charset=utf-8",st=200):
  self.send_response(st);self.send_header("Content-Type",ct);self.send_header("Content-Length",str(len(b)));self.send_header("Cache-Control","no-store");self.end_headers();self.wfile.write(b)
 def do_GET(self):
  p=urllib.parse.urlparse(self.path).path
  if p=="/":return self.out(remote("index.html").encode(),"text/html; charset=utf-8")
  if p.startswith("/phone/"):
   try:i=int(p.rsplit("/",1)[1]);html=remote("phone.html").replace("__PHONE_INDEX__",str(i)).replace("__PHONE_NO__",str(i+1));return self.out(html.encode(),"text/html; charset=utf-8")
   except:return self.out(b"bad phone",st=400)
  if p=="/info":
   arr=[]
   for pi,ph in enumerate(STATE["phones"]):
    vs=[{"name":v["name"],"size_mb":round(v["size"]/1048576,1),"shortcut_url":sc(pi,vi),"video_url":f"http://{LAN}:{PORT}/video/{pi}/{vi}"} for vi,v in enumerate(ph)]
    arr.append({"videos":vs,"progress":STATE["progress"][pi]})
   return self.out(json.dumps({"phone_count":STATE["phone_count"],"phones":arr},ensure_ascii=False).encode(),"application/json")
  if p.startswith("/video/"):
   try:_,pi,vi=p.strip("/").split("/");return self.video(int(pi),int(vi))
   except:return self.out(b"bad video",st=400)
  return self.out(b"404",st=404)
 def do_POST(self):
  p=urllib.parse.urlparse(self.path)
  if p.path=="/set_phone_count":
   n=int(self.headers.get("Content-Length","0"));d=json.loads(self.rfile.read(n));c=max(1,min(20,int(d.get("count",1))));reset(c);return self.out(b'{"ok":true}',"application/json")
  if p.path=="/clear":reset(STATE["phone_count"]);return self.out(b'{"ok":true}',"application/json")
  if p.path=="/progress":
   n=int(self.headers.get("Content-Length","0"));d=json.loads(self.rfile.read(n));pi=int(d["phone"]);a=d["action"];pr=STATE["progress"][pi];total=len(STATE["phones"][pi])
   if a=="advance":pr["done"]=min(total,pr["done"]+1)
   elif a=="undo":pr["done"]=max(0,pr["done"]-1)
   elif a=="reset":pr["done"]=0
   return self.out(b'{"ok":true}',"application/json")
  if p.path=="/upload":
   q=urllib.parse.parse_qs(p.query);idx=int(q["index"][0]);total=int(q["total"][0])
   if idx==0:reset(STATE["phone_count"])
   ln=int(self.headers.get("Content-Length","0"));name=os.path.basename(urllib.parse.unquote(self.headers.get("X-Filename","video.mp4")));mime=self.headers.get("X-Mime","video/mp4");ext=os.path.splitext(name)[1] or ".mp4";per=math.ceil(total/STATE["phone_count"]);pi=min(idx//per,STATE["phone_count"]-1);vi=len(STATE["phones"][pi]);path=os.path.join(TMP,f"p{pi}_{vi}_{idx}{ext}")
   with open(path,"wb") as f:
    left=ln
    while left:
     c=self.rfile.read(min(left,1048576))
     if not c:break
     f.write(c);left-=len(c)
   STATE["phones"][pi].append({"path":path,"name":name,"mime":mime,"size":os.path.getsize(path)})
   return self.out(b'{"ok":true}',"application/json")
  return self.out(b"404",st=404)
 def video(self,pi,vi):
  v=STATE["phones"][pi][vi];path=v["path"];size=os.path.getsize(path);self.send_response(200);self.send_header("Content-Type",v["mime"]);self.send_header("Content-Length",str(size));self.send_header("Cache-Control","public,max-age=3600");self.end_headers()
  with open(path,"rb") as f:
   while True:
    c=f.read(1048576)
    if not c:break
    self.wfile.write(c)
if __name__=="__main__":
 print("固定工作台：http://127.0.0.1:8888")
 print("页面会自动从 GitHub 获取最新版。")
 threading.Timer(.6,lambda:webbrowser.open(f"http://127.0.0.1:{PORT}/")).start()
 ThreadingHTTPServer(("0.0.0.0",PORT),H).serve_forever()
