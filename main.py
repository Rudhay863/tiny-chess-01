import json as j,os,urllib.request as u
U=os.environ["MAKEFUN_ENV_URL"]
def post(p,d):
 with u.urlopen(U+p,j.dumps(d).encode())as f:return j.load(f)
A="abcdefgh"
PC="PNBRQKpnbrqk"
M=[0,100,320,330,500,900,0]
T=["a"*32,"aaaabcc]b`_aaaaebbcfccegkkkkaaaa","WY[[Y]ab[bcd[ade[bde[acdY]aaWY[[","]____baa_ccc_acc_bbc_abc_aaa]___","aaab`aaa`aaa`aaa`aaa`aaabcccaaaa","]__`_aba_bbbaabb`abb_abb_aaa]__`","egcaeeaa_]]]][[Y[YYW[YYW[YYW[YYW"]
W=[[M[a]+(ord(T[a][r*4+min(f,7-f)])-97)*5 for r in range(8)for f in range(8)]for a in range(7)]
KD=(-17,-16,-15,-1,1,15,16,17)
ND=(-33,-31,-18,-14,14,18,31,33)
BD=(-17,-15,15,17)
RD=(-16,-1,1,16)
C=[15]*128
C[0],C[7],C[112],C[119]=13,14,7,11
b=[0]*128
K={1:4,-1:116}
D=Exception
KL=[0]*128
def parse(f):
 global turn,cast,ep
 p=f.split()
 b[:]=[0]*128
 s=112
 for ch in p[0]:
  if ch=="/":s-=24
  elif ch.isdigit():s+=int(ch)
  else:
   j=PC.index(ch)
   b[s]=j+1 if j<6 else 5-j
   if j in(5,11):K[1 if j==5 else-1]=s
   s+=1
 turn=2*(p[1]=="w")-1
 cast=sum(1<<i for i in range(4)if "KQkq"[i]in p[2])
 ep=ord(p[3][0])-97+(int(p[3][1])-1)*16 if p[3]!="-" else-1
def atk(s,y):
 for t in(s-17*y,s-15*y):
  if not t&136 and b[t]==y:return 1
 for o in ND+KD:
  t=s+o
  if not t&136 and b[t]==(2*y if o in ND else 6*y):return 1
 for o in BD+RD:
  t=s+o
  while not t&136 and not b[t]:t+=o
  if not t&136 and b[t] in(5*y,3*y if o in BD else 4*y):return 1
 return 0
def gen():
 m=[]
 ap=m.append
 R=6 if turn>0 else 1
 for s in range(128):
  p=b[s]
  if p*turn<=0:continue
  a=p if p>0 else -p
  if a==1:
   d=16*turn
   q=5 if(s>>4)==R else 0
   t=s+d
   if not b[t]:
    ap((s,t,q))
    if(s>>4)==7-R and not b[s+2*d]:ap((s,s+2*d,0))
   for o in(-1,1):
    t=s+d+o
    if t&136:continue
    if b[t]*turn<0 or t==ep:ap((s,t,q))
  else:
   for o in(ND,BD,RD,BD+RD,KD)[a-2]:
    t=s+o
    while not t&136 and b[t]*turn<=0:
     ap((s,t,0))
     if b[t]or a%4==2:break
     t+=o
 z=4 if turn>0 else 116
 for H,E,G in(((1 if turn>0 else 4),1,3),((2 if turn>0 else 8),-1,-4)):
  if cast&H and b[z+G]==4*turn and all(not b[z+i*E]for i in(1,2,3)if E<0 or i<3)and all(not atk(z+i*E,-turn)for i in(0,1,2)):ap((z,z+2*E,0))
 return m
def make(mv):
 global cast,ep,turn
 f,t,pr=mv
 p=b[f]
 cap=b[t]
 oc,oe,ep=cast,ep,-1
 e=0
 if p==turn:
  if t==oe:
   b[t-16*turn]=0
   e=1
  elif abs(t-f)==32:ep=f+16*turn
 b[t]=pr*turn if pr else p
 b[f]=0
 if p==6*turn:
  K[turn]=t
  if abs(t-f)==2:
   rf=t+1 if t>f else t-2
   rt=(f+t)//2
   b[rt]=b[rf]
   b[rf]=0
 nc=cast
 if p==6*turn:nc&=12 if turn>0 else 3
 nc&=C[f]&C[t]
 cast=nc
 turn=-turn
 return(f,t,pr,cap,oc,oe,e)
def unmake(u):
 global cast,ep,turn
 f,t,pr,cap,oc,oe,e=u
 p=b[t]
 turn=-turn
 b[f]=turn if pr else p
 b[t]=cap
 if e:b[t-16*turn]=-turn
 if p==6*turn:
  K[turn]=f
  if abs(t-f)==2:
   rt=(f+t)//2
   rf=t+1 if t>f else t-2
   b[rf]=b[rt]
   b[rt]=0
 cast,ep=oc,oe
def ev():
 e=0
 for s in range(128):
  p=b[s]
  if p:
   i=s-(s>>4)*8
   e+=W[p][i]if p>0 else-W[-p][i^56]
 return e
def sr(d,a,be,pl):
 global N
 N+=1
 if N>1e5:raise D
 q=not d and not atk(K[turn],-turn)
 if q:
  s=ev()*turn
  if s>=be:return be
  if s>a:a=s
 ms=gen()
 if q:ms=[m for m in ms if b[m[1]]or m[1]==ep]
 ms.sort(key=lambda m:-(m==KL[pl])*9999-M[abs(b[m[1]])])
 n=0
 for m in ms:
  u=make(m)
  if atk(K[-turn],turn):
   unmake(u)
   continue
  n+=1
  v=-sr(max(d-1,0),-be,-a,pl+1)
  unmake(u)
  if v>=be:KL[pl]=m;return be
  if v>a:a=v
 if not n:return-99999+pl if atk(K[turn],-turn)else(d==0)*a
 return a
def choose(fen,legal):
 parse(fen)
 global N
 N=0
 ms=[(0,(ord(m[0])-97+(ord(m[1])-49<<4),ord(m[2])-97+(ord(m[3])-49<<4),PC.index(m[4])-5 if len(m)==5 else 0))for m in legal]
 best=ms[0][1]
 try:
  for d in range(99):
   sc=[]
   for _,m in ms:
    u=make(m);v=-sr(d-1,-10**9,10**9,1);unmake(u);sc.append((v,m))
   sc.sort(reverse=True)
   best=sc[0][1]
   ms=sc
 except D:pass
 f,t,pr=best
 return A[f&7]+str(f//16+1)+A[t&7]+str(t//16+1)+("nbrq"[pr-2]if pr else"")
while(g:=post("/game",{}))["status"]!="done":
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
