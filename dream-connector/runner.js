const { spawn } = require('child_process');
const { promptStack } = require("./stack");

var running = false;

function runNextScript() {
  if (promptStack.length > 0 && !running) {
    console.log('----- Generate new dream section -----');
    console.log('Prompts in stack: ', promptStack.length);

    running = true;

    prompt = ""

    // Check if stack only contains one prompt
    if (promptStack.length == 1) { prompt = Object.values(promptStack[0]); }
    else { prompt = Object.values(promptStack.shift()); }

    console.log('Current prompt: ', prompt);

    // spawn new child process to call the python script; 'local' for use with webui
    const pythonProcess = spawn('python', ['/workspace/colab-dream/dream-braider/generator.py', "local", prompt]);
    console.log('Dream-Braider running: ', running);

    // Listen for data on the standard output stream
    pythonProcess.stdout.on('data', (data) => {
       console.debug(`stdout: ${data}`)
    });
    
    // Listen for data on the standard error stream
    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      console.log(`Python script finished with code ${code}`);
      running = false;
      console.log('Dream-Braider running: ', running);
      runNextScript();
    });
  }
  if (!running) setTimeout(runNextScript, 3000);
  // else setTimeout(runNextScript, 10000);
}

module.exports = {
    runNextScript
  };