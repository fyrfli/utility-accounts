'use strict';

const todayDate = new Date();
jsyear.innerText = todayDate.getFullYear();

const mainHdg = document.querySelector(".main-hdg");
const mainPara = document.querySelector(".main-para");
let dataFile = "";
const theOpt = document.querySelectorAll(".opt");
theOpt.addEventListener('click', function () {
 mainPara.textContent = currentTarget();
});
mainPara.innerText = Object.values(theOpt);

fetch("../assets/datatwo.json")
  .then((response) => {
    if (!response.ok) {
      mainPara.textContent = "Fetch returned: " + response.status;
    }
    else {
      return response.json();
    }
  })
  .then((data) => {
    // mainPara.innerText = "yay! data!  " + JSON.stringify(data);
    data.forEach((u) => {
      // if (u.name == "water") {
      //   mainPara.textContent = u.name + " due: " + u.duedate;
      // }
      //mainPara.textContent += "\n" + u.name;
    })
  });