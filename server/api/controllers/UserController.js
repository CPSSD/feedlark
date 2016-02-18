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
   */
  logout: function (req, res) {
    req.session.me = null;
		if (req.wantsJSON) {
      return res.ok('Logged out! See you next time :)');
    }
		return res.redirect('/');
  },


  /**
   * `UserController.singup()`
   */
  singup: function (req, res) {
		User.signup({
      name: req.param('username'),
      email: req.param('email'),
      password: req.param('password')
    }, function (err, user) {
      if (err) return res.negotiate(err);

      req.session.me = user.id;
      if (req.wantsJSON) {
        return res.ok('Signup successful! Horray!');
      }
      return res.redirect('/welcome');
    });
  }
};
