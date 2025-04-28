const WIGGLE_NUM_LET = 20;
const WIGGLE_OFFSET = 5;

// @ts-ignore
export default function bounceDat(text) {
  let words = text.textContent || "";
  text.innerHTML = "";

  for (let j = 0; j < words.length; j++) {
    let sp = document.createElement("span");
    sp.textContent = words[j];
    // Maybe some day these letters will be colorful...
    // sp.style.color = "hsl(" + Math.floor(Math.random() * 361) + ", 100%, 50%)";

    text.appendChild(sp);
  }

  let loop = 0;
  let timerId = setInterval(() => {
    text.children[loop].style.top = -WIGGLE_OFFSET + "px";

    if (loop > 0) {
      text.children[loop - 1].style.top = "0px";
    } else {
      text.children[text.children.length - 1].style.top = "0px";
    }

    loop++;
    if (loop >= text.children.length) {
      loop = 0;
    }
  }, 100);
}