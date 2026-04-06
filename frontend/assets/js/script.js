"use strict";
const nav = document.querySelector(".nav");
const hamburger = document.querySelector(".hamburger");

hamburger.addEventListener("click", () => {
  nav.classList.toggle("nav__open");
  hamburger.classList.toggle("hamburger__open");
});

nav.addEventListener("click", () => {
  nav.classList.remove("nav__open");
  hamburger.classList.remove("hamburger__open");
});
