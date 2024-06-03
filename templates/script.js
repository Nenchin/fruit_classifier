// Set constraints for the video stream
var constraints = { video: { facingMode: "user" }, audio: false };
// Define constants
const cOutput = document.querySelector("#output");
const cSensor = document.querySelector("#sensor");
const cTrigger = document.querySelector("#camera--trigger");
const video = document.querySelector("#video");
// Start Cam function
const startCam = () => {
  //Initialize video
  

  // validate video element
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia(constraints)
      .then(function(stream) {
      track = stream.getTracks()[0];
        video.srcObject = stream;
      })
      .catch(function (error) {
        console.log("Something went wrong!");
      });
  }
};

// Stop the webcam function
const stopCam = () => {
  let stream = video.srcObject;
  let tracks = stream.getTracks();
  tracks.forEach((track) => track.stop());
  video.srcObject = null;
};

// Take a picture when cameraTrigger is tapped
// cTrigger.onclick = function() {
//  cSensor.width = video.videoWidth;
//  cSensor.height = video.videoHeight;
//  cSensor.getContext("2d").drawImage(video, 0, 0);
//  cOutput.src = cSensor.toDataURL("./static/images/webp");
//  cOutput.classList.add("taken");

cTrigger.onclick = function() {
    cSensor.width = video.videoWidth;
    cSensor.height = video.videoHeight;
    cSensor.getContext("2d").drawImage(video, 0, 0);
    cOutput.src = cSensor.toDataURL("./static/image");
    cOutput.classList.add("taken");
};

  // Send the data URL to the Flask endpoint for saving
//  fetch('/save_image', {
//    method: 'POST',
//    body: JSON.stringify({ 'image': cOutput.src }),
//    headers: { 'Content-Type': 'application/json' }
//})
//.then(function(response) {
//    console.log('Image saved successfully');
//})
//.catch(function(error) {
//    console.log('Error saving image: ' + error);
//});
//};

$(() => {
  startCam();
  stopCam();
});
