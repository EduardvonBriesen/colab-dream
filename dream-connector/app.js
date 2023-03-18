const express = require("express");

const app = express();
const { readJson } = require("./connector");
const { reset } = require("./resetter");

//START THE SERVER
const port = 8000 || process.env.PORT;

app.use(express.json());
app.post("/prompt", readJson);
app.post("/reset", reset);

app.listen(port, () => {
  console.log(`node server up and running on port ${port}..`);
});
