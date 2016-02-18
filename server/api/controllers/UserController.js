/**
 * UserController
 *
 * @description :: Server-side logic for managing users
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {

  /**
   * `UserController.login()`
   */
  login: function (req, res) {
		return res.login({
			username: req.param('username'),
      email: req.param('email'),
      password: req.param('password'),
      successRedirect: '/',
      invalidRedirect: '/login'
    });
  },


  /**
   * `UserController.logout()`
   *
   * @description :: Logout, don't bother checking if they're logged in
   */
  logout: function (req, res) {
    req.session.me = null;
		if (req.wantsJSON) {
      return res.ok('Logged out! See you next time :)');
    }
		return res.redirect('/');
  },


  /**
   * `UserController.signup()`
   */
  signup: function (req, res) {
    User.create({
      username: req.param('username'),
      email: req.param('email')
    })
    .then(function (user) {
      req.session.me = user.id;
      if (req.wantsJSON) {
        return res.ok('Signup successful! Horray!');
      }
      return res.redirect('/welcome');
    })
    .catch(function (err) {
      console.log(err);
      res.negotiate(err);
    });
  }
};
