import * as THREE from 'https://cdn.skypack.dev/three@0.132.2';

var container = document.getElementById('container');
var renderer = new THREE.WebGLRenderer();

// Set the background color to grey
renderer.setClearColor(0x888888);

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

//make it responsive (dynamic size)
// window.addEventListener('resize', function()
// {
// 	var width = window.innerWidth;
// 	var height = window.innerHeight;
// 	renderer.setSize(width,height);
// 	camera.aspect = width/height;
// 	camera.updateProjectionMatrix();
// });

addEventListener("resize",() => {
    camera.aspect = getWidth() / getHeight();
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
},false);

var scene = new THREE.Scene();

const geometry = new THREE.BoxGeometry( 1, 1, 1 );
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

var camera = new THREE.PerspectiveCamera(45, container.offsetWidth / container.offsetHeight, 0.1, 1000);
camera.position.z = 5;

// Add your scene objects, lights, etc.

// Render the scene
renderer.render(scene, camera);


function animate() {
	requestAnimationFrame( animate );

	cube.rotation.x += 0.01;
	cube.rotation.y += 0.01;

	renderer.render( scene, camera );
}

animate();

// ----------------------------------UPLOAD SECTION----------------------------

// prevent the default behavior of web browser
['dragleave', 'drop', 'dragenter', 'dragover'].forEach(function (evt) {
    document.addEventListener(evt, function (e) {
        e.preventDefault();
    }, false);
});

var drop_area = document.getElementById('drop_area');
drop_area.addEventListener('drop', function (e) {
    e.preventDefault();
    var fileList = e.dataTransfer.files; // the files to be uploaded
    if (fileList.length == 0) {
        return false;
    }

    // we use XMLHttpRequest here instead of fetch, because with the former we can easily implement progress and speed.
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/upload', true); // aussume that the url /upload handles uploading.
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // uploading is successful
            alert('Successfully uploaded!');  // please replace with your own logic
            reloadImage();
        }
    };

    // show uploading progress
    var lastTime = Date.now();
    var lastLoad = 0; 
    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            // update progress
            var percent = Math.floor(event.loaded / event.total * 100);
            document.getElementById('upload_progress').textContent = percent + '%';

            // update speed
            var curTime = Date.now();
            var curLoad = event.loaded;
            var speed = ((curLoad - lastLoad) / (curTime - lastTime) / 1024).toFixed(2);
            document.getElementById('speed').textContent = speed + 'MB/s'
            lastTime = curTime;
            lastLoad = curLoad;
        }
    };

    // send files to server
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    var fd = new FormData();
    for (let file of fileList) {
        fd.append('image', file);
    }
    lastTime = Date.now();
    xhr.send(fd);
}, false);


// -----------------------------refresh certain content---------------

function reloadImage() {
    var imageElement = document.getElementById('picture');

    // Add a timestamp query parameter to the image URL to force reload
    // var timestamp = new Date().getTime();
    var imageUrl = imageElement.src + '?t=';

    // Set the updated URL to the image element
    imageElement.src = imageUrl;
}