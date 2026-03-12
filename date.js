"use strict";

const logo = document.querySelector(".header__logo");
const today_btn = document.querySelector("#today");
const date_field = document.querySelector("#start_date");
const today = new Date();
const weekdays = [
  "Понедельник",
  "Вторник",
  "Среда",
  "Четверг",
  "Пятница",
  "Суббота",
  "Воскресенье",
];

logo.textContent = `${weekdays[today.getDay() - 1]} ${today.getDate()}.${(today.getMonth() + 1).toString().padStart(2, "0")}.${today.getFullYear()}`;

today_btn.addEventListener("click", () => {
  date_field.value = `${today.getFullYear()}-${(today.getMonth() + 1).toString().padStart(2, "0")}-${today.getDate()}`;
});
