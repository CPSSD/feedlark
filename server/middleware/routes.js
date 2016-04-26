// All routing
// I've opted for a single file approach as this means that things
//  like express and the auth middleware aren't imported N times

const router = require("express").Router();

const userController = require("../controllers/users");
const feedController = require("../controllers/feeds");
const streamController = require("../controllers/streams");
const bookmarkController = require("../controllers/bookmarks");
const updater = require("./updater");

// Checks if the client is authenticated
function isAuthed(req, res, next) {
  if (req.session.username) {
    if (process.env.ENVIRONMENT == "PRODUCTION" && typeof req.session.verified != "boolean") {
      res.redirect(302, "/user/verify");
    } else {
      res.locals.session = req.session;
      next();
    }
  } else {
    res.redirect(302, "/forbidden");
  }
}

// User pages

// Logout
router.all("/user/logout", userController.logout);

// Signup
router.all("/user/signup", userController.signup);

// Login processing
router.post("/user/login", userController.login);

// Login form
router.get("/user/login", (req, res) => {
  // Go to profile if user is already logged in
  if (typeof req.session.username != "undefined") return res.redirect(302, "/user");

  res.render("login");
});

// Verification action
router.get("/user/verify/:token", userController.verify);

// Verification asker
router.get("/user/verify", (req, res) => {
  res.locals.session = req.session;
  res.render("verify_ask");
});

// Profile
router.get("/user", isAuthed, userController.profile);

// Summary sender
router.get("/user/summaries/:token", userController.sendSummaries);

// Profile tokens
router.get("/user/tokens", isAuthed, userController.profileTokens);

// Profile settings
router.post("/user/change/password", isAuthed, userController.changePassword);

// Profile settings
router.post("/user/change/email", isAuthed, userController.changeEmail);

// Profile settings
router.post("/user/change/summaryinterval", isAuthed, userController.changeSummaryInterval);

// Show interest
router.post("/feeds/like", isAuthed, feedController.like);

// Show disinterest buttons
router.post("/feeds/dislike", isAuthed, feedController.dislike);

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
    if (process.env.ENVIRONMENT == "PRODUCTION" && typeof req.session.verified != "boolean") {
      res.redirect(302, "/user/verify");
    } else {
      res.locals.session = req.session;
      next();
    }
  } else {
    res.status(200).render('index');
  }
}, streamController.index);

// Display Bookmarks
router.get("/bookmarks", isAuthed, bookmarkController.bookmarks);

// Add Bookmark
router.post("/bookmarks/add", isAuthed, bookmarkController.add);

// Delete Bookmark
router.post("/bookmarks/remove", isAuthed, bookmarkController.remove);

// Tokens (for API stuff!)
router.get("/token/add", isAuthed, userController.addToken);
router.get("/token/remove", isAuthed, userController.removeToken);
router.get("/token/list", isAuthed, userController.listTokens);

// Plaintext Endpoint
router.get("/plaintext", userController.validToken, streamController.plaintext);

// Repo updater
router.post("/pull/:token", updater.check, updater.run);

// Routes for ToS and Privacy Policy
router.get("/terms", (req, res) => {
  return res.status(200).render("terms_of_service");
});
router.get("/privacy", (req, res) => {
  return res.status(200).render("privacy_policy");
});

// 403 page
router.get("/forbidden", (req, res) => {
  res.locals.session = req.session;
  res.render("403");
});

module.exports = router;
