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
  const libList = Array.from(preInstallList.children).map(
    (li) => li.textContent
  );
  const sendData = { libs: libList };
  try {
    const response = await fetch(`${config.API_URL}/libs`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sendData),
    });
    const data = await response.json();
    console.log(data);
    preInstallList.innerHTML = "";
  } catch (error) {
    console.error("Error uploading libraries:", error);
  }
});

// Libraries container element
const libsContainer = document.getElementById("libs-container");

// Get all libraries
const fetchLibsData = async () => {
  try {
    const response = await fetch(`${config.API_URL}/libs`, {
      method: "GET",
      credentials: "same-origin",
    });
    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error("Error fetching libraries:", error);
    return [];
  }
};

// Display data as a list
const displayData = (libs) => {
  // Convert the string of libraries into an array
  if (typeof libs === "string") {
    libs = libs.split("\n").filter((lib) => lib.trim() !== "");
  }

  // Check if there are no libraries
  if (!Array.isArray(libs) || libs.length === 0) {
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
  const libs = await fetchLibsData();
  displayData(libs);
}, 5000);
