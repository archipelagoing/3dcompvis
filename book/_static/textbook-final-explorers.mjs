/* Two local, mathematical 3D explorers; printable counterparts live in MyST. */
import * as THREE from './vendor/three/three.module.min.mjs';
import {OrbitControls} from './vendor/three/OrbitControls.mjs';
let serial=0;
const el=(tag,cls='',text='')=>{const n=document.createElement(tag);n.className=cls;n.textContent=text;return n;};
const fmt=n=>Number(n.toFixed(5)).toString();
const NS='http://www.w3.org/2000/svg';
const sv=(tag,attrs={},text='')=>{const n=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));n.textContent=text;return n;};
function setup(root,title,description){
 root.classList.add('has-3d');const stage=root.querySelector('.interactive-stage');
 const views=el('div','scene-views'),panel=el('div','scene-panel'),viewport=el('div','scene-viewport'),canvas=el('canvas','scene-canvas');
 canvas.tabIndex=0;canvas.setAttribute('role','img');canvas.setAttribute('aria-label',title+'. Rotate by dragging; labeled controls change the mathematical model.');
 viewport.append(canvas);panel.append(el('h4','',title),viewport);const side=el('div','scene-image-panel');views.append(panel,side);
 const controls=el('div','demo-controls scene-controls'),toolbar=el('div','scene-toolbar'),summary=el('p','demo-values scene-summary');summary.setAttribute('aria-live','polite');
 stage.append(el('p','',description),views,el('p','scene-help','Drag the 3D view to orbit; scroll or pinch to zoom. Orbiting changes only your inspection view. All model values can be changed with the labeled controls.'),controls,toolbar,summary);
 const renderer=new THREE.WebGLRenderer({canvas,antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));renderer.setClearColor(0xf4f8fb);
 const scene=new THREE.Scene();scene.add(new THREE.HemisphereLight(0xffffff,0x9aaabd,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(3,8,5);scene.add(light);
 const camera=new THREE.PerspectiveCamera(42,1,.01,100);camera.position.set(6,6,8);const orbit=new OrbitControls(camera,canvas);orbit.target.set(0,1,0);orbit.minDistance=.5;orbit.maxDistance=30;
 let stopped=false;
 function draw(){if(stopped)return;renderer.render(scene,camera);root.dataset.rendered='true';}
 orbit.addEventListener('change',()=>{root.dataset.view=fmt(camera.position.x)+','+fmt(camera.position.y)+','+fmt(camera.position.z);draw();});
 const resize=new ResizeObserver(()=>{const w=viewport.clientWidth,h=Math.max(300,Math.min(420,w*.8));renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();draw();});resize.observe(viewport);
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();stopped=true;resize.disconnect();root.dataset.ready='false';root.dataset.error='true';stage.replaceChildren();});
 const inputs={};
 function range(name,label,min,max,step,value,unit=''){
  const wrap=el('div','demo-control'),lab=el('label','',label+' '),input=el('input'),output=el('output');
  Object.assign(input,{type:'range',name,id:`final-${++serial}`,min,max,step,value});lab.htmlFor=input.id;output.htmlFor=input.id;
  const update=()=>{output.textContent=fmt(+input.value)+unit;};input.addEventListener('input',update);update();lab.append(output);wrap.append(lab,input);controls.append(wrap);inputs[name]=input;return input;
 }
 function line(points,color){const geometry=new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p)));const n=new THREE.Line(geometry,new THREE.LineBasicMaterial({color}));scene.add(n);return n;}
 function ball(color,r=.065){const n=new THREE.Mesh(new THREE.SphereGeometry(r,20,14),new THREE.MeshStandardMaterial({color}));scene.add(n);return n;}
 function svg(label,viewBox='0 0 320 240'){const n=sv('svg',{viewBox,role:'img','aria-label':label});n.classList.add('scene-image');side.append(n);return n;}
 return {stage,side,controls,toolbar,summary,renderer,scene,camera,orbit,inputs,range,line,ball,draw,svg};
}
export function createCornerExplorer(root){
 const ui=setup(root,'Patch error surface E(u,v)','A flat patch gives a plane; an edge gives a valley; a corner gives a bowl. The two listed gradients define the exact quadratic model; the image patch is schematic.');
 const {side,controls,range,scene,summary,draw}=ui;
 const lab=el('label','','Patch model '),select=el('select');select.id=`final-${++serial}`;select.name='patch';lab.htmlFor=select.id;
 ['corner','edge','flat'].forEach(value=>{const o=el('option','',value[0].toUpperCase()+value.slice(1));o.value=value;select.append(o);});lab.append(select);controls.prepend(lab);
 const u=range('u','Horizontal shift u',-2,2,.05,1,' px'),v=range('v','Vertical shift v',-2,2,.05,-1,' px');
 const svg=ui.svg('Schematic patch and draggable trial shift');svg.style.touchAction='none';const values=el('pre','scene-equation');side.append(values,el('p','','Drag the orange trial marker in this schematic, or use sliders. Surface height is E/16; horizontal coordinates are pixel shifts.'));
 const geometry=new THREE.BufferGeometry(),vertices=[],indices=[],N=32;
 for(let i=0;i<=N;i++)for(let j=0;j<=N;j++)vertices.push(-2+4*i/N,0,-2+4*j/N);
 for(let i=0;i<N;i++)for(let j=0;j<N;j++){const a=i*(N+1)+j,b=a+N+1;indices.push(a,b,a+1,b,b+1,a+1);}
 geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.setIndex(indices);
 const surface=new THREE.Mesh(geometry,new THREE.MeshStandardMaterial({color:0x4d91c6,side:THREE.DoubleSide,roughness:.6,transparent:true,opacity:.8}));scene.add(surface);
 const wire=new THREE.LineSegments(new THREE.WireframeGeometry(geometry),new THREE.LineBasicMaterial({color:0x244966,transparent:true,opacity:.3}));scene.add(wire);
 ui.line([[-2.4,0,0],[2.4,0,0]],0xa71930);ui.line([[0,0,-2.4],[0,0,2.4]],0x124fad);const marker=ui.ball(0xe27c18,.095);
 const models={flat:{a:0,c:0,b:0,g:'(0,0), (0,0)',lo:0,hi:0},edge:{a:8,c:8,b:8,g:'(2,2), (2,2)',lo:0,hi:16},corner:{a:4,c:0,b:9,g:'(2,0), (0,3)',lo:4,hi:9}};
 function update(){
  const model=models[select.value],{a,c,b,lo,hi}=model,x=+u.value,y=+v.value,cost=a*x*x+2*c*x*y+b*y*y;
  const pos=geometry.attributes.position;for(let i=0;i<pos.count;i++){const xx=pos.getX(i),yy=pos.getZ(i);pos.setY(i,(a*xx*xx+2*c*xx*yy+b*yy*yy)/16);}pos.needsUpdate=true;geometry.computeVertexNormals();wire.geometry.dispose();wire.geometry=new THREE.WireframeGeometry(geometry);marker.position.set(x,cost/16+.08,y);
  svg.replaceChildren(sv('rect',{x:30,y:20,width:260,height:180,fill:'#d9dfe5',stroke:'#53657c'}));
  if(select.value==='edge')svg.append(sv('path',{d:'M30 20 L290 200 L30 200 Z',fill:'#374f69'}));
  if(select.value==='corner')svg.append(sv('path',{d:'M160 20 L160 110 L290 110 L290 200 L30 200 L30 20 Z',fill:'#374f69'}));
  svg.append(sv('line',{x1:160,y1:110,x2:160+x*45,y2:110+y*35,stroke:'#a71930','stroke-width':3}),sv('circle',{cx:160+x*45,cy:110+y*35,r:9,fill:'#d46b08'}),sv('text',{x:24,y:230,fill:'#18334d','font-size':15},`Trial shift (${fmt(x)}, ${fmt(y)}) px`));
  const h=a*b-c*c-.04*(a+b)**2;
  values.textContent=`Gradients: ${model.g}\nM = [[${a}, ${c}], [${c}, ${b}]]\nEigenvalues: ${lo}, ${hi}\nE = ${fmt(cost)}\nHarris k=.04: ${fmt(h)}`;
  summary.textContent=`${select.value}: E = ${a}u² + ${2*c}uv + ${b}v² = ${fmt(cost)}. Smallest eigenvalue ${lo}: ${lo===0?'at least one shift direction is unconstrained.':'both shift directions are constrained.'}`;
  Object.assign(root.dataset,{patch:select.value,m11:a,m12:c,m22:b,lambdaMin:lo,lambdaMax:hi,u:x,v:y,cost,harris:h});draw();
 }
 let dragging=false;const drag=e=>{const box=svg.getBoundingClientRect(),px=(e.clientX-box.left)*320/box.width,py=(e.clientY-box.top)*240/box.height;u.value=Math.max(-2,Math.min(2,(px-160)/45));v.value=Math.max(-2,Math.min(2,(py-110)/35));u.dispatchEvent(new Event('input'));v.dispatchEvent(new Event('input'));};
 svg.addEventListener('pointerdown',e=>{dragging=true;svg.setPointerCapture(e.pointerId);drag(e);});svg.addEventListener('pointermove',e=>{if(dragging)drag(e);});svg.addEventListener('pointerup',()=>dragging=false);svg.addEventListener('pointercancel',()=>dragging=false);
 [select,u,v].forEach(n=>n.addEventListener('input',update));update();
}
export function createRefinementExplorer(root){
 const ui=setup(root,'Two cameras and one moving point','The point stays on the measured left ray. Its right projection changes with depth. Try Z = 6 m to make the mismatch obvious, then take improving steps. This is a fixed-camera point refinement, a small subset of bundle adjustment.');
 const {range,scene,camera,orbit,summary,toolbar,side,draw}=ui;
 const depth=range('depth','Current depth Z',2,8,.000001,4,' m'),measurement=range('measurement','Measured right u',200,235,.1,219,' px'),damping=range('damping','Damping λ',0,200,1,0);
 const step=el('button','','Take one GN / LM step'),reset=el('button','','Reset');step.type=reset.type='button';toolbar.append(step,reset);
 const svg=ui.svg('Right image: measured and predicted point','0 0 340 260'),values=el('pre','scene-equation');side.append(values,el('p','','Blue: current point and predicted ray. Orange: measured ray and consistent point. Camera baseline is 0.2 m. Virtual image planes use pitch 0.0005 m/pixel and are 0.4 m in front of each camera.'));
 camera.position.set(5,3,-1.5);orbit.target.set(.6,-.3,-2.3);orbit.update();
 const world=(x,y,z)=>[x,-y,-z];const point=ui.ball(0x124fad,.045),target=ui.ball(0xd46b08,.045);
 const left=ui.ball(0x18334d,.025),right=ui.ball(0x18334d,.025);right.position.set(.2,0,0);
 const lines=[ui.line([[0,0,0],[0,0,-4]],0x124fad),ui.line([[.2,0,0],[0,0,-4]],0x124fad),ui.line([[.2,0,0],[0,0,-4]],0xd46b08)];
 for(const base of [0,.2]){
  const plane=new THREE.Mesh(new THREE.PlaneGeometry(.32,.24),new THREE.MeshBasicMaterial({color:0x779ec6,transparent:true,opacity:.18,side:THREE.DoubleSide}));plane.position.set(base+.16,-.12,-.4);scene.add(plane);
  ui.line([[base,0,0],[base+.32,0,-.4],[base+.32,-.24,-.4],[base,0,0],[base,-.24,-.4],[base+.32,-.24,-.4]],0x8da4bb);
 }
 let last='No update taken yet.';
 function update(){
  const z=+depth.value,obs=+measurement.value,lambda=+damping.value,pred=260-160/z,r=pred-obs,J=160/(z*z),delta=-J*r/(J*J+lambda),truth=160/(260-obs);
  point.position.set(...world(260*z/800,120*z/800,z));target.position.set(...world(260*truth/800,120*truth/800,truth));
  [point,point,target].forEach((p,i)=>{lines[i].geometry.dispose();lines[i].geometry=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(i? .2:0,0,0),p.position.clone()]);});
  const map=x=>15+x*.8;svg.replaceChildren(sv('rect',{x:10,y:10,width:320,height:210,fill:'#fff',stroke:'#697d93'}),sv('line',{x1:map(obs),x2:map(obs),y1:15,y2:200,stroke:'#d46b08','stroke-width':2}),sv('circle',{cx:map(pred),cy:100,r:6,fill:'#124fad'}),sv('text',{x:18,y:242,fill:'#18334d','font-size':14},`Measured ${fmt(obs)} px; predicted ${fmt(pred)} px`));
  values.textContent=`X = ${fmt(260*z/800)} m\nY = ${fmt(120*z/800)} m\nZ = ${fmt(z)} m\nr = ${fmt(r)} px; J = ${fmt(J)} px/m\nProposed ΔZ = ${fmt(delta)} m\nE = ½r² = ${fmt(.5*r*r)}\nExact Z* = ${fmt(truth)} m`;
  summary.textContent=last+' Left projection stays (260,120). Right residual = '+fmt(r)+' px. '+(lambda?'Damped LM direction.':'Undamped Gauss–Newton direction.');
  Object.assign(root.dataset,{depth:z,measurement:obs,damping:lambda,prediction:pred,residual:r,jacobian:J,delta,cost:.5*r*r,targetDepth:truth,pointX:260*z/800,pointY:120*z/800});draw();
 }
 step.addEventListener('click',()=>{const z=+depth.value,obs=+measurement.value,r=260-160/z-obs,J=160/z**2;let delta=-J*r/(J*J+(+damping.value)),candidate=z+delta,attempts=0;
  while(attempts<16&&(candidate<2||candidate>8||.5*(260-160/candidate-obs)**2>.5*r*r)){delta*=.5;candidate=z+delta;attempts++;}
  if(candidate>=2&&candidate<=8&&.5*(260-160/candidate-obs)**2<=.5*r*r){depth.value=candidate;last=`Accepted ΔZ = ${fmt((+depth.value)-z)} m${attempts?' after reducing the step':''}.`;depth.dispatchEvent(new Event('input'));}else{last='Step rejected; choose a different starting depth or damping.';update();}});
 reset.addEventListener('click',()=>{depth.value=4;measurement.value=219;damping.value=0;last='Reset to the printed example.';[depth,measurement,damping].forEach(n=>n.dispatchEvent(new Event('input')));});
 [depth,measurement,damping].forEach(n=>n.addEventListener('input',update));update();
}
