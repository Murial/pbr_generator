import * as THREE from 'https://unpkg.com/three@0.126.1/build/three.module.js';
import GUI from 'https://cdn.jsdelivr.net/npm/lil-gui@0.18/+esm';
import { OrbitControls } from 'https://unpkg.com/three@0.126.1/examples/jsm/controls/OrbitControls.js';
import { RGBELoader } from 'https://unpkg.com/three@0.126.1/examples/jsm/loaders/RGBELoader.js';

var container = document.getElementById('container');

var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setClearColor(0x888888);
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// GUI PARAMETERS
const params = {
    displacementScale: 0.2,
    normalScale : 0.7,
    reflectivity: 0.2,
    roughness : 4,
    exposure : 1,
    tilingX : 1,
    tilingY : 1
}

function getWidth() {
    return parseInt(window.getComputedStyle(container).width);
}
function getHeight() {
    return parseInt(window.getComputedStyle(container).height);
}

// Set the size of the renderer to match the container
renderer.setSize(container.offsetWidth, container.offsetHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

renderer.useLegacyLights = false;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ReinhardToneMapping ;
renderer.toneMappingExposure = params.exposure;
renderer.shadowMap.enabled = true;

addEventListener("resize", () => {
    camera.aspect = getWidth() / getHeight();
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
}, false);

var scene = new THREE.Scene();

//ENVIRONMENT SETTINGS
new RGBELoader().load("../static/images/hdri/blouberg_sunrise_2_4k.hdr", (texture) =>{
    texture.mapping = THREE.EquirectangularReflectionMapping;
    texture.magFilter = THREE.NearestFilter;
    scene.background = texture;
    scene.environment = texture;
});

//texture settings
//define each texture name by an array
var textureNames = ['albedo.png', 'height.png', 'normal.png', 'roughness.png'];

var textures = [];

textureNames.forEach(function(textureName) {
    var img = new Image();
    img.src = '/static/images/pbr/' + textureName;
    img.onload = function() {
        textures[img]
    };
});

//load each texture to the respective 
// var textureLoader = new THREE.TextureLoader();
// var albedoTexture = textureLoader.load('../static/images/pbr/albedo.png');
// var bumpTexture = textureLoader.load('../static/images/pbr/height.png');
// var normalTexture = textureLoader.load('../static/images/pbr/normal.png');
// var roughnessTexture = textureLoader.load('../static/images/pbr/roughness.png');

var textureLoader = new THREE.TextureLoader();
var albedoTexture = textureLoader.load('../static/images/pbr/' + textureNames[0]);
var bumpTexture = textureLoader.load('../static/images/pbr/' + textureNames[1]);
var normalTexture = textureLoader.load('../static/images/pbr/' + textureNames[2]);
var roughnessTexture = textureLoader.load('../static/images/pbr/' + textureNames[3]);

//TEXTURE TILING
albedoTexture.wrapS = THREE.RepeatWrapping;
albedoTexture.wrapT = THREE.RepeatWrapping;
bumpTexture.wrapS = THREE.RepeatWrapping;
bumpTexture.wrapT = THREE.RepeatWrapping;
normalTexture.wrapS = THREE.RepeatWrapping;
normalTexture.wrapT = THREE.RepeatWrapping;
roughnessTexture.wrapS = THREE.RepeatWrapping;
roughnessTexture.wrapT = THREE.RepeatWrapping;

albedoTexture.repeat.set( params.tilingX, params.tilingY );
bumpTexture.repeat.set( params.tilingX, params.tilingY );
normalTexture.repeat.set( params.tilingX, params.tilingY );
roughnessTexture.repeat.set( params.tilingX, params.tilingY );

//mesh setting
const geometry = new THREE.SphereGeometry(1.8, 256, 256);

var ballMat = new THREE.MeshPhysicalMaterial({
    //load albedo texture
    map: albedoTexture,

    //load height texture
    displacementMap: bumpTexture,
    displacementScale:0.2, //displacement value; default = 1
    displacementBias: -0.05, //displacement offset; default = 0

    // load normal texture
    normalMap: normalTexture,
    normalScale: new THREE.Vector2(1,1), //normal value; range 0-1; default = (1,1)

    //load roughness texture
    roughnessMap: roughnessTexture,
    roughness: params.roughness, //roughness value; default = 1

    //specular settings
    reflectivity : params.reflectivity,
});

const sphere = new THREE.Mesh( geometry, ballMat );
sphere.position.set(0, 0, 0);
scene.add(sphere);

var camera = new THREE.PerspectiveCamera(50, container.offsetWidth / container.offsetHeight, 0.1, 1000);
camera.position.z = 5;

const controls = new OrbitControls( camera, renderer.domElement );
controls.update();

//---------------------------------LIGHTING SECTION-------------------------------------
const hemiLight = new THREE.HemisphereLight(0xffeeb1, 0x080820, 0.1);
scene.add(hemiLight);

const spotLight = new THREE.SpotLight(0xffa95c,0.5);
spotLight.position.set(-20,20,20);
spotLight.castShadow = true;
scene.add( spotLight );

spotLight.shadow.bias = -0.0001;
spotLight.shadow.mapSize.width = 1024*4;
spotLight.shadow.mapSize.height = 1024*4;

spotLight.position.set( 
    camera.position.x + 10,
    camera.position.y + 10,
    camera.position.z + 10,
);

//SHADOW AND ANISOTROPY SETTING
sphere.traverse(n => { if ( n.isMesh ) {
    n.castShadow = true; 
    n.receiveShadow = true;
    if(n.material.map) n.material.map.anisotropy = 16; 
}});

const light1 = new THREE.PointLight( 0xfc9403,0.2); //YELLOW
const light2 = new THREE.PointLight( 0x00ffc8,0.2) // BLUE
const light3 = new THREE.PointLight( 0xffffff,1); //WHITE
light1.position.set( 0, 0, 10 );
light2.position.set( -7, 2, 0 );
light3.position.set( 10, 2, -10 );
scene.add( light1 );
scene.add( light2 );
scene.add( light3 );
//---------------------------------END OF LIGHTING SECTION-------------------------------------

function animate() {
    requestAnimationFrame(animate);

    //UPDATING PARAMS FOR GUI CONTROLLER
    sphere.material.displacementScale = params.displacementScale;
    sphere.material.roughness = params.roughness;
    sphere.material.reflectivity = params.reflectivity;
    renderer.toneMappingExposure = params.exposure;

    //TEXTURE TILING UPDATE
    albedoTexture.repeat.set( params.tilingX, params.tilingY );
    bumpTexture.repeat.set( params.tilingX, params.tilingY );
    normalTexture.repeat.set( params.tilingX, params.tilingY );
    roughnessTexture.repeat.set( params.tilingX, params.tilingY );

    // SPHERE ANIMATION ACCORDING TO Y AXIS
    sphere.rotation.y += 0.005;
    controls.update();

    renderer.render(scene, camera);
}

// GUI Controller section
const gui = new GUI();
gui.add( sphere.material.normalScale,'x', 0, 1, 0.001 ).name("normal X");
gui.add( sphere.material.normalScale,'y', 0, 1, 0.001 ).name("normal Y");
gui.add( params, 'tilingX', 1, 10, 1 );
gui.add( params, 'tilingY', 1, 10, 1 );
gui.add( params, 'displacementScale', 0, 1, 0.01 );
gui.add( params, 'exposure', 0, 2, 0.01 );
gui.add( params, 'roughness', 0, 5, 0.01 );
gui.add( params, 'reflectivity', 0, 2, 0.01 );
gui.open();

animate();

