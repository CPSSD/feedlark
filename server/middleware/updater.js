const fs = require("fs");
const exec = require("child_process").exec;

const cmd = "/bin/bash -c ../script/update.sh";
const token_file = "../script/update_token.key";
const ref = "refs/heads/master";

module.exports = {
  check: (req, res, next) => {

	// Set encoding type
	res.type("json");

    // Check the ref
    if (req.body.ref != ref) {
      return res.status(304).send('{"status": "not modified", "error": "Wrong ref."}');
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
        return;
      }

      console.log(require("strftime")("%H:%M %d/%m/%y") + " INFO: Repo updated");
    });

    // Return immediately. The script could take a while to run.
    return res.status(200).send('{"status": "success"}').end();
  }
};
