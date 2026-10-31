"use strict";

const openButton = document.getElementById("start");
const dialog = document.getElementById("data_dialog");
const form = document.querySelector(".data_dialog__form");
const startDateInput = document.getElementById("start_date");
const cancelButton = document.getElementById("cancel");
const confirmButton = document.getElementById("confirm");

// startDateInput.addEventListener("change", () => {
//   if (startDateInput.value) {
//     openButton.disabled = false;
//   } else {
//     openButton.disabled = true;
//   }
// });

// openButton.addEventListener("click", (e) => {
//   e.preventDefault();
//   dialog.showModal();

//   const dateElement = document.querySelector(".working-date");
//   // TODO: Отправить запрос на API для добавления рабочего дня в баунд и получения его ID
//   const selectedDate = startDateInput.value;

//   console.log(typeof selectedDate, selectedDate);

//   dateElement.textContent = `${selectedDate.split("-").reverse().join(".")}`;
// });

cancelButton.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.close();
});

confirmButton.addEventListener("click", (e) => {
  e.preventDefault();
  let formData = new FormData(form);
  const selectedDate = startDateInput.value;
  // localStorage.setItem("selectedDate", selectedDate);
  console.log(selectedDate);
  console.log(Object.fromEntries(formData.entries()));
  // TODO: Отправить данные формы на API для создания рабочего периода для рабочего дня
  dialog.close();
});
