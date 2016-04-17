const fs = require("fs");
const spawn = require("child_process").spawn;

const cmd = "../script/update.sh";
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
    console.log(require("strftime")("%H:%M %d/%m/%y") + " INFO: Repo update started");

    spawn(cmd, [], {
      shell: true,
      detached: true,
      stdio: ["ignore"]
    });

    // Return immediately. The script could take a while to run.
    return res.status(200).send('{"status": "success"}').end();
  }
};
