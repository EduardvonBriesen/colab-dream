const { spawn } = require("child_process");

exports.readJson = (req, res) => {
  //do something
  console.log("Dream request received");
  console.log(req.body);
  var largeDataSet = [];

  // spawn new child process to call the python script
  const python = spawn("python", ["/workspace/colab-dream/dream-braider/generator.py", "local", Object.values(req.body)]);

  // collect data from script
  python.stdout.on('data', (data) => {
    console.log("Pipe data from python script ...");
    largeDataSet.push(data);
  });
  
  // Listen for data on the standard error stream
  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
  
  // in close event we are sure that stream is from child process is closed
  python.on("close", (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send(largeDataSet.join(""));
  });
};
