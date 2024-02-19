/*
 * #####
 *
 * This file Setup Left Bar and Tab Switching
 *
 * #####
 */

// Button and Tab elements
const buttons = {
  edit: document.getElementById("edit-btn"),
  monitor: document.getElementById("monitor-btn"),
  libs: document.getElementById("libs-btn"),
  add_lib: document.getElementById("add-lib-btn"),
};

const tabs = {
  edit: document.getElementById("edit-tab"),
  monitor: document.getElementById("monitor-tab"),
  libs: document.getElementById("libs-tab"),
  add_lib: document.getElementById("add-lib-tab"),
};

// Function to handle button click
const handleButtonClick = (buttonKey) => {
  // Set active button and hide other tabs
  for (let key in buttons) {
    if (buttonKey === key) {
      buttons[key].setAttribute("active", "");
      tabs[key].style.display = "flex";
    } else {
      buttons[key].removeAttribute("active");
      tabs[key].style.display = "none";
    }
  }
};

// Add event listeners
for (let key in buttons) {
  buttons[key].addEventListener("click", () => handleButtonClick(key));
}
