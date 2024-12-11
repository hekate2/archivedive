// Get links from angelfire directory page (don't forget to add links id to parent)
let links = document.querySelector("#tools table tr").querySelectorAll("a");
let str = "";

links.forEach((link) => {
  str += link + "\n";
});

console.log(str);
