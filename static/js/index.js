let statusMsg = document.querySelector("#status-msg");
let video = document.querySelector("#video");
let start_button = document.querySelector("#start-record");
let stop_button = document.querySelector("#stop-record");
let download_link = document.querySelector("#download-video");
const uploadBtn = document.querySelector("#upload-btn");
const personNameInput = document.querySelector("#person-name");

const videoFeeds = document.getElementById("video-feeds");
let camera_stream = null;
let media_recorder = null;

let intermediary_blobs_recorded = [];
let finalRecoredVideoBlob = null;

const addNewVideoFeed = (videoSrc) => {
  videoFeeds.innerHTML = "";
  const newVid = document.createElement("video");
  newVid.src = videoSrc;
  newVid.controls = true;
  newVid.muted = true;
  newVid.autoplay = true;
  newVid.style.width = '95%';
  videoFeeds.append(newVid);
  intermediary_blobs_recorded = [];
};

window.onload = async () => {
  statusMsg.innerText = "Camera loaded";
  camera_stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true,
  });
  video.srcObject = camera_stream;
};

start_button.addEventListener("click", function () {
  stop_button.style = "display:block;";
  statusMsg.innerText = "recording...";
  media_recorder = new MediaRecorder(camera_stream, { mimeType: "video/webm" });
  media_recorder.addEventListener("dataavailable", function (e) {
    console.log(e.data);
    console.log(URL.createObjectURL(e.data));
    intermediary_blobs_recorded.push(e.data);
  });

  // event : recording stopped & all blobs sent
  media_recorder.addEventListener("stop", function () {
    start_button.innerText = "Try again";
    statusMsg.innerText = "Recorded.. Try pressing start to try again";
    finalRecoredVideoBlob = new Blob(intermediary_blobs_recorded, {
      type: "video/webm",
    });
    let video_local = URL.createObjectURL(finalRecoredVideoBlob);
    addNewVideoFeed(video_local);
    download_link.href = video_local;
  });

  // start recording with each recorded blob having 0.1 second video
  media_recorder.start(1000);
});

stop_button.addEventListener("click", function () {
  media_recorder.stop();
  stop_button.style = "display:none;";
});

uploadBtn.addEventListener("click", () => {
  if (!personNameInput.value) {
    return alert("Enter name")
  }
  var data = new FormData();
  data.append("file", finalRecoredVideoBlob, personNameInput.value);
  fetch("/upload", {
    method: "POST",
    body: data,
  }).then((resp) => {
    console.log(resp);
    alert("File uploaded successfully and is being processed")
    personNameInput.value = ""
  }).catch(err => {
    console.log(err);
    alert("There seems to be some error in uploading file..  please check again")
  })
});
