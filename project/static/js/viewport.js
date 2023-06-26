import * as THREE from 'https://unpkg.com/three@0.126.1/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.126.1/examples/jsm/controls/OrbitControls.js';
import { FlakesTexture } from 'https://unpkg.com/three@0.126.1/examples/jsm/textures/FlakesTexture.js';
import { RGBELoader } from 'https://unpkg.com/three@0.126.1/examples/jsm/loaders/RGBELoader.js'


// var scene, camera, renderer, controls, pointlight;
// var container = document.getElementById('container');

// scene = new THREE.Scene();

// renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
// renderer.setClearColor(0x888888);
// renderer.setSize(window.innerWidth, window.innerHeight);
// document.body.appendChild(renderer.domElement);

// renderer.outputEncoding = THREE.sRGBEncoding;
// renderer.toneMapping = THREE.ACESFilmicToneMapping;
// renderer.toneMappingExposure = 1.25;

// renderer.setSize(container.offsetWidth, container.offsetHeight);
// renderer.setPixelRatio(window.devicePixelRatio);
// container.appendChild(renderer.domElement);

// camera = new THREE.PerspectiveCamera(50, container.innerWidth / container.innerHeight, 1, 1000);
// camera.position.set(0, 0, 500);

// // camera = new THREE.PerspectiveCamera(45, container.offsetWidth / container.offsetHeight, 0.1, 1000);
// // camera.position.z = 5;

// addEventListener("resize", () => {
//     camera.aspect = getWidth() / getHeight();
//     camera.updateProjectionMatrix();

//     renderer.setSize(window.innerWidth, window.innerHeight);
// }, false);

// controls = new OrbitControls(camera, renderer.domElement);

// pointlight = new THREE.PointLight(0xffffff, 1);
// pointlight.position.set(200, 200, 200);
// scene.add(pointlight);

// let envmaploader = new THREE.PMREMGenerator(renderer);


// new RGBELoader().setPath('/pbr_generator/project/images/hdri/').load('pine_attic_2k.hdr', function (hdrmap) {

//     let envmap = envmaploader.fromCubemap(hdrmap);
//     let texture = new THREE.CanvasTexture(new FlakesTexture());
//     texture.wrapS = THREE.RepeatWrapping;
//     texture.wrapT = THREE.RepeatWrapping;
//     texture.repeat.x = 10;
//     texture.repeat.y = 6;

//     const ballMaterial = {
//         clearcoat: 1.0,
//         clearcoatRoughness: 0.1,
//         metalness: 0.9,
//         roughness: 0.5,
//         color: 0x8418ca,
//         normalMap: texture,
//         normalScale: new THREE.Vector2(0.15, 0.15),
//         envMap: envMap.texture
//     };

//     let ballGeo = new THREE.SphereGeometry(100, 64, 64);
//     let ballMat = new THREE.MeshPhysicalMaterial(ballMaterial);
//     let ballMesh = new THREE.Mesh(ballGeo, ballMat);
//     scene.add(ballMesh);

//     animate();
// });  

// function animate() {
//     controls.update();
//     renderer.render(scene, camera);
//     requestAnimationFrame(animate);
// }

var container = document.getElementById('container');

var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setClearColor(0x888888);
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

function getWidth() {
    return parseInt(window.getComputedStyle(canvas).width);
}

function getHeight() {
    return parseInt(window.getComputedStyle(canvas).height);
}

// Set the size of the renderer to match the container
renderer.setSize(container.offsetWidth, container.offsetHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.25;

addEventListener("resize", () => {
    camera.aspect = getWidth() / getHeight();
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
}, false);

var scene = new THREE.Scene();

//texture settings
var textureLoader = new THREE.TextureLoader();
var albedoTexture = textureLoader.load('project/static/images/pbr/Albedo.png');
var normalTexture = textureLoader.load('path/to/normal.jpg');
var roughnessTexture = textureLoader.load('path/to/roughness.jpg');
var metalnessTexture = textureLoader.load('path/to/metalness.jpg');

var ballMat = new THREE.MeshStandardMaterial({
    map: albedoTexture,
    normalMap: normalTexture,
    roughnessMap: roughnessTexture,
    bumpMap: heightTexture
});

//mesh setting
const geometry = new THREE.SphereGeometry(1.3, 64, 64);
const material = new THREE.MeshBasicMaterial( ballMat );
const sphere = new THREE.Mesh( geometry, material );
scene.add(sphere);

var camera = new THREE.PerspectiveCamera(45, container.offsetWidth / container.offsetHeight, 0.1, 1000);
camera.position.z = 5;

// controls = new OrbitControls(camera, renderer.domElement);

const light = new THREE.PointLight( 0xffffff,100 );
light.position.set( 50, 50, 50 );
scene.add( light );

// Render the scene
renderer.render(scene, camera);

function animate() {
    requestAnimationFrame(animate);

    sphere.rotation.x += 0.01;
    sphere.rotation.y += 0.01;

    renderer.render(scene, camera);
}

animate();