import config from "./config.js";
/*
 * #####
 *
 * This file is used to view/edit libraries in server
 *
 * #####
 */


// Add libs to preinstall list on enter
const addLibInput = document.getElementById("add-lib-input");
const preInstallList = document.getElementById("libs-list");

addLibInput.addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    const li = document.createElement("li");
    li.textContent = addLibInput.value;
    preInstallList.appendChild(li);
    addLibInput.value = "";
  }
});

// Delete preinstall list on click
const deleteList = document.getElementById("delete-libs-btn");
deleteList.addEventListener("click", () => {
  preInstallList.innerHTML = "";
});

// Upload preinstall list to server
const uploadList = document.getElementById("upload-libs-btn");
uploadList.addEventListener("click", async () => {
  const lib_list = Array.from(preInstallList.children).map(
    (li) => li.textContent
  );
  const send_data = { libs: lib_list };
  const response = await fetch(`${config.API_URL}/libs`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(send_data),
  });
  const data = await response.json();
  console.log(data);
  preInstallList.innerHTML = "";
});

// Libraries container element
const libsContainer = document.getElementById("libs-container");

// Get all libraries
const libsData = async () => {
  try {
    const response = await fetch(`${config.API_URL}/libs`, {
      method: "GET",
      credentials: "same-origin",
    });
    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error(error);
  }
};

// Display data as a list
const displayData = (libs) => {
  // Check if there are no libraries
  //   then display a message
  if (libs === null || libs === undefined || libs.length === 0) {
    libsContainer.innerHTML = "<p><strong>No libraries found</strong></p>";
    return;
  }

  const ul = document.createElement("ul");
  ul.classList.add("libs-list");

  // Loop through libraries Array
  libs.forEach((lib) => {
    const li = document.createElement("li");
    li.textContent = lib;
    ul.appendChild(li);
  });

  libsContainer.innerHTML = "";
  libsContainer.appendChild(ul);
};

// Get data every 5 seconds
setInterval(async () => {
  const libs = await libsData();
  displayData(libs);
}, 5000);
