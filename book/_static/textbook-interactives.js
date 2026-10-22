/* Local teaching demos. Print/no-JS content lives in MyST. */
(() => {
  "use strict";
  const projectionModule = new URL("textbook-3d.mjs", document.currentScript.src);
  const stereoModule = new URL("textbook-stereo.mjs", document.currentScript.src);
  const finalModule = new URL("textbook-final-explorers.mjs", document.currentScript.src);
  const NS = "http://www.w3.org/2000/svg";
  let sequence = 0;
  const pretty = (n) => Number.isFinite(n) ? String(Number(n.toFixed(3))) : "undefined";
  const svgNode = (tag, attrs = {}, text = "") => {
    const node = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([name, value]) => node.setAttribute(name, value));
    if (text) node.textContent = text;
    return node;
  };
  const line = (svg, x1, y1, x2, y2, cls = "demo-grid") =>
    svg.append(svgNode("line", {x1, y1, x2, y2, class: cls}));
  const label = (svg, x, y, text, extra = {}) =>
    svg.append(svgNode("text", {x, y, class: "demo-label", ...extra}, text));
  const dot = (svg, x, y, cls, radius = 5) =>
    svg.append(svgNode("circle", {cx: x, cy: y, r: radius, class: cls}));

  function setup(root, description, fields) {
    const stage = root.querySelector(".interactive-stage");
    const intro = document.createElement("p"); intro.textContent = description;
    const controls = document.createElement("div"); controls.className = "demo-controls";
    const inputs = {};
    fields.forEach(({name, title, min, max, step, value, unit}) => {
      const id = `textbook-demo-${++sequence}`;
      const wrap = document.createElement("div"); wrap.className = "demo-control";
      const lab = document.createElement("label"); lab.htmlFor = id; lab.textContent = title;
      const readout = document.createElement("output"); readout.htmlFor = id;
      const input = document.createElement("input");
      Object.assign(input, {id, type: "range", name, min, max, step, value});
      inputs[name] = input;
      input.addEventListener("input", () => { readout.textContent = `${pretty(+input.value)}${unit}`; });
      readout.textContent = `${pretty(value)}${unit}`;
      lab.append(readout); wrap.append(lab, input); controls.append(wrap);
    });
    const reset = document.createElement("button");
    reset.type = "button"; reset.className = "demo-reset"; reset.textContent = "Reset";
    reset.addEventListener("click", () => fields.forEach(({name, value}) => {
      inputs[name].value = value;
      inputs[name].dispatchEvent(new Event("input", {bubbles: true}));
    }));
    const svg = svgNode("svg", {viewBox: "0 0 720 340", role: "img", class: "demo-svg"});
    const title = svgNode("title", {}, root.getAttribute("aria-label")); svg.append(title);
    const values = document.createElement("p"); values.className = "demo-values";
    values.setAttribute("aria-live", "polite"); values.setAttribute("aria-atomic", "true");
    const scrollHint = document.createElement("p"); scrollHint.className = "demo-scroll-hint";
    scrollHint.textContent = "Swipe the diagram sideways to see both views.";
    stage.append(intro, controls, reset, svg, scrollHint, values);
    return {inputs, svg, values, fields, reset};
  }

  async function projection(root) {
    const {createProjectionExplorer} = await import(projectionModule.href);
    createProjectionExplorer(root);
  }

  function homography(root) {
    const {inputs, svg, values} = setup(root,
      "Change the perspective term p in H = [[1,0,0], [0,1,0], [p,0,1]]. Watch the square become a trapezoid. The four numbered points remain collinear; compare their cross-ratio.",
      [{name: "perspective", title: "Perspective term p", min: -0.8, max: 0.8, step: 0.05, value: 0.5, unit: ""}]);
    const crossRatio = x => ((x[2]-x[0])*(x[3]-x[1]))/((x[2]-x[1])*(x[3]-x[0]));
    const render = () => {
      svg.querySelectorAll(":scope > :not(title)").forEach(n => n.remove());
      const p = +inputs.perspective.value;
      const transform = ([u,v]) => [u/(1+p*u), v/(1+p*u)];
      const points = [-0.75,-0.25,0.25,0.75].map(x => [x,0.3]);
      const corners = [[-1,-1],[1,-1],[1,1],[-1,1]];
      const mapped = corners.map(transform);
      const extent = Math.max(...mapped.flat().map(Math.abs));
      label(svg, 20, 25, "Source plane");
      label(svg, 390, 25, "Destination plane (fit to view)");
      const drawPlane = (centerX, scale, mapping) => {
        const screen = point => { const [u,v] = mapping(point); return [centerX+scale*u,175-scale*v]; };
        const path = points => points.map(screen).map(p => p.join(",")).join(" ");
        for (const t of [-1,-0.5,0,0.5,1]) {
          svg.append(svgNode("polyline", {points: path([[-1,t],[1,t]]), class: "demo-grid", fill: "none"}));
          svg.append(svgNode("polyline", {points: path([[t,-1],[t,1]]), class: "demo-grid", fill: "none"}));
        }
        svg.append(svgNode("polygon", {points: path(corners), class: "demo-boundary"}));
        svg.append(svgNode("polyline", {points: path([[-1,0.3],[1,0.3]]), class: "demo-ray", fill: "none"}));
        points.forEach((point,i) => {
          const [x,y] = screen(point); dot(svg,x,y,"demo-point",4);
          label(svg,x,y-12,String(i+1),{"text-anchor":"middle"});
        });
      };
      drawPlane(175,110,point => point); drawPlane(545,110/extent,transform);
      const ratio = crossRatio(points.map(point => transform(point)[0]));
      const sample = transform([1,1]);
      label(svg, 22, 319, "Equally spaced source points");
      label(svg, 390, 319, "Spacing changes; straight lines stay straight");
      values.textContent = `p = ${pretty(p)}. Point (1, 1) maps to (${pretty(sample[0])}, ${pretty(sample[1])}); denominator = ${pretty(1+p)}. Cross-ratio: source ${pretty(4/3)}, destination ${pretty(ratio)}. ${p === 0 ? "p = 0 gives the identity map." : "A nonzero p adds perspective."}`;
      root.dataset.crossRatio = ratio; root.dataset.mappedU = sample[0]; root.dataset.mappedV = sample[1];
    };
    Object.values(inputs).forEach(input => input.addEventListener("input", render)); render();
  }

  function ransac(root) {
    const {inputs, svg, values, reset} = setup(root,
      "Each hypothesis draws four independent match statuses: blue = inlier, orange = outlier. The first 40 hypotheses are shown. Compare one experiment with the predicted probability and 200 simulated experiments. This uses the independent-status approximation, not the exact 25-pair pentagon sampler.",
      [{name: "inliers", title: "Inlier fraction w", min: 5, max: 95, step: 5, value: 20, unit: "%"},
       {name: "trials", title: "Trials per experiment N", min: 1, max: 3000, step: 1, value: 100, unit: ""}]);
    let seed = 1;
    const random = initial => {
      let state = initial >>> 0;
      return () => {
        state += 0x6D2B79F5;
        let t = state;
        t = Math.imul(t ^ t >>> 15, t | 1);
        t ^= t + Math.imul(t ^ t >>> 7, t | 61);
        return ((t ^ t >>> 14) >>> 0) / 4294967296;
      };
    };
    const again = document.createElement("button");
    again.type = "button"; again.className = "demo-reset";
    again.textContent = "Run another experiment"; reset.after(again);
    const render = () => {
      svg.querySelectorAll(":scope > :not(title)").forEach(n => n.remove());
      const w = +inputs.inliers.value / 100, n = +inputs.trials.value, q = w ** 4;
      const probability = -Math.expm1(n * Math.log1p(-q));
      const budget99 = Math.ceil(Math.log(0.01) / Math.log1p(-q));
      const rng = random(seed), samples = [];
      let cleanSamples = 0;
      for (let i = 0; i < n; i++) {
        const sample = Array.from({length: 4}, () => rng() < w);
        if (sample.every(Boolean)) cleanSamples++;
        if (i < 40) samples.push(sample);
      }
      let empiricalSuccesses = 0;
      for (let run = 0; run < 200; run++) {
        const experiment = random(seed * 104729 + run * 7919);
        for (let trial = 0; trial < n; trial++) {
          if (experiment() < q) { empiricalSuccesses++; break; }
        }
      }
      label(svg, 18, 28, `First ${samples.length} hypotheses (of ${n})`);
      samples.forEach((sample, i) => {
        const x = 22 + (i % 8) * 48, y = 65 + Math.floor(i / 8) * 43;
        if (sample.every(Boolean)) svg.append(svgNode("rect", {x: x-6, y: y-12, width: 43, height: 24, fill: "none", stroke: "#245981", "stroke-width": 2}));
        sample.forEach((good, j) => svg.append(svgNode("circle", {cx: x+j*9, cy: y, r: 3.5, fill: good ? "#245981" : "#b54708"})));
      });
      const bar = (y, title, fraction) => {
        label(svg, 438, y, title);
        svg.append(svgNode("rect", {x: 440, y: y+12, width: 240, height: 25, fill: "#e5e7eb"}));
        svg.append(svgNode("rect", {x: 440, y: y+12, width: 240*fraction, height: 25, fill: "#245981"}));
        label(svg, 438, y+60, `${(100*fraction).toFixed(2)}%`);
      };
      bar(45, "Predicted success probability", probability);
      bar(157, "Observed: 200 experiments", empiricalSuccesses/200);
      label(svg, 20, 298, "A box marks a clean four-inlier sample.");
      label(svg, 20, 324, `This experiment: ${cleanSamples} clean samples. Seed: ${seed}.`);
      values.textContent = `q = (${pretty(w)})^4 = ${q.toPrecision(5)}. P = 1 − (1 − ${q.toPrecision(5)})^${n} = ${(probability*100).toFixed(2)}%. At least one clean sample: ${cleanSamples ? "yes" : "no"} in this experiment; ${empiricalSuccesses}/200 experiments succeeded. A 99% budget is ${budget99.toLocaleString("en-US")} trials under this model. Clean does not guarantee a correct homography; nondegenerate geometry and reliable scoring are also needed.`;
      Object.assign(root.dataset, {q, probability, cleanSamples, empiricalSuccesses, seed, budget99});
    };
    reset.addEventListener("click", () => { seed = 1; render(); });
    again.addEventListener("click", () => { seed++; render(); });
    Object.values(inputs).forEach(input => input.addEventListener("input", render));
    render();
  }

  async function stereo(root) {
    const {createStereoExplorer} = await import(stereoModule.href);
    createStereoExplorer(root);
  }

  async function corner(root) { const m = await import(finalModule.href); m.createCornerExplorer(root); }
  async function refinement(root) { const m = await import(finalModule.href); m.createRefinementExplorer(root); }

  function initialize() {
    document.querySelectorAll(".interactive-demo:not([data-ready]):not([data-initializing])").forEach(root => {
      root.dataset.initializing = "true";
      Promise.resolve().then(() => ({projection, homography, ransac, stereo, corner, refinement}[root.dataset.demo])(root)).then(() => {
        root.dataset.ready = "true";
      }).catch(error => {
        // WebGL/module failures preserve the complete static explanation.
        root.querySelector(".interactive-stage").replaceChildren();
        root.dataset.error = "true";
        console.warn("Textbook demo unavailable; showing the static view.", error);
      });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
  else initialize();
})();
