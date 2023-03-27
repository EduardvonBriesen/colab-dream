const express = require("express");

const app = express();
const { readJson } = require("./connector");
const { reset } = require("./resetter");
const { promptStack } = require("./stack");
const { runNextScript } = require('./runner');

//START THE SERVER
const port = 8000 || process.env.PORT;

app.use(express.json());
// app.post("/prompt", readJson);

// Add prompt to stack
app.post("/prompt", (req, res) => {
  console.log("----- Dream request received -----");

  promptStack.push(req.body);

  console.log('Prompts in stack: ', promptStack.length);
  console.log('Prompts: ',promptStack);

  res.sendStatus(200);
});

// Reset everything
app.post("/reset", reset);

// Initialize caller function
runNextScript();

app.listen(port, () => {
  console.log(`node server up and running on port ${port}..`);
});
