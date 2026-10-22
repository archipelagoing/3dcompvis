/* Camera geometry in actual 3D, rendered locally with Three.js r180. */
import * as THREE from './vendor/three/three.module.min.mjs';
import {OrbitControls} from './vendor/three/OrbitControls.mjs';

const fmt = n => Number.isFinite(n) ? String(Number(n.toFixed(3))) : 'undefined';
const world = (x, y, z) => new THREE.Vector3(x, -y, -z);
const colors = {camera: 0x24577a, ray: 0xbb5b0b, x: 0xb83940, y: 0x23805c, z: 0x336ab0};
let nextId = 0;
const element = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
};

export function createProjectionExplorer(root) {
  const stage = root.querySelector('.interactive-stage');
  root.classList.add('has-3d');
  const intro = element('p', '', 'Drag the orange 3D point or use the sliders. The orange ray meets the blue image plane at q; the linked image shows the same point in pixels.');
  const views = element('div', 'scene-views');
  const scenePanel = element('div', 'scene-panel');
  const sceneTitle = element('h4', '', '3D scene');
  const viewport = element('div', 'scene-viewport');
  const canvas = element('canvas', 'scene-canvas');
  canvas.tabIndex = 0;
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', 'Rotatable 3D scene with a camera, image plane, world point, and projection ray. Use the labeled sliders to change the scene without dragging.');
  const labels = element('div', 'scene-labels'); labels.setAttribute('aria-hidden', 'true');
  viewport.append(canvas, labels); scenePanel.append(sceneTitle, viewport);
  const imagePanel = element('div', 'scene-image-panel');
  imagePanel.append(element('h4', '', 'Camera image · 500 × 500 px'));
  const image = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  image.setAttribute('viewBox', '0 0 300 300'); image.setAttribute('role', 'img');
  image.setAttribute('aria-label', 'Image coordinates of the projected world point');
  image.classList.add('scene-image'); imagePanel.append(image);
  const status = element('p', 'scene-status'); imagePanel.append(status);
  views.append(scenePanel, imagePanel);
  const toolbar = element('div', 'scene-toolbar');
  const controlsWrap = element('div', 'demo-controls scene-controls');
  const fields = [
    {name:'pointX', title:'Point X · left/right', min:-3, max:3, step:.25, value:1, unit:' units'},
    {name:'pointY', title:'Point Y · up/down', min:-2, max:2, step:.25, value:.5, unit:' units'},
    {name:'pointZ', title:'Point Z · world depth', min:4, max:14, step:.5, value:10, unit:' units'},
    {name:'camera', title:'Camera Z · move camera', min:-2, max:12, step:.5, value:0, unit:' units'},
    {name:'focal', title:'Focal length f', min:150, max:1000, step:10, value:500, unit:' px'},
    {name:'yaw', title:'Camera yaw · turn camera', min:-45, max:45, step:5, value:0, unit:'°'},
  ];
  const inputs = {}, readouts = {};
  fields.forEach(field => {
    const wrap = element('div', 'demo-control');
    const label = element('label', '', field.title);
    const input = element('input');
    Object.assign(input, {type:'range', id:`projection-3d-${++nextId}`, ...field});
    // Only input attributes are used; titles/units remain in their labels.
    label.htmlFor = input.id;
    const output = element('output'); output.htmlFor = input.id;
    label.append(output); wrap.append(label, input); controlsWrap.append(wrap);
    inputs[field.name] = input; readouts[field.name] = output;
  });
  const help = element('p', 'scene-help', 'Drag empty space to orbit; scroll or pinch to zoom. Drag the point to move it at its current world depth. Changing your inspection view does not move the blue teaching camera.');
  const pipeline = element('div', 'scene-pipeline');
  const steps = ['1 · World point', '2 · Camera coordinates', '3 · Image coordinates'];
  const cards = steps.map(title => {
    const card = element('div', 'scene-step');
    const output = element('div', 'scene-equation');
    card.append(element('strong', '', title), output); pipeline.append(card); return output;
  });
  const summary = element('p', 'demo-values scene-summary');
  summary.setAttribute('aria-live', 'polite'); summary.setAttribute('aria-atomic', 'true');
  stage.append(intro, views, toolbar, help, controlsWrap, pipeline, summary);

  const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:false});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0xf4f8fb);
  const scene = new THREE.Scene();
  scene.add(new THREE.HemisphereLight(0xffffff,0xbccbd6,2));
  const sunlight=new THREE.DirectionalLight(0xffffff,2.5);
  sunlight.position.set(5,10,6);scene.add(sunlight);
  const observer = new THREE.PerspectiveCamera(42, 1, .1, 120);
  observer.position.set(8, 6, 6);
  const orbit = new OrbitControls(observer, canvas);
  orbit.target.set(0, 0, -5); orbit.enableDamping = false;
  orbit.minDistance = 3; orbit.maxDistance = 55; orbit.enablePan = true;
  const grid = new THREE.GridHelper(24, 24, 0xa4b8c5, 0xd6e1e8);
  grid.position.set(0, -3, -5); scene.add(grid);

  const cameraGroup = new THREE.Group(); scene.add(cameraGroup);
  const body = new THREE.Mesh(new THREE.BoxGeometry(.8,.55,.65), new THREE.MeshStandardMaterial({color:colors.camera,roughness:.6}));
  body.position.z = .38; cameraGroup.add(body);
  const lens = new THREE.Mesh(new THREE.CylinderGeometry(.17,.17,.22,24), new THREE.MeshStandardMaterial({color:0x102f45,roughness:.4}));
  lens.rotation.x = Math.PI/2; cameraGroup.add(lens);
  const center = new THREE.Mesh(new THREE.SphereGeometry(.085,16,12),new THREE.MeshBasicMaterial({color:0xffffff}));
  cameraGroup.add(center);
  const planeGeometry = new THREE.PlaneGeometry(2,2);
  const imagePlane = new THREE.Mesh(planeGeometry, new THREE.MeshBasicMaterial({color:0x4188b0, side:THREE.DoubleSide, transparent:true, opacity:.2, depthWrite:false}));
  const planeEdges = new THREE.LineSegments(new THREE.EdgesGeometry(planeGeometry), new THREE.LineBasicMaterial({color:colors.camera}));
  imagePlane.add(planeEdges); scene.add(imagePlane);
  const planeGrid = new THREE.Group(); imagePlane.add(planeGrid);
  for (let v=-.5; v<=.5; v+=.5) {
    addLine([new THREE.Vector3(v,-1,.002), new THREE.Vector3(v,1,.002)],0x94b3c7,planeGrid);
    addLine([new THREE.Vector3(-1,v,.002), new THREE.Vector3(1,v,.002)],0x94b3c7,planeGrid);
  }
  const point = new THREE.Mesh(new THREE.SphereGeometry(.2,24,16),new THREE.MeshStandardMaterial({color:colors.ray,roughness:.5}));
  const q = new THREE.Mesh(new THREE.SphereGeometry(.085,20,12),new THREE.MeshBasicMaterial({color:colors.ray, depthTest:false}));
  q.renderOrder = 10; scene.add(point,q);
  const ray = addLine([new THREE.Vector3(),new THREE.Vector3()], colors.ray);
  const optical = addLine([new THREE.Vector3(),new THREE.Vector3()], colors.z);
  const frustum = [];
  for (const [x,y] of [[-1,-1],[1,-1],[1,1],[-1,1]]) {
    frustum.push({x,y,line:addLine([new THREE.Vector3(),new THREE.Vector3()],0x93b1c3)});
  }
  const arrows = [
    [world(1,0,0),colors.x,'+X'],[world(0,1,0),colors.y,'+Y'],[world(0,0,1),colors.z,'+Z'],
  ].map(([direction,color,text]) => {
    const arrow = new THREE.ArrowHelper(direction,new THREE.Vector3(),1.8,color,.22,.1);scene.add(arrow);
    return {arrow,direction,text};
  });

  function addLine(points, color, parent=scene) {
    const mesh = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color}));
    parent.add(mesh); return mesh;
  }
  function setLine(mesh, a, b) {
    const attr=mesh.geometry.getAttribute('position');
    attr.setXYZ(0,a.x,a.y,a.z);attr.setXYZ(1,b.x,b.y,b.z);attr.needsUpdate=true;
    mesh.geometry.computeBoundingSphere();
  }
  const annotations = [];
  function annotation(text, color, offset=[0,0]) {
    const label=element('span','scene-tag',text);label.style.borderColor=color;labels.append(label);
    const entry={label,position:new THREE.Vector3(),visible:true,offset};annotations.push(entry);return entry;
  }
  const cameraLabel=annotation('C · camera','#24577a',[-42,38]);
  const pointLabel=annotation('P · world point','#bb5b0b');
  const planeLabel=annotation('Virtual image plane','#24577a');
  const qLabel=annotation('q · projected point','#bb5b0b',[85,25]);
  const axisLabels=arrows.map(a=>annotation(a.text,`#${a.arrow.line.material.color.getHexString()}`));
  axisLabels.forEach(entry=>entry.label.classList.add('scene-axis-tag'));
  let state, drawPending=false;
  function draw() {
    if (drawPending) return;
    drawPending=true;
    requestAnimationFrame(() => {
      drawPending=false;
      if (!root.isConnected) return;
      const width=viewport.clientWidth,height=viewport.clientHeight;
      if (!width || !height) return;
      if (canvas.width!==Math.round(width*renderer.getPixelRatio()) || canvas.height!==Math.round(height*renderer.getPixelRatio())) {
        renderer.setSize(width,height,false);observer.aspect=width/height;observer.updateProjectionMatrix();
      }
      renderer.render(scene,observer);
      annotations.forEach(({label,position,visible,offset}) => {
        const screen=position.clone().project(observer);
        const show=visible && screen.z>=-1 && screen.z<=1 && Math.abs(screen.x)<.98 && Math.abs(screen.y)<.98;
        label.hidden=!show;
        if (show) {
          const margin=label.offsetWidth/2+5;
          label.style.left=`${Math.max(margin,Math.min(width-margin,(screen.x+1)*width/2+offset[0]))}px`;
          label.style.top=`${Math.max(25,Math.min(height-10,(1-screen.y)*height/2+offset[1]))}px`;
        }
      });
      root.dataset.view=observer.position.toArray().map(fmt).join(',');
      const screenPoint=point.position.clone().project(observer);
      root.dataset.pickX=String((screenPoint.x+1)*width/2);
      root.dataset.pickY=String((1-screenPoint.y)*height/2);
      root.dataset.rendered='true';
    });
  }
  orbit.addEventListener('change',draw);
  const resize=new ResizeObserver(draw);resize.observe(viewport);
  function view(position) {
    observer.position.copy(position);orbit.target.set(0,0,-5);orbit.update();draw();
  }
  const overview = new THREE.Vector3(8,6,6);
  [['Perspective view',overview],['Side view',new THREE.Vector3(16,1,-5)],['Look along Z',new THREE.Vector3(0,0,17)]].forEach(([title,position])=>{
    const button=element('button','demo-reset',title);button.type='button';
    button.addEventListener('click',()=>view(position));toolbar.append(button);
  });
  const reset=element('button','demo-reset','Reset');reset.type='button';
  reset.addEventListener('click',()=>{
    fields.forEach(field=>{inputs[field.name].value=field.value;});update();view(overview);
  });toolbar.append(reset);

  function renderImage(u,v,inside) {
    image.replaceChildren();
    const make=(tag,attrs,text='')=>{
      const n=document.createElementNS('http://www.w3.org/2000/svg',tag);
      Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));n.textContent=text;image.append(n);return n;
    };
    make('rect',{x:20,y:20,width:250,height:250,fill:'#fff',stroke:'#24577a','stroke-width':2});
    for (const t of [20,70,120,170,220,270]) {
      make('line',{x1:t,y1:20,x2:t,y2:270,stroke:'#e1e8ed'});
      make('line',{x1:20,y1:t,x2:270,y2:t,stroke:'#e1e8ed'});
    }
    make('line',{x1:145,y1:20,x2:145,y2:270,stroke:'#7f96a5','stroke-dasharray':'4 3'});
    make('line',{x1:20,y1:145,x2:270,y2:145,stroke:'#7f96a5','stroke-dasharray':'4 3'});
    make('circle',{cx:145,cy:145,r:3,fill:'#24577a'});
    make('text',{x:151,y:139,fill:'#24577a','font-size':11},'(250, 250)');
    make('text',{x:20,y:13,fill:'#172936','font-size':11},'(0, 0)');
    make('text',{x:240,y:290,fill:'#172936','font-size':11},'u →');
    make('text',{x:278,y:36,fill:'#172936','font-size':11},'v ↓');
    if (inside) {
      const x=20+u/2,y=20+v/2;
      make('line',{x1:145,y1:145,x2:x,y2:y,stroke:'#bb5b0b','stroke-width':2});
      make('circle',{cx:x,cy:y,r:5,fill:'#bb5b0b',stroke:'#fff'});
    } else make('text',{x:145,y:190,fill:'#172936','font-size':12,'text-anchor':'middle'},'No visible image point');
  }

  function update() {
    fields.forEach(field=>{readouts[field.name].textContent=`${fmt(+inputs[field.name].value)}${field.unit}`;});
    const x=+inputs.pointX.value,y=+inputs.pointY.value,z=+inputs.pointZ.value;
    const camera=+inputs.camera.value,f=+inputs.focal.value,yaw=+inputs.yaw.value;
    const angle=yaw*Math.PI/180,c=Math.cos(angle),s=Math.sin(angle);
    const xc=c*x-s*(z-camera),yc=y;
    const rawDepth=s*x+c*(z-camera),depth=Math.abs(rawDepth)<1e-9?0:rawDepth;
    const u=depth===0?NaN:250+f*xc/depth,v=depth===0?NaN:250+f*yc/depth;
    const inside=depth>0 && u>=0 && u<500 && v>=0 && v<500;
    const visibility=depth===0?'undefined':depth<0?'behind':inside?'inside':'outside';
    const message=depth===0?'Zero camera depth: no finite projection.':depth<0?'P is behind the camera.':inside?'The ray hits the image rectangle.':'P is in front, but its ray misses the image rectangle.';
    state={x,y,z,camera,f,yaw,depth,u,v,inside};
    const C=world(0,0,camera),P=world(x,y,z),physicalF=f*.004;
    const fromCamera=(a,b,d)=>world(c*a+s*d,b,camera-s*a+c*d);
    cameraGroup.position.copy(C);cameraGroup.rotation.y=-angle;point.position.copy(P);
    imagePlane.position.copy(fromCamera(0,0,physicalF));imagePlane.rotation.y=-angle;
    const Q=depth===0?null:C.clone().addScaledVector(P.clone().sub(C),physicalF/depth);
    q.visible=inside;
    if (Q) q.position.copy(Q);
    // Extend to the virtual plane only when the visible intersection lies beyond P.
    const end=inside && physicalF>depth ? Q : P;
    setLine(ray,C,end);ray.material.color.setHex(depth>0?colors.ray:0x9aa6ae);
    setLine(optical,C,fromCamera(0,0,6));
    frustum.forEach(({x,y,line})=>setLine(line,C,fromCamera(x,y,physicalF)));
    const directions=[world(c,0,-s),world(0,1,0),world(s,0,c)];
    arrows.forEach((a,i)=>{
      a.arrow.position.copy(C);a.arrow.setDirection(directions[i]);
      axisLabels[i].position.copy(C.clone().addScaledVector(directions[i],2));
    });
    cameraLabel.position.copy(C);
    pointLabel.position.copy(P.clone().add(new THREE.Vector3(0,.5,0)));
    planeLabel.position.copy(fromCamera(-.8,-1.4,physicalF));
    qLabel.visible=inside;
    if (Q) qLabel.position.copy(Q.clone().add(new THREE.Vector3(.15,-.35,0)));
    status.textContent=message;
    cards[0].textContent=`P = (${fmt(x)}, ${fmt(y)}, ${fmt(z)})`;
    cards[1].textContent=yaw===0 ? `R = I, t = (0, 0, ${fmt(-camera)})\nXc = ${fmt(x)}, Yc = ${fmt(y)}\nZc = ${fmt(z)} − (${fmt(camera)}) = ${fmt(depth)}` :
      `R = Ry(${fmt(-yaw)}°), t = −R C\nXc = ${fmt(c)} × ${fmt(x)} − (${fmt(s)}) × ${fmt(z-camera)} = ${fmt(xc)}\nYc = ${fmt(yc)}\nZc = ${fmt(s)} × ${fmt(x)} + ${fmt(c)} × ${fmt(z-camera)} = ${fmt(depth)}`;
    cards[2].textContent=`u = ${f} × ${fmt(xc)} / ${fmt(depth)} + 250 = ${fmt(u)} px\nv = ${f} × ${fmt(yc)} / ${fmt(depth)} + 250 = ${fmt(v)} px`;
    summary.textContent=`Camera coordinates: (${fmt(xc)}, ${fmt(yc)}, ${fmt(depth)}). Pixel: (${fmt(u)}, ${fmt(v)}). ${message}`;
    Object.assign(root.dataset,{depth:String(depth),u:String(u),v:String(v),visibility,pointX:String(x),pointY:String(y),pointZ:String(z),physicalF:String(physicalF)});
    Object.assign(root.dataset,{qx:Q?String(Q.x):'NaN',qy:Q?String(-Q.y):'NaN',qz:Q?String(-Q.z):'NaN'});
    Object.assign(root.dataset,{xc:String(xc),yc:String(yc),yaw:String(yaw)});
    renderImage(u,v,inside);draw();
  }
  Object.values(inputs).forEach(input=>input.addEventListener('input',update));

  const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();
  let dragging=null,dragPlane;
  const pick=event=>{
    const rect=canvas.getBoundingClientRect();
    pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);
    raycaster.setFromCamera(pointer,observer);
  };
  canvas.addEventListener('pointerdown',event=>{
    if (event.button!==0 || dragging!==null) return;
    pick(event);
    if (!raycaster.intersectObject(point,false).length) return;
    dragging=event.pointerId;orbit.enabled=false;
    dragPlane=new THREE.Plane().setFromNormalAndCoplanarPoint(new THREE.Vector3(0,0,1),point.position);
    canvas.setPointerCapture(event.pointerId);canvas.classList.add('is-dragging');
    event.stopImmediatePropagation();event.preventDefault();
  },true);
  canvas.addEventListener('pointermove',event=>{
    if (dragging!==event.pointerId) return;
    pick(event);const hit=raycaster.ray.intersectPlane(dragPlane,new THREE.Vector3());
    if (hit) {
      inputs.pointX.value=Math.max(-3,Math.min(3,Math.round(hit.x*4)/4));
      inputs.pointY.value=Math.max(-2,Math.min(2,Math.round(-hit.y*4)/4));update();
    }
    event.stopImmediatePropagation();
  },true);
  const release=event=>{
    if (dragging!==event.pointerId) return;
    dragging=null;orbit.enabled=true;canvas.classList.remove('is-dragging');
    if (canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId);
    event.stopImmediatePropagation();
  };
  canvas.addEventListener('pointerup',release,true);canvas.addEventListener('pointercancel',release,true);
  canvas.addEventListener('webglcontextlost',event=>{
    event.preventDefault();root.dataset.ready='false';stage.hidden=true;
    orbit.dispose();resize.disconnect();
  });
  orbit.update();update();root.dataset.renderer='webgl';
}
