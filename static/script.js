// Configure require.js paths
require.config({
    paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.20.0/min/vs",
    },
});

// Load Monaco Editor
require(["vs/editor/editor.main"], () => {
    const content = "# Your Python code here";
    const editor = monaco.editor.create(document.getElementById("monaco-container"), {
        value: content,
        language: "python",
        theme: "vs-dark",
    });
});

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

// Monitor container element
const monitorContainer = document.getElementById("monitor-container");

// Fetch available functions and display as a table
fetch("http://localhost:7000/api/functions")
    .then((response) => response.json())
    .then((data) => {
        const funcs = data.data.functions;
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

        monitorContainer.appendChild(table);
    });
