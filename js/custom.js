// custom.js
// Author: Kat Herring
// Custom JavaScript for Kat's Portfolio


function runClock() {
  var currTime = new Date();
  var hour = currTime.getHours();
  var day = currTime.getDay(); // 0 = Sunday, 5 = Friday

  var recall = setTimeout(runClock, 1800000); // call every 30min

  if (hour > 23 || hour < 8) {
    currStatus = "sleeping";
    currDesc = "Sleeping (Ideally)";
  } else if (day === 0 || day === 5) {
    currStatus = "free";
    currDesc = "Personal Projects! (Ideally)";
  } else {
    currStatus = "working";
    currDesc = "Coursework and Related Activity";
  }

  setStatus(currStatus, currDesc);
};

function setStatus(currStatus, currDesc) {
  var color = "danger"; // default
  if ( currStatus==="sleep" ) {
    color = "primary";
  } else if ( currStatus === "free" ) {
    color = "success"
  }
  var statushtml = '<strong class="text-' + color + '">' + currStatus.toUpperCase() + "</strong> - " + currDesc;

  $("#about-status")[0].innerHTML = statushtml;
};
