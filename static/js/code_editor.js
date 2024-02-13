import config from "./config.js";

/*
 * #####
 *
 * This file Setup Monaco Editor and Code Submission
 *
 * #####
 */
const submitBtn = document.getElementById("submit-btn");

// Configure require.js paths
require.config({
  paths: {
    vs: config.MONACO_EDITOR_URL,
  },
});

// Load Monaco Editor
require(["vs/editor/editor.main"], () => {
  let content = "def function_name():\n\t# Your Python code here";
  const editor = monaco.editor.create(
    document.getElementById("monaco-container"),
    {
      value: content,
      language: "python",
      theme: "vs-dark",
    }
  );

  editor.onDidChangeModelContent(() => {
    content = editor.getValue();
  });

  submitBtn.addEventListener("click", async () => {
    const send_data = {
      content: content,
    };

    try {
      const response = await fetch(`${config.API_URL}/functions`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(send_data),
      });

      const data = await response.json();
      console.log(data);
      //   clear the editor
      editor.setValue("def function_name():\n\t# Your Python code here");
    } catch (error) {
      console.error("Error:", error);
    }
  });
});
