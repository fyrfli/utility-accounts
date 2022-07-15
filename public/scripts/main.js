'use strict';

// Full year for footer
const todayDate = new Date();
jsyear.innerText = todayDate.getFullYear();

const resultFld = document.querySelector(".results");
const optionsSelect = document.querySelectorAll(".lnk");
const dataFile = "assets/accounts.json";
const dataArr = [];
let i = 0;

fetch(dataFile)
.then((response) => {
  if (!response.ok) {
    resultFld.innerText = "Fetch returned: " + response;
  }
  else {
    return response.json();
  }
})
.then((data) => {
  for(i in data) {
    dataArr.push([i], data [i]);
  }
  resultFld.innerText = dataArr[0];
})

