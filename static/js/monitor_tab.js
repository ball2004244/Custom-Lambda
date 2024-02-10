import config from "./config.js";

/*
 * This file handle the monitor tab
 */
// Monitor container element
const monitorContainer = document.getElementById("monitor-container");

// Get all cloud functions
async function fetchData() {
  try {
    const response = await fetch(`${config.API_URL}/functions`);
    const data = await response.json();
    return data.data.functions;
  } catch (error) {
    console.error(error);
  }
}

// Display data in as a table
function displayData(funcs) {
  // Check if there are no functions
//   then display a message
    if (funcs === null || funcs === undefined) {
        monitorContainer.innerHTML = "<p><strong>No functions found</strong></p>";
        return;
    }

    if (Object.keys(funcs).length === 0) {
        monitorContainer.innerHTML = "<p><strong>No functions found</strong></p>";
        return;
    }
  const table = document.createElement("table");
  table.classList.add("funcs-table");

  // Create table header
  const header = document.createElement("tr");
  const keyHeader = document.createElement("th");
  keyHeader.textContent = "ith Function Store";
  header.appendChild(keyHeader);
  const valueHeader = document.createElement("th");
  valueHeader.textContent = "Function Names";
  header.appendChild(valueHeader);
  table.appendChild(header);

  // Loop through functions
  Object.keys(funcs).forEach((key) => {
    const row = document.createElement("tr");
    const keyCell = document.createElement("th");
    keyCell.textContent = key;
    row.appendChild(keyCell);

    const valueCell = document.createElement("td");
    const ul = document.createElement("ul");
    funcs[key].forEach((value) => {
      const li = document.createElement("li");
      li.textContent = value;
      ul.appendChild(li);
    });

    valueCell.appendChild(ul);
    row.appendChild(valueCell);
    table.appendChild(row);
  });

  // Clear the previous table
  while (monitorContainer.firstChild) {
    monitorContainer.removeChild(monitorContainer.firstChild);
  }

  monitorContainer.appendChild(table);
}

// Fetch and display data every 5 seconds
setInterval(async () => {
  const data = await fetchData();
  displayData(data);
}, 5000);
