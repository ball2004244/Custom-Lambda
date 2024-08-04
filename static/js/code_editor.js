import config from "./config.js";

/*
 * #####
 *
 * This file Setup Monaco Editor and Code Submission
 *
 * #####
 */
const submitBtn = document.getElementById("submit-btn");

const default_code = `def hello():
\t'''
\tNote that, the submit function must be in this format:
\t
\t***
\tdef function_name(b, c, d):
\t\treturn e
\t***
\t
\tOtherwise, the code wont run as expected
\t'''
\treturn "Hello World!"
`;

// Configure require.js paths
require.config({
  paths: {
    vs: config.MONACO_EDITOR_URL,
  },
});

// Load Monaco Editor
require(["vs/editor/editor.main"], () => {
  let content = default_code;
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
        body: JSON.stringify({
          content: content,
          username: "test",
          password: "test",
        }),
      });

      const data = await response.json();
      console.log(data);
      //   clear the editor
      editor.setValue(default_code);
    } catch (error) {
      console.error("Error:", error);
    }
  });
});