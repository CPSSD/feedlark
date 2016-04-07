const fs = require("fs");
const exec = require("child_process").exec;

const cmd = "/bin/bash -c ../script/update.sh";
const token_file = "../script/update_token.key";
const ref = "refs/heads/master";

module.exports = {
  check: (req, res, next) => {

    // Check the ref
    if (req.query.ref != ref) {
      return res.status(400).send('{"status": "bad request", "error": "Wrong ref."}');
    }

    // Load the token
    if (fs.exists(token_file)) {
      fs.readFile(token_file, (err, token) => {
        if (err) return res.status(500).send('{"status": "failure", "error": "' + err + '"}');

        // Check the token
        if (req.params.token != token) {
          return res.status(403).send('{"status": "access denied", "error": "Incorrect token."}');
        }

        next();
      });

    // Set the token (first request)
    } else {
      fs.writeFile(token_file, req.params.token, err => {
        if (err) return res.status(500).send('{"status": "failure", "error": "' + err + '"}');

        next();
      });
    }
  },

  // Run the script
  run: (req, res) => {    
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.log(require("strftime")("%H:%M %d/%m/%y") + " ERROR: Repo update failed!\n" + stderr);
        return res.status(500).send('{"status": "failure", "error": "' + stderr + '"}');
      }

      console.log(require("strftime")("%H:%M %d/%m/%y") + " INFO: Repo updated");
      return res.status(200).send('{"status": "success"}');
    });
  }
};
