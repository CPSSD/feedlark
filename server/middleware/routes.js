// All routing
// I've opted for a single file approach as this means that things
//  like express and the auth middleware aren't imported N times

const router = require("express").Router();

const userController = require("../controllers/users");
const feedController = require("../controllers/feeds");
const streamController = require("../controllers/streams");


// Checks if the client is authenticated
function isAuthed(req, res, next) {
  if (req.session.username) {
    res.locals.session = req.session;
    next();
  } else {
    res.status(403).end();
  }
}

// User pages

// Logout
router.all("/user/logout", userController.logout);

// Signup
router.get("/user/signup", (req, res) => { res.render("signup"); });

// Signup processing
router.post("/user/signup", userController.signup);

// Login processing
router.post("/user/login", userController.login);

// Login form
router.get("/user/login", (req, res) => {
  // Go to profile if user is already logged in
  if (typeof req.session.username != "undefined") return res.redirect(302, "/user");

  res.render("login");
});

// Profile
router.get("/user", isAuthed, userController.profile);

// Feeds pages

// Add
router.get("/feeds/add", isAuthed, (req, res) => { res.render("feeds_add"); });

// Add processing
router.post("/feeds/add", isAuthed, feedController.add);

// Remove processing
router.get("/feeds/remove", isAuthed, feedController.remove);

// List
router.get("/feeds", isAuthed, feedController.index);

// Stream & Landing page
router.get("/", (req, res, next) => {
  if (req.session.username) {
    res.locals.session = req.session;
    next();
  } else {
    res.render('index').end();
  }
}, streamController.index);

// Tokens (for API stuff!)
router.get("/token/add", isAuthed, userController.addToken);
router.get("/token/remove", isAuthed, userController.removeToken);
router.get("/token/list", isAuthed, userController.listTokens);

// Plaintext Endpoint
router.get("/plaintext", userController.validToken, streamController.plaintext);

// Repo updater
// Yes, the auth token is part of the URL
// It's just a really handy way to make sure it's github doing the job :P
router.get("/pull/d8db76806cd5a6f825200d5da204d3fc22d2b96d4832b3519ee2759b23ee7324", (req, res) => {
  var exec = require("child_process").exec;
  var cmd = "/bin/bash -c ../script/update.sh";
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
    	console.log(require("strftime")("%H:%M %d/%m/%y") + " ERROR: Repo update failed!\n" + stderr);
    	return res.status(500).send('{"status": "failure", "error": "' + stderr + '"}');
    }
    return res.status(200).send('{"status": "success"}');
    console.log(require("strftime")("%H:%M %d/%m/%y") + " INFO: Repo updated");
  });
});

module.exports = router;
