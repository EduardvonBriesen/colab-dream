const express = require("express");

const app = express();
const { readJson } = require("./connector");

//START THE SERVER
const port = 8000 || process.env.PORT;

app.use(express.json());
app.post("/prompt", readJson);

app.listen(port, () => {
  console.log(`node server up and running on port ${port}..`);
});
