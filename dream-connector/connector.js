const { spawn } = require("child_process");

exports.readJson = (req, res) => {
  //do something
  console.log(req.body);
  var largeDataSet = [];
  // spawn new child process to call the python script
  const python = spawn("python", ["main.py"]);
  // collect data from script
  python.stdout.on("data", function (data) {
    console.log("Pipe data from python script ...");
    largeDataSet.push(data);
  });
  // in close event we are sure that stream is from child process is closed
  python.on("close", (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send(largeDataSet.join(""));
  });
};
