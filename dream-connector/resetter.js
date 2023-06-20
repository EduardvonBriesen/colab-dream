const { spawn } = require("child_process");

exports.reset = (req, res) => {
  //do something
  console.log("Reset request received");
  console.log(req.body);
  var largeDataSet = [];

  // spawn new child process to call the python script
  const python = spawn("python", ["/home/ubuntu/colab-dream/dream-braider/helper/reset.py"]);

  // collect data from script
  python.stdout.on('data', (data) => {
    console.log("Pipe data from python script ...");
    largeDataSet.push(data);
  });
  
  // Listen for data on the standard error stream
  python.stderr.on('data', (data) => {
    console.error("Pipe data from python script ...");
    console.error(`stderr: ${data}`);
  });
  
  // in close event we are sure that stream is from child process is closed
  python.on("close", (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send(largeDataSet.join(""));
  });
};
