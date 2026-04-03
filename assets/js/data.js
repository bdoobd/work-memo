"use strict";

const openButton = document.getElementById("start");
const dialog = document.getElementById("data_dialog");
const startDateInput = document.getElementById("start_date");

startDateInput.addEventListener("change", () => {
  if (startDateInput.value) {
    openButton.disabled = false;
  } else {
    openButton.disabled = true;
  }
});

openButton.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.showModal();

  const dateElement = document.querySelector(".working-date");
  const selectedDate = startDateInput.value;
  dateElement.textContent = `Дата: ${selectedDate}`;
});
