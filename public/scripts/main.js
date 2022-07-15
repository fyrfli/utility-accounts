'use strict';

// Full year for footer
const todayDate = new Date();
jsyear.innerText = todayDate.getFullYear();

const resultFld = document.querySelector(".results");
const optionsSelect = document.querySelectorAll(".lnk");

resultFld.innerText = Object.keys(optionsSelect);
