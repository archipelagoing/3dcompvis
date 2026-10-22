/* Rectified stereo in world-length units, with local Three.js rendering. */
import * as THREE from './vendor/three/three.module.min.mjs';
import {OrbitControls} from './vendor/three/OrbitControls.mjs';
const fmt=n=>Number.isFinite(n)?String(Number(n.toFixed(4))):'undefined';
const world=(x,y,z)=>new THREE.Vector3(x,-y,-z);
const el=(tag,cls='',text='')=>{const n=document.createElement(tag);n.className=cls;n.textContent=text;return n;};
let serial=0;

export function createStereoExplorer(root) {
  root.classList.add('has-3d');
  const stage=root.querySelector('.interactive-stage');
  const intro=el('p','','Orange is the true point. Purple is the estimate from a perturbed right-image match. Drag the orange point to change depth, or use the sliders. Both cameras stay aligned; the point stays halfway between them as baseline changes.');
  const views=el('div','scene-views'),panel=el('div','scene-panel'),viewport=el('div','scene-viewport');
  const canvas=el('canvas','scene-canvas');canvas.tabIndex=0;canvas.setAttribute('role','img');
  canvas.setAttribute('aria-label','Rotatable 3D stereo cameras, virtual image planes, viewing rays, true point and estimated point. Labeled sliders provide all model controls.');
  const overlay=el('div','scene-labels');overlay.setAttribute('aria-hidden','true');
  viewport.append(canvas,overlay);panel.append(el('h4','','3D cameras and ray intersection'),viewport);
  const imagePanel=el('div','scene-image-panel');imagePanel.append(el('h4','','Linked camera images · 250 × 200 px'));
  const NS='http://www.w3.org/2000/svg';
  const makeSvg=()=>{const n=document.createElementNS(NS,'svg');n.setAttribute('viewBox','0 0 300 160');n.setAttribute('role','img');n.classList.add('scene-image');return n;};
  const leftImage=makeSvg(),rightImage=makeSvg();leftImage.setAttribute('aria-label','Left image: fixed measured reference column');rightImage.setAttribute('aria-label','Right image: true and perturbed correspondence columns');
  const status=el('p','scene-status');imagePanel.append(leftImage,rightImage,status);views.append(panel,imagePanel);
  const toolbar=el('div','scene-toolbar'),controls=el('div','demo-controls scene-controls');
  const fields=[
    {name:'depth',title:'True depth Z',min:2,max:100,step:1,value:20,unit:' cm'},
    {name:'baseline',title:'Baseline b',min:2,max:20,step:1,value:10,unit:' cm'},
    {name:'focal',title:'Focal length f',min:5,max:100,step:5,value:50,unit:' px'},
    {name:'error',title:'Disparity error δ',min:-2,max:2,step:1,value:1,unit:' px'},
  ];
  const inputs={},outputs={};
  fields.forEach(field=>{
    const wrap=el('div','demo-control'),lab=el('label','',field.title),input=el('input'),output=el('output');
    Object.assign(input,{type:'range',id:`stereo-${++serial}`,name:field.name,min:field.min,max:field.max,step:field.step,value:field.value});
    lab.htmlFor=input.id;output.htmlFor=input.id;lab.append(output);wrap.append(lab,input);controls.append(wrap);inputs[field.name]=input;outputs[field.name]=output;
  });
  const help=el('p','scene-help','Drag empty space to orbit; scroll/pinch to zoom. Orbiting changes your inspection view only. The translucent triangle is the epipolar plane through both centers and the point. Virtual-plane pixel pitch is 0.02 cm/pixel; point and camera markers are schematic.');
  const pipeline=el('div','scene-pipeline');
  const cards=['1 · Project the true point','2 · Perturb one match','3 · Reconstruct depth'].map(title=>{const card=el('div','scene-step'),value=el('div','scene-equation');card.append(el('strong','',title),value);pipeline.append(card);return value;});
  const summary=el('p','demo-values scene-summary');summary.setAttribute('aria-live','polite');summary.setAttribute('aria-atomic','true');
  stage.append(intro,views,toolbar,help,controls,pipeline,summary);
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));renderer.setClearColor(0xf4f8fb);
  const scene=new THREE.Scene();scene.add(new THREE.HemisphereLight(0xffffff,0xbccbd6,2));
  const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(10,20,10);scene.add(light);
  const observer=new THREE.PerspectiveCamera(42,1,.05,10000);observer.position.set(25,18,20);
  const orbit=new OrbitControls(observer,canvas);orbit.enableDamping=false;orbit.minDistance=2;orbit.maxDistance=1000;orbit.target.set(5,0,-10);
  const grid=new THREE.GridHelper(200,40,0x9ab1c0,0xd8e3eb);grid.position.set(0,-5,-40);scene.add(grid);
  const truePoint=new THREE.Mesh(new THREE.SphereGeometry(.3,20,16),new THREE.MeshStandardMaterial({color:0xbb5b0b}));
  const estimate=new THREE.Mesh(new THREE.SphereGeometry(.42,20,16),new THREE.MeshBasicMaterial({color:0x8050a0,wireframe:true}));scene.add(truePoint,estimate);
  function line(color){const n=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3()]),new THREE.LineBasicMaterial({color}));scene.add(n);return n;}
  const leftRay=line(0xbb5b0b),rightRay=line(0x24577a),observedRay=line(0x8050a0),baseline=line(0x526977);
  const setLine=(n,a,b)=>{const p=n.geometry.getAttribute('position');p.setXYZ(0,a.x,a.y,a.z);p.setXYZ(1,b.x,b.y,b.z);p.needsUpdate=true;n.geometry.computeBoundingSphere();};
  const cameras=[0,1].map(()=>{const body=new THREE.Mesh(new THREE.BoxGeometry(.9,.6,.7),new THREE.MeshStandardMaterial({color:0x24577a}));scene.add(body);return body;});
  const planes=[0,1].map(()=>{
    const geometry=new THREE.PlaneGeometry(5,4),plane=new THREE.Mesh(geometry,new THREE.MeshBasicMaterial({color:0x4188b0,side:THREE.DoubleSide,transparent:true,opacity:.18,depthWrite:false}));
    plane.add(new THREE.LineSegments(new THREE.EdgesGeometry(geometry),new THREE.LineBasicMaterial({color:0x24577a})));scene.add(plane);return plane;
  });
  const qPoints=[0,1,2].map((_,i)=>{const n=new THREE.Mesh(new THREE.SphereGeometry(.08,12,10),new THREE.MeshBasicMaterial({color:i===2?0x8050a0:0xbb5b0b,depthTest:false}));n.renderOrder=10;scene.add(n);return n;});
  const triangleGeometry=new THREE.BufferGeometry();triangleGeometry.setAttribute('position',new THREE.Float32BufferAttribute(new Array(9).fill(0),3));
  const triangle=new THREE.Mesh(triangleGeometry,new THREE.MeshBasicMaterial({color:0x6d91ae,side:THREE.DoubleSide,transparent:true,opacity:.12,depthWrite:false}));scene.add(triangle);
  const tags=[];
  function tag(text,color){const label=el('span','scene-tag',text);label.style.borderColor=color;overlay.append(label);const item={label,position:new THREE.Vector3(),visible:true};tags.push(item);return item;}
  const leftTag=tag('C_L · origin','#24577a'),rightTag=tag('C_R · baseline b','#24577a'),pointTag=tag('True P','#bb5b0b'),estimateTag=tag('Estimated P','#8050a0');
  let state,queued=false,dragging=null;
  function draw(){
    if(queued)return;queued=true;
    requestAnimationFrame(()=>{
      queued=false;if(!root.isConnected)return;
      const width=viewport.clientWidth,height=viewport.clientHeight;if(!width||!height)return;
      renderer.setSize(width,height,false);observer.aspect=width/height;observer.updateProjectionMatrix();renderer.render(scene,observer);
      tags.forEach(t=>{const p=t.position.clone().project(observer);t.label.hidden=!t.visible||p.z<-1||p.z>1||Math.abs(p.x)>.98||Math.abs(p.y)>.98;
        if(!t.label.hidden){const margin=t.label.offsetWidth/2+4;t.label.style.left=`${Math.max(margin,Math.min(width-margin,(p.x+1)*width/2))}px`;t.label.style.top=`${Math.max(25,Math.min(height-8,(1-p.y)*height/2))}px`;}});
      const p=truePoint.position.clone().project(observer);Object.assign(root.dataset,{pickX:(p.x+1)*width/2,pickY:(1-p.y)*height/2,view:observer.position.toArray().map(fmt).join(','),rendered:'true'});
    });
  }
  orbit.addEventListener('change',draw);const resize=new ResizeObserver(draw);resize.observe(viewport);
  function fitView(reset=false){
    const dir=reset?new THREE.Vector3(1,.7,1):observer.position.clone().sub(orbit.target).normalize();
    orbit.target.set(state.b/2,0,-state.z/2);observer.position.copy(orbit.target).addScaledVector(dir.normalize(),Math.max(state.z,state.b*2)*1.9);orbit.update();draw();
  }
  const reset=el('button','demo-reset','Reset');reset.type='button';reset.addEventListener('click',()=>{fields.forEach(f=>{inputs[f.name].value=f.value;});update(false);fitView(true);});toolbar.append(reset);
  const side=el('button','demo-reset','Side view');side.type='button';side.addEventListener('click',()=>{observer.position.copy(orbit.target).add(new THREE.Vector3(0,Math.max(state.z,state.b*2)*1.5,.001));orbit.update();draw();});toolbar.append(side);
  const perspective=el('button','demo-reset','Perspective view');perspective.type='button';perspective.addEventListener('click',()=>fitView(true));toolbar.append(perspective);
  function image(svg,title,trueU,observedU){
    svg.replaceChildren();
    const put=(tag,attrs,text='')=>{const n=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));n.textContent=text;svg.append(n);};
    put('rect',{x:20,y:25,width:250,height:105,fill:'#fff',stroke:'#24577a'});
    put('text',{x:20,y:16,'font-size':12,fill:'#172936'},title);
    put('line',{x1:20,y1:77,x2:270,y2:77,stroke:'#a6bac9','stroke-dasharray':'4 3'});
    put('line',{x1:145,y1:25,x2:145,y2:130,stroke:'#a6bac9','stroke-dasharray':'4 3'});
    if(trueU>=0&&trueU<250)put('circle',{cx:20+trueU,cy:77,r:5,fill:'#bb5b0b'});
    if(observedU!==null&&observedU>=0&&observedU<250){put('line',{x1:20+observedU,y1:57,x2:20+observedU,y2:97,stroke:'#8050a0','stroke-width':2});}
    put('text',{x:20,y:150,'font-size':12,fill:'#172936'},`true u = ${fmt(trueU)}${observedU===null?'':`; observed u = ${fmt(observedU)}`}`);
  }
  function update(refit=true){
    fields.forEach(f=>{outputs[f.name].textContent=fmt(+inputs[f.name].value)+f.unit;});
    const z=+inputs.depth.value,b=+inputs.baseline.value,f=+inputs.focal.value,delta=+inputs.error.value;
    const d=f*b/z,measured=d+delta,zhat=Math.abs(measured)<1e-12?NaN:f*b/measured;
    const valid=measured>1e-12,ul=125+d/2,ur=125-d/2,observed=ur-delta,xhat=valid?b*d/(2*measured):NaN;
    const exact=valid?zhat-z:NaN,linear=-f*b*delta/(d*d),physicalF=f*.02;
    const refitNeeded=state&&(state.z!==z||state.b!==b);state={z,b,f,delta};
    const CL=world(0,0,0),CR=world(b,0,0),P=world(b/2,0,z),Phat=world(xhat,0,zhat);
    truePoint.position.copy(P);truePoint.scale.setScalar(Math.max(1,z/25));estimate.visible=valid;estimate.scale.copy(truePoint.scale);if(valid)estimate.position.copy(Phat);
    cameras[0].position.copy(world(0,0,-.4));cameras[1].position.copy(world(b,0,-.4));
    planes[0].position.copy(world(0,0,physicalF));planes[1].position.copy(world(b,0,physicalF));
    const ql=world(physicalF*(ul-125)/f,0,physicalF),qr=world(b+physicalF*(ur-125)/f,0,physicalF),qo=world(b+physicalF*(observed-125)/f,0,physicalF);
    [ql,qr,qo].forEach((q,i)=>qPoints[i].position.copy(q));
    setLine(leftRay,CL,valid&&zhat>z?Phat:P);setLine(rightRay,CR,P);setLine(baseline,CL,CR);
    setLine(observedRay,CR,valid?Phat:world(b+(observed-125)/f*z*1.3,0,z*1.3));
    const attr=triangleGeometry.getAttribute('position');[CL,CR,P].forEach((p,i)=>attr.setXYZ(i,p.x,p.y,p.z));attr.needsUpdate=true;triangleGeometry.computeBoundingSphere();
    leftTag.position.copy(CL).add(new THREE.Vector3(0,-1,0));rightTag.position.copy(CR).add(new THREE.Vector3(0,-1,0));pointTag.position.copy(P).add(new THREE.Vector3(0,1,0));
    estimateTag.visible=valid;if(valid)estimateTag.position.copy(Phat).add(new THREE.Vector3(1,-1,0));
    const visibility=ul>=0&&ul<250&&ur>=0&&ur<250&&observed>=0&&observed<250;
    status.textContent=!valid?(Math.abs(measured)<1e-12?'Zero measured disparity: no finite intersection.':'Negative measured disparity: no forward reconstructed point in this convention.'):
      `Estimated depth ${fmt(zhat)} cm. ${visibility?'Both correspondences lie inside the images.':'A correspondence is outside the image; the ray equation is still shown.'}`;
    cards[0].textContent=`P = (${fmt(b/2)}, 0, ${fmt(z)}) cm\nuL = 125 + ${f} × ${fmt(b/2)} / ${z} = ${fmt(ul)}\nuR = 125 + ${f} × (${fmt(-b/2)}) / ${z} = ${fmt(ur)}`;
    cards[1].textContent=`d = ${fmt(ul)} − ${fmt(ur)} = ${fmt(d)} px\nmeasured d = ${fmt(d)} + (${delta}) = ${fmt(measured)}\nobserved uR = ${fmt(ur)} − (${delta}) = ${fmt(observed)}`;
    cards[2].textContent=`estimated Z = ${f} × ${b} / ${fmt(measured)} = ${valid?fmt(zhat):'no forward depth'} cm\nexact error = ${fmt(exact)} cm\nfirst-order error = ${fmt(linear)} cm`;
    summary.textContent=`True depth ${z} cm; disparity ${fmt(d)} px; measured disparity ${fmt(measured)} px. ${status.textContent} ${valid?`Signed exact error ${fmt(exact)} cm; linearized error ${fmt(linear)} cm.`:''}`;
    Object.assign(root.dataset,{depth:z,baseline:b,focal:f,delta,disparity:d,measured,estimatedZ:zhat,estimatedX:xhat,exactError:exact,linearError:linear,ul,ur,observedU:observed,physicalF,valid:String(valid),leftQ:ql.toArray().join(','),rightQ:qr.toArray().join(','),observedQ:qo.toArray().join(',')});
    image(leftImage,'Left image · orange reference',ul,null);image(rightImage,'Right image · purple observed match',ur,observed);
    if(refit&&refitNeeded&&dragging===null)fitView();else draw();
  }
  Object.values(inputs).forEach(input=>input.addEventListener('input',()=>update()));
  const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2(),dragPlane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
  const pick=e=>{const r=canvas.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);raycaster.setFromCamera(pointer,observer);};
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0||dragging!==null)return;pick(e);if(!raycaster.intersectObject(truePoint,false).length)return;dragging=e.pointerId;orbit.enabled=false;canvas.setPointerCapture(e.pointerId);canvas.classList.add('is-dragging');e.stopImmediatePropagation();e.preventDefault();},true);
  canvas.addEventListener('pointermove',e=>{if(dragging!==e.pointerId)return;pick(e);const hit=raycaster.ray.intersectPlane(dragPlane,new THREE.Vector3());if(hit){inputs.depth.value=Math.max(2,Math.min(100,Math.round(-hit.z)));update(false);}e.stopImmediatePropagation();},true);
  const release=e=>{if(dragging!==e.pointerId)return;dragging=null;orbit.enabled=true;canvas.classList.remove('is-dragging');if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);e.stopImmediatePropagation();};
  canvas.addEventListener('pointerup',release,true);canvas.addEventListener('pointercancel',release,true);
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();root.dataset.ready='false';stage.hidden=true;orbit.dispose();resize.disconnect();});
  update(false);fitView(true);root.dataset.renderer='webgl';
}
