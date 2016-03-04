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
router.get("/user", isAuthed, (req, res) => { res.render("profile"); });

// Feeds pages

// Add
router.get("/feeds/add", isAuthed, (req, res) => { res.render("feeds_add"); });

// Add processing
router.post("/feeds/add", isAuthed, feedController.add);

// Remove processing
router.get("/feeds/remove", isAuthed, feedController.remove);

// List
router.get("/feeds", isAuthed, feedController.index);

// Stream
router.get("/stream", isAuthed, streamController.index);

// Home/Index
router.get("/", (req, res) => {
  res.render('index');
});

module.exports = router;
