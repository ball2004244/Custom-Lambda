import config from "./config.js";

/*
 * #####
 *
 * This file handle the monitor tab
 *
 * #####  const funcStore = document.getElementById("func-store");

 */

// DOM elements
const monitorContainer = document.getElementById("monitor-container");
const displayContainer = document.getElementById("display-res-container");
const funcNameElement = document.getElementById("func-name");
const funcStoreElement = document.getElementById("func-store");
const paramsTable = document.getElementById("params-table");
const executeButton = document.getElementById("execute-btn");
const closeButton = document.getElementById("close-res-container");
const resContainer = document.getElementById("display-res");

// Fetch all cloud functions from the server
const fetchFunctions = async () => {
  try {
    const response = await fetch(`${config.API_URL}/users/functions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: "test",
        password: "test"
      }),
      credentials: "same-origin",
    });

    if (!response.ok) {
      const errorData = await response.json();
      if (errorData.detail && errorData.detail[0] && errorData.detail[0].type === "missing") {
        console.error("Field required error on fetching user functions: ", errorData);
      } else {
        console.error("An error occurred on fetching user functions: ", errorData);
      }
      return; // Exit the function after handling the error
    }

    const data = await response.json();
    return data.data.functions;
  } catch (error) {
    console.error("Fetch error: ", error);
  }
};

// Display the fetched functions in a paginated format
const displayFunctions = (functions) => {
  if (isEmpty(functions)) {
    displayNoFunctionsMessage();
    return;
  }

  const flattenedFunctions = flattenFunctions(functions);
  const pageSize = 25; // 5x5
  const numberOfPages = calculateNumberOfPages(flattenedFunctions, pageSize);

  createPaginationButtons(numberOfPages, flattenedFunctions, pageSize);
  displayPage(flattenedFunctions, 0, pageSize);
};

// Check if the functions object is empty
const isEmpty = (functions) => {
  return (
    functions === null ||
    functions === undefined ||
    Object.keys(functions).length === 0
  );
};

// Display a message when no functions are found
const displayNoFunctionsMessage = () => {
  monitorContainer.innerHTML = "<p><strong>No functions found</strong></p>";
};

// Flatten the functions into a single array
const flattenFunctions = (functions) => {
  const flatFuncs = [];
  Object.keys(functions).forEach((key) => {
    functions[key].forEach((value) => {
      flatFuncs.push({ key, ...value });
    });
  });
  return flatFuncs;
};

// Calculate the number of pages
const calculateNumberOfPages = (flattenedFunctions, pageSize) => {
  return Math.ceil(flattenedFunctions.length / pageSize);
};

// Create the pagination buttons
const createPaginationButtons = (
  numberOfPages,
  flattenedFunctions,
  pageSize
) => {
  const pagination = document.createElement("div");
  for (let i = 0; i < numberOfPages; i++) {
    const button = createPaginationButton(i, flattenedFunctions, pageSize);
    pagination.appendChild(button);
  }
  monitorContainer.appendChild(pagination);
};

// Create a single pagination button
const createPaginationButton = (pageIndex, flattenedFunctions, pageSize) => {
  const button = document.createElement("button");
  button.textContent = pageIndex + 1;
  button.addEventListener("click", () =>
    displayPage(flattenedFunctions, pageIndex, pageSize)
  );
  return button;
};

// Display a page of functions
const displayPage = (flattenedFunctions, pageIndex, pageSize) => {
  clearMonitorContainer();
  const grid = createGrid();
  addFunctionsToGrid(flattenedFunctions, pageIndex, pageSize, grid);
  monitorContainer.appendChild(grid);
};

// Clear the monitor container
const clearMonitorContainer = () => {
  while (monitorContainer.firstChild) {
    monitorContainer.removeChild(monitorContainer.firstChild);
  }
};

// Create a grid for the functions
const createGrid = () => {
  const grid = document.createElement("div");
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "repeat(5, 1fr)";
  grid.style.gridGap = "10px";
  return grid;
};

// Add the functions to the grid
const addFunctionsToGrid = (flattenedFunctions, pageIndex, pageSize, grid) => {
  const start = pageIndex * pageSize;
  const end = start + pageSize;
  for (let i = start; i < end && i < flattenedFunctions.length; i++) {
    const button = createFunctionButton(flattenedFunctions[i]);
    grid.appendChild(button);
  }
};

// Create a button for a single function
const createFunctionButton = (func) => {
  const button = document.createElement("button");
  button.textContent = func.function;
  button.style.width = "200px"; // Set the default width of the button to 200px
  button.style.fontSize = "14px";
  button.addEventListener("click", () => displayFunctionDetails(func));
  return button;
};

// Display the details of a function
const displayFunctionDetails = (func) => {
  clearFunctionDetails();
  populateFunctionDetails(func);
  displayContainer.style.display = "flex";
};

// Clear the previous function details
const clearFunctionDetails = () => {
  funcNameElement.textContent = "";
  funcStoreElement.textContent = "";
  paramsTable.innerHTML = "";
};

// Populate the function details
const populateFunctionDetails = (func) => {
  funcNameElement.textContent = func.function;
  funcStoreElement.textContent = func.key;

  const params = func.params;
  const dataTypes = ["String", "Number", "Boolean", "Object", "Array"]; // Add more data types as needed

  for (let i = 0; i < params.length; i++) {
    const row = createParamRow(params[i], dataTypes);
    paramsTable.appendChild(row);
  }
};

// Create a row for a single parameter
const createParamRow = (param, dataTypes) => {
  const row = document.createElement("tr");

  const nameCell = createNameCell(param);
  row.appendChild(nameCell);

  const dataTypeCell = createDataTypeCell(dataTypes);
  row.appendChild(dataTypeCell);

  const valueCell = createValueCell();
  row.appendChild(valueCell);

  return row;
};

// Create the name cell for a parameter
const createNameCell = (param) => {
  const nameCell = document.createElement("th");
  nameCell.textContent = param;
  return nameCell;
};

// Create the data type cell for a parameter
const createDataTypeCell = (dataTypes) => {
  const dataTypeCell = document.createElement("th");
  const select = createDataTypeSelect(dataTypes);
  dataTypeCell.appendChild(select);
  return dataTypeCell;
};

// Create the data type select for a parameter
const createDataTypeSelect = (dataTypes) => {
  const select = document.createElement("select");
  select.classList.add("data-type-select");
  dataTypes.forEach((dataType) => {
    const option = createOption(dataType);
    select.appendChild(option);
  });
  return select;
};

// Create an option for the data type select
const createOption = (dataType) => {
  const option = document.createElement("option");
  option.value = dataType;
  option.text = dataType;
  return option;
};

// Create the value cell for a parameter
const createValueCell = () => {
  const valueCell = document.createElement("th");
  const input = createInput();
  valueCell.appendChild(input);
  return valueCell;
};

// Create the input for the value cell
const createInput = () => {
  const input = document.createElement("input");
  input.type = "text";
  input.classList.add("param-value-input");
  return input;
};

// Display the result of executing a function
const displayExecResult = (res) => {
  clearExecResult();
  populateExecResult(res);
};

// Clear the previous execution result
const clearExecResult = () => {
  resContainer.innerHTML = "";
};

// Populate the execution result
const populateExecResult = (res) => {
  console.log(res);
  const returnResult = createResultElement("Return Result", res.return_value);
  resContainer.appendChild(returnResult);

  const stdout = createResultElement("Console Output", res.stdout);
  resContainer.appendChild(stdout);

  const stderr = createResultElement("Console Error", res.stderr);
  resContainer.appendChild(stderr);
};

// Create a p element for a single result
const createResultElement = (label, result) => {
  const p = document.createElement("p");
  p.textContent = `${label}: ${result}`;
  return p;
};

// Fetch and display functions
const fetchAndDisplayFunctions = async () => {
  const functions = await fetchFunctions();
  displayFunctions(functions);
};

// Execute a function
const executeFunction = async () => {
  const params = getParams();
  const funcName = funcNameElement.textContent;
  const target = funcStoreElement.textContent;

  const response = await sendExecuteRequest(funcName, target, params);
  const data = await response.json();

  displayExecResult(data.data);
};

// Get the parameters from the input fields
const getParams = () => {
  const paramInputs = Array.from(
    document.getElementsByClassName("param-value-input")
  );
  const dataTypeSelects = Array.from(
    document.getElementsByClassName("data-type-select")
  );

  return paramInputs.map((input, index) => {
    const dataType = dataTypeSelects[index].value;
    return castValue(dataType, input.value);
  });
};

// Send the execute request to the server
const sendExecuteRequest = async (funcName, target, params) => {
  const send_data = {
    params: params,
    target: target,
    username: "test",
    password: "test",
  };

  try {
    const response = await fetch(`${config.API_URL}/execute/${funcName}`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Server error on executing function: ", errorData);
    }

    return response;

  } catch (error) {
    console.error("Error on executing function: ", error);
    return response;
  }

};

// Close the function details
const closeFunctionDetails = () => {
  displayContainer.style.display = "none";
};

// Cast a value to the correct type
const castValue = (dataType, value) => {
  switch (dataType) {
    case "String":
      return String(value);
    case "Number":
      return Number(value);
    case "Boolean":
      return value.toLowerCase() === "true";
    case "Object":
    case "Array":
      return JSON.parse(value);
    default:
      return value;
  }
};

// Execute a function when the execute button is clicked
executeButton.addEventListener("click", executeFunction);

// Close the function details when the close button is clicked
closeButton.addEventListener("click", closeFunctionDetails);

// Fetch and display functions every 5 seconds
setInterval(fetchAndDisplayFunctions, 5000);
