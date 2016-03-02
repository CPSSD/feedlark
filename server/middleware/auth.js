/*
# Auth.js

Some authorization helper functions
*/

module.exports = {
  isAuthed: (req, res, next) => {
    if (req.session.username) {
      next(req, res);
    } else {
      res.status(403).end();
    }
  },

  authorise: (req, res, user, next) => {
    req.session.username = user;
    next(req, res);
  },

  deauthorize: (req, res, next) => {
    req.session.destroy();
    next(req, res);
  }
}
