"use strict";

const logo = document.querySelector(".header__logo");
const today_btn = document.querySelector("#today");
const date_field = document.querySelector("#start_date");
const startButton = document.querySelector("#start");
const today = new Date();
const weekdays = [
  "Воскресенье",
  "Понедельник",
  "Вторник",
  "Среда",
  "Четверг",
  "Пятница",
  "Суббота",
];

logo.textContent = `${weekdays[today.getDay()]} ${today.getDate()}.${(today.getMonth() + 1).toString().padStart(2, "0")}.${today.getFullYear()}`;

today_btn.addEventListener("click", () => {
  date_field.value = `${today.getFullYear()}-${(today.getMonth() + 1).toString().padStart(2, "0")}-${today.getDate().toString().padStart(2, "0")}`;

  startButton.disabled = false;
});
