import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

BACKPRESSURE_NORM=0.5

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

def draw_plan(draw_a,ref_a):
    if not pos(draw_a): return {"error":"the draw amps must be above zero"}
    if not pos(ref_a): return {"error":"the reference amps must be above zero"}
    pct=draw_a/ref_a*100
    return {"pct":r1(pct)}

def render_draw(r,draw_a,ref_a):
    return ("The "+jsnum(draw_a)+"-amp draw is "+jsnum(r["pct"])+"% of the "+jsnum(ref_a)
            +"-amp reference you entered - a share of that number, not a safe-current rating; follow the vehicle outlet limit and the inflator's instructions, and never defeat or oversize a fuse.")

cases=[]
def add(tool,args):
    if tool=="fill": r=fill_plan(*args); fn=render_fill
    elif tool=="duty": r=duty_plan(*args); fn=render_duty
    else: r=draw_plan(*args); fn=render_draw
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(35,12,45),(35,8,45),(20,15,60),(50,10,40),(12,20,55),(30,6,35)]:
    add("fill",a)
for a in [(40,3,4),(25,5,4),(60,2,4),(30,2,2),(50,4,3),(20,3,6)]:
    add("duty",a)
for a in [(10,12),(14,12),(16,12),(8,8),(12,12),(20,16)]:
    add("draw",a)
add("fill",[0,12,45]); add("fill",[35,0,45]); add("fill",[35,12,0])
add("duty",[0,3,4]); add("duty",[110,3,4]); add("duty",[40,0,4]); add("duty",[40,3,0])
add("draw",[0,12]); add("draw",[10,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
