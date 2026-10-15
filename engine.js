var InflatorMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  var BACKPRESSURE_NORM = 0.5;
  function fillPlan(flowLpm, psi, tireL) {
    if (!pos(flowLpm)) return { error: "the sticker flow must be above zero" };
    if (!pos(psi)) return { error: "the PSI to add must be above zero" };
    if (!pos(tireL)) return { error: "the tire liters must be above zero" };
    var honestFlow = flowLpm * BACKPRESSURE_NORM;
    var freeAir = tireL * (psi / 14.7);
    var minutes = freeAir / honestFlow;
    var verdict = minutes < 2 ? "a quick top-up"
      : minutes <= 6 ? "a coffee break per tire"
      : "bring a book";
    return { honestFlow: r1(honestFlow), freeAir: r1(freeAir), minutes: r1(minutes), verdict: verdict };
  }
  function renderFill(r, flowLpm, psi, tireL) {
    var word = r.minutes === 1 ? " minute - " : " minutes - ";
    return "The " + jsnum(flowLpm) + "-liter sticker flow honestly moves " + jsnum(r.honestFlow)
      + " liters a minute at the 0.5 back-pressure norm; the " + jsnum(tireL) + "-liter tire takes "
      + jsnum(r.freeAir) + " liters of free air for the " + jsnum(psi) + " PSI, about " + jsnum(r.minutes) + word + r.verdict + ".";
  }
  function dutyPlan(dutyPct, fillMin, tires) {
    if (!pos(dutyPct) || dutyPct > 100) return { error: "the duty percent must sit between zero and 100" };
    if (!pos(fillMin)) return { error: "the minutes per tire must be above zero" };
    if (!pos(tires)) return { error: "the tire count must be above zero" };
    var perWindow = dutyPct / 100 * 10;
    var workMin = tires * fillMin;
    var windows = Math.ceil(workMin / perWindow);
    var sessionMin = workMin + (windows - 1) * (10 - perWindow);
    var verdict = sessionMin <= 15 ? "one honest stretch"
      : sessionMin <= 30 ? "a coffee-and-tires morning"
      : "a patient afternoon";
    return { perWindow: r1(perWindow), workMin: r1(workMin), windows: windows, sessionMin: r1(sessionMin), verdict: verdict };
  }
  function renderDuty(r, dutyPct, fillMin, tires) {
    var w1 = r.perWindow === 1 ? " minute" : " minutes";
    var w2 = r.windows === 1 ? " across 1 window" : " across " + jsnum(r.windows) + " windows";
    var w3 = r.sessionMin === 1 ? " minute all in" : " minutes all in";
    return "At the " + jsnum(dutyPct) + "% duty cycle the pump honestly works " + jsnum(r.perWindow) + w1
      + " in every 10; the " + jsnum(tires) + "-tire job is " + jsnum(r.workMin) + " minutes of work" + w2
      + " - about " + jsnum(r.sessionMin) + w3 + ", " + r.verdict + ".";
  }
  function drawPlan(drawA, refA) {
    if (!pos(drawA)) return { error: "the draw amps must be above zero" };
    if (!pos(refA)) return { error: "the reference amps must be above zero" };
    var pct = drawA / refA * 100;
    return { pct: r1(pct) };
  }
  function renderDraw(r, drawA, refA) {
    return "The " + jsnum(drawA) + "-amp draw is " + jsnum(r.pct) + "% of the " + jsnum(refA)
      + "-amp reference you entered - a share of that number, not a safe-current rating; follow the vehicle outlet limit and the inflator's instructions, and never defeat or oversize a fuse.";
  }
  return { fillPlan: fillPlan, renderFill: renderFill, dutyPlan: dutyPlan, renderDuty: renderDuty, drawPlan: drawPlan, renderDraw: renderDraw };
})();
if (typeof module !== "undefined" && module.exports) module.exports = InflatorMath;
