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
    xhr.open('post', '/upload', true); // aussume that the urDl /upload handles uploading.
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

// -----------------------------CLICKABLE DIV-----------------------------
// Get references to the clickable div and file input element
var clickableDiv = document.getElementById('drop_area');
var fileInput = document.getElementById('fileInput');

// Add a click event listener to the clickable div
clickableDiv.addEventListener('click', function (e) {
    // Trigger the click event on the file input element
    fileInput.click();
});
  
document.getElementById('fileInput').addEventListener('change', function(event) {
var selectedImage = document.getElementById('picture');
// var files = event.target.files[0];
var files = fileInput.files;

for (var i = 0; i < files.length; i++) {
    var file = files[i];
    console.log('File name:', file.name);
    console.log('File type:', file.type);
    console.log('File size:', file.size);
  }

// Send the FormData object to the Flask backend using an AJAX request
var xhr = new XMLHttpRequest();
xhr.open('POST', '/upload', true);
xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        // Request completed successfully
        alert('Successfully uploaded!');  // please replace with your own logic
        reloadImage()
    }
};

// send files to server
xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
var fd = new FormData();
for (let file of files) {
    fd.append('image', file);
}
xhr.send(fd);

// Create a FileReader object to read the selected file
var reader = new FileReader();
reader.onload = function() {
    selectedImage.src = reader.result;
};
reader.readAsDataURL(file);
});
  

// -----------------------------refresh certain content---------------

function reloadImage() {
    var imageElement = document.getElementById('picture');

    // Add a timestamp query parameter to the image URL to force reload
    // var timestamp = new Date().getTime();
    var imageUrl = imageElement.src + '?t=';

    // Set the updated URL to the image element
    imageElement.src = imageUrl;
}