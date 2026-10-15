import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

BACKPRESSURE_NORM=0.5; FUSE_NORM=0.8

def fill_plan(flow_lpm,psi,tire_l):
    if not pos(flow_lpm): return {"error":"the sticker flow must be above zero"}
    if not pos(psi): return {"error":"the PSI to add must be above zero"}
    if not pos(tire_l): return {"error":"the tire liters must be above zero"}
    honest_flow=flow_lpm*BACKPRESSURE_NORM
    free_air=tire_l*(psi/14.7)
    minutes=free_air/honest_flow
    if minutes<2: verdict="a quick top-up"
    elif minutes<=6: verdict="a coffee break per tire"
    else: verdict="bring a book"
    return {"honestFlow":r1(honest_flow),"freeAir":r1(free_air),"minutes":r1(minutes),"verdict":verdict}

def render_fill(r,flow_lpm,psi,tire_l):
    word=" minute - " if r["minutes"]==1 else " minutes - "
    return ("The "+jsnum(flow_lpm)+"-liter sticker flow honestly moves "+jsnum(r["honestFlow"])
            +" liters a minute at the 0.5 back-pressure norm; the "+jsnum(tire_l)+"-liter tire takes "
            +jsnum(r["freeAir"])+" liters of free air for the "+jsnum(psi)+" PSI, about "+jsnum(r["minutes"])+word+r["verdict"]+".")

def duty_plan(duty_pct,fill_min,tires):
    if not pos(duty_pct) or duty_pct>100: return {"error":"the duty percent must sit between zero and 100"}
    if not pos(fill_min): return {"error":"the minutes per tire must be above zero"}
    if not pos(tires): return {"error":"the tire count must be above zero"}
    per_window=duty_pct/100*10
    work_min=tires*fill_min
    windows=math.ceil(work_min/per_window)
    session_min=work_min+(windows-1)*(10-per_window)
    if session_min<=15: verdict="one honest stretch"
    elif session_min<=30: verdict="a coffee-and-tires morning"
    else: verdict="a patient afternoon"
    return {"perWindow":r1(per_window),"workMin":r1(work_min),"windows":windows,"sessionMin":r1(session_min),"verdict":verdict}

def render_duty(r,duty_pct,fill_min,tires):
    w1=" minute" if r["perWindow"]==1 else " minutes"
    w2=" across 1 window" if r["windows"]==1 else " across "+jsnum(r["windows"])+" windows"
    w3=" minute all in" if r["sessionMin"]==1 else " minutes all in"
    return ("At the "+jsnum(duty_pct)+"% duty cycle the pump honestly works "+jsnum(r["perWindow"])+w1
            +" in every 10; the "+jsnum(tires)+"-tire job is "+jsnum(r["workMin"])+" minutes of work"+w2
            +" - about "+jsnum(r["sessionMin"])+w3+", "+r["verdict"]+".")

def socket_plan(draw_a,fuse_a):
    if not pos(draw_a): return {"error":"the draw amps must be above zero"}
    if not pos(fuse_a): return {"error":"the fuse amps must be above zero"}
    honest_a=fuse_a*FUSE_NORM
    ratio=draw_a/honest_a
    if ratio<=1: verdict="the socket holds"
    elif ratio<=1.25: verdict="on the edge, keep the engine running"
    else: verdict="blows the fuse"
    return {"honestA":r1(honest_a),"pct":r1(ratio*100),"verdict":verdict}

def render_socket(r,draw_a,fuse_a):
    return ("The "+jsnum(draw_a)+"-amp draw against the "+jsnum(fuse_a)+"-amp fuse's honest "+jsnum(r["honestA"])
            +" amps (the 0.8 norm, labeled) runs at "+jsnum(r["pct"])+"% of the limit - "+r["verdict"]+".")

cases=[]
def add(tool,args):
    if tool=="fill": r=fill_plan(*args); fn=render_fill
    elif tool=="duty": r=duty_plan(*args); fn=render_duty
    else: r=socket_plan(*args); fn=render_socket
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(35,12,45),(35,8,45),(20,15,60),(50,10,40),(12,20,55),(30,6,35)]:
    add("fill",a)
for a in [(40,3,4),(25,5,4),(60,2,4),(30,2,2),(50,4,3),(20,3,6)]:
    add("duty",a)
for a in [(10,15),(14,15),(16,15),(8,10),(12,15),(20,20)]:
    add("socket",a)
add("fill",[0,12,45]); add("fill",[35,0,45]); add("fill",[35,12,0])
add("duty",[0,3,4]); add("duty",[110,3,4]); add("duty",[40,0,4]); add("duty",[40,3,0])
add("socket",[0,15]); add("socket",[10,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
