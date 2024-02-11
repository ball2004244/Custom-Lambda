import config from "./config.js";
/*
 * #####
 *
 * This file handle the monitor tab
 *
 * #####
 */

// Monitor container element
const monitorContainer = document.getElementById("monitor-container");
const displayContainer = document.getElementById("display-res-container");
const funcNameElement = document.getElementById("func-name");
const paramsTable = document.getElementById("params-table");
const executeButton = document.getElementById("execute-btn");
const closeButton = document.getElementById("close-res-container");

// Get all cloud functions
// TODO: Get each function instead of all functions
const fetchData = async () => {
  try {
    const response = await fetch(`${config.API_URL}/functions`);
    const data = await response.json();
    return data.data.functions;
  } catch (error) {
    console.error(error);
  }
};


// Display data in as a paginated format
const displayData = (funcs) => {
  // Check if there are no functions
  //   then display a message
  if (
    funcs === null ||
    funcs === undefined ||
    Object.keys(funcs).length === 0
  ) {
    monitorContainer.innerHTML = "<p><strong>No functions found</strong></p>";
    return;
  }

  // Flatten the functions into a single array
  const flatFuncs = [];
  Object.keys(funcs).forEach((key) => {
    funcs[key].forEach((value) => {
      flatFuncs.push({ key, ...value });
    });
  });

  // Calculate the number of pages
  const pageSize = 25; // 5x5
  const numPages = Math.ceil(flatFuncs.length / pageSize);

  // Create the pagination buttons
  const pagination = document.createElement("div");
  for (let i = 0; i < numPages; i++) {
    const button = document.createElement("button");
    button.textContent = i + 1;
    button.addEventListener("click", () => displayPage(flatFuncs, i, pageSize));
    pagination.appendChild(button);
  }
  monitorContainer.appendChild(pagination);

  // Display the first page
  displayPage(flatFuncs, 0, pageSize);
};

// Display a page of functions
const displayPage = (funcs, pageIndex, pageSize) => {
  // Remove previous page
  while (monitorContainer.firstChild) {
    monitorContainer.removeChild(monitorContainer.firstChild);
  }

  // Create a grid for the functions
  const grid = document.createElement("div");
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "repeat(5, 1fr)";
  grid.style.gridGap = "10px";

  // Add the functions to the grid
  const start = pageIndex * pageSize;
  const end = start + pageSize;
  for (let i = start; i < end && i < funcs.length; i++) {
    const button = document.createElement("button");
    button.textContent = funcs[i].function;
    button.addEventListener("click", () => displayFunctionDetails(funcs[i]));
    grid.appendChild(button);
  }

  monitorContainer.appendChild(grid);
};

// Display the details of a function
const displayFunctionDetails = (func) => {
  // Clear previous function details
  funcNameElement.textContent = func.function;
  paramsTable.innerHTML = '';

  // Add the function parameters to paramsTable
  func.params.forEach((param) => {
    const row = document.createElement("tr");
    const nameCell = document.createElement("th");
    nameCell.textContent = param;
    row.appendChild(nameCell);
    const valueCell = document.createElement("th");
    const input = document.createElement("input");
    input.type = "text";
    input.classList.add("param-value-input");
    valueCell.appendChild(input);
    row.appendChild(valueCell);
    paramsTable.appendChild(row);
  });

  // Show displayContainer
  displayContainer.style.display = 'flex';
};

// Execute a function
executeButton.addEventListener("click", async () => {
  const params = Array.from(document.getElementsByClassName("param-value-input")).map(input => input.value);
  const response = await fetch(`${config.API_URL}/execute/${funcNameElement.textContent}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ params, target: funcNameElement.textContent }),
  });
  const data = await response.json();
  console.log(data);
});

// Close the function details
closeButton.addEventListener("click", () => {
  displayContainer.style.display = 'none';
});

// Fetch and display data every 5 seconds
setInterval(async () => {
  const data = await fetchData();
  displayData(data);
}, 5000);
