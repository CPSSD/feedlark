/*
# Auth.js

Some authorization helper functions
*/

module.exports = {
  isAuthed: (req, res, next) => {
    if (req.session.username) {
      res.locals.session = req.session;
      next();
    } else {
      res.status(403).end();
    }
  },

  authorise: (req, res, user, next) => {
    req.session.username = user;
    next();
  },

  deauthorize: (req, res, next) => {
    req.session.destroy();
    next();
  }
};
