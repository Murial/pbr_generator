function urlToPromise(url) {
    return new Promise(function(resolve, reject) {
        JSZipUtils.getBinaryContent(url, function (err, data) {
            if(err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    });
}

$("#download_form").on("submit", function () {
    resetMessage();

    var zip = new JSZip();
    

    // when everything has been downloaded, we can trigger the dl
    zip.generateAsync({type:"blob"}, function updateCallback(metadata) {
        var msg = "progression : " + metadata.percent.toFixed(2) + " %";
        if(metadata.currentFile) {
            msg += ", current file = " + metadata.currentFile;
        }
        showMessage(msg);
        updatePercent(metadata.percent|0);
    })
        .then(function callback(blob) {

            // see FileSaver.js
            saveAs(blob, "example.zip");

            showMessage("done !");
        }, function (e) {
            showError(e);
        });

    return false;
});