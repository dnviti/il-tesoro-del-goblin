def cube(c,r):
    x=c-(r-(r&1))//2; z=r; return x,-x-z,z
def dist(a,b):
    A=cube(*a);B=cube(*b); return max(abs(A[i]-B[i]) for i in range(3))
plan=[('Lia G1',(2,0),(2,2),4),('Marco G1',(7,9),(7,7),3),('Sara G1',(0,5),(4,4),9),
('Lia G2',(2,2),(4,3),2),('Marco G2',(7,7),(5,6),6),('Sara G2',(4,4),(4,6),8),
('Lia G3',(4,3),(5,4),None),('Marco G3',(5,6),(8,5),3),('Sara G3',(4,6),(1,7),None),
('Lia G4',(9,4),(8,1),3),('Marco G4',(8,5),(9,6),None),
('Lia G5',(8,1),(8,5),4),('Marco G5',(9,6),(6,8),None),('Sara->Loc',(1,7),(1,4),None),
('Lia G6',(8,5),(7,5),None),('Marco G6',(6,8),(3,6),None),('Sara G6',(1,4),(2,5),None),
('Lia G7',(7,5),(5,6),None),('Sara G7',(2,5),(3,5),None),('Lia G8',(5,6),(4,7),None),
('Marco resp->cr',(7,0),(3,6),None)]
for n,a,b,m in plan: print(n,a,b,dist(a,b),m)
print('adj sara(4,6)-marco(5,6)',dist((4,6),(5,6)))
print('sara(3,5)-lia(5,6)',dist((3,5),(5,6)),'lia(4,7)-sara(3,5)',dist((4,7),(3,5)))
print('(2,5)-(3,6)',dist((2,5),(3,6)),'(3,5)-(3,6)',dist((3,5),(3,6)))
print('lia(9,4) others', dist((9,4),(5,6)),dist((9,4),(4,6)))
print('----')
for a,b in [((5,6),(1,4)),((9,4),(8,1)),((1,4),(2,4)),((2,7),(0,7)),((8,1),(7,3)),((2,4),(2,2)),((1,6),(1,4)),((7,3),(7,5)),((2,2),(3,6)),((1,4),(2,5)),((7,5),(5,6)),((5,6),(4,6))]: print(a,b,dist(a,b))
both=lambda L:[q for p in L for q in [(p[0],p[1]),(9-p[0],9-p[1])]]
qs=both([(6,0),(8,0),(1,1),(3,1),(6,1),(2,2),(5,2),(8,2),(9,1),(4,3),(7,3),(8,3),(0,3),(2,4),(5,4)])
print('q from (0,7) dist3:',[q for q in qs if dist((0,7),q)==3])
print('ragno (1,7) in qs',(1,7) in qs, (2,4) in qs,(7,5) in qs,(5,6) in qs,(2,2) in qs,(7,3) in qs)
spec=set(qs)|set(both([(4,0),(3,2),(7,4),(4,4),(9,2),(1,4),(4,1),(8,1)]))|{(3,3),(6,3),(3,6),(6,6)}
c=[(x,y) for x in range(10) for y in range(10) if dist((7,0),(x,y))<=6 and dist((x,y),(3,6))==2 and dist((x,y),(4,6))>1 and dist((x,y),(2,5))>1]
print('marco g8 cand',[(p, p in spec) for p in c])
# neighbors path from (4,6) to (1,7)
print('====')
print([(p, p in spec) for p in [(x,y) for x in range(10) for y in range(10)] if dist((7,0),p)==3 and dist(p,(3,6))>=4 and not p in spec])
for a,b in [((3,8),(1,4)),((1,4),(2,2)),((2,7),(3,8)),((4,6),(2,7)),((1,7),(2,7))]: print(a,b,dist(a,b))
