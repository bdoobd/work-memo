"use strict";
import { API_BASE } from "./config.js";

navigation = document.querySelector(".nav__list");

navigation.addEventListener("click", (event) => {
  if (event.target.tagName == "A") console.log(event.target);
});
