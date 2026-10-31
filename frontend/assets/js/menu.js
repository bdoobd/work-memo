"use strict";
import { API_BASE } from "./config.js";

navigation = document.querySelector(".nav__list");

navigation.addEventListener("click", (event) => {
  if (event.target.tagName == "A") {
    console.log(event.target);
    console.log(`${API_BASE}/users/`);
    fetchUsers();
    }
});

async function fetchUsers() {
  try {
    const response = await fetch(`${API_BASE}/users/`);
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("Error fetching users:", error);
  }
}