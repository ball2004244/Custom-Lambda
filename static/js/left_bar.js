/*
 * This file Setup Left Bar and Tab Switching
 */
// Button elements
const editBtn = document.getElementById("edit-btn");
const monitorBtn = document.getElementById("monitor-btn");

// Tab elements
const editTab = document.getElementById("edit-tab");
const monitorTab = document.getElementById("monitor-tab");

// Edit button click event
editBtn.addEventListener("click", () => {
  editBtn.setAttribute("active", "");
  monitorBtn.removeAttribute("active");
  editTab.style.display = "flex";
  monitorTab.style.display = "none";
});

// Monitor button click event
monitorBtn.addEventListener("click", () => {
  monitorBtn.setAttribute("active", "");
  editBtn.removeAttribute("active");
  monitorTab.style.display = "flex";
  editTab.style.display = "none";
});
