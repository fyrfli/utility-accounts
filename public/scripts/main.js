'use strict';

const todayDate = new Date();
jsyear.innerText = todayDate.getFullYear();

const mainHdg = document.querySelector(".main-hdg");
const mainPara = document.querySelector(".main-para");
let dataFile = "assets/datatwo.json";
const theOpt = document.querySelectorAll(".opt");


fetch(dataFile)
  .then((response) => {
    if (!response.ok) {
      mainPara.textContent = "Fetch returned: " + response.status;
    }
    else {
      return response.json();
    }
  })
  .then((data) => {
    mainPara.innerText = Object.entries(data);
  });