import * as THREE from './three.module.js';

let scene = new THREE.Scene();
scene.background = new THREE.Color(0x222222);

let camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(0,5,12);

let renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

const light = new THREE.DirectionalLight(0xffffff,1);
light.position.set(5,10,5);
scene.add(light);

const amb = new THREE.AmbientLight(0xffffff,0.4);
scene.add(amb);

// Ground
const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(200,200),
    new THREE.MeshPhongMaterial({color:0x333333})
);
ground.rotation.x = -Math.PI/2;
scene.add(ground);

// Placeholder cube car
let car = new THREE.Mesh(
    new THREE.BoxGeometry(2,1,4),
    new THREE.MeshPhongMaterial({color:0xff0000})
);
scene.add(car);

let speed = 0;
let keys = {};
onkeydown = e => keys[e.key]=true;
onkeyup = e => keys[e.key]=false;

function animate(){
    requestAnimationFrame(animate);

    if(keys["ArrowUp"]) speed += 0.02;
    if(keys["ArrowDown"]) speed -= 0.02;
    if(keys["ArrowLeft"]) car.rotation.y += 0.05;
    if(keys["ArrowRight"]) car.rotation.y -= 0.05;

    speed *= 0.98;
    car.translateZ(speed);

    document.getElementById("score").innerText = "Speed: "+speed.toFixed(2);

    renderer.render(scene,camera);
}
animate();

onresize = ()=>{
    renderer.setSize(innerWidth, innerHeight);
    camera.aspect = innerWidth/innerHeight;
    camera.updateProjectionMatrix();
};
