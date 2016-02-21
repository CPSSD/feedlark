/**
 * UserController
 *
 * @description :: Server-side logic for managing users.
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */
var bcrypt = require("bcrypt-nodejs");

function redirect(req, res, url) {
	if (req.wantsJSON) return res.ok("Success");
	return res.redirect(url);
}

module.exports = {

	/**
	 * `UserController.login()`
	 */
	login: function (req, res) {
		// Logged in already?
		if (typeof req.session.username != "undefined") return redirect(req, res, "/user/profile");
		// Not logged in, and not trying to...
		if (req.method != "POST") return res.ok({}, "login");

		// Import things & load request vars
		var email = req.param("email");
		var password = req.param("password");
		if (!_.isString(email) || !_.isString(password)) return res.badRequest({err: "Invalid email/password combination."}, "signup");

		// Find the user with this email address
		// Using "Dynamic Finders"
		User.findByEmail(email).exec(function (err, user) {

			// Is the user name valid? (DB query returns nothing if not)
			user = user[0];
			if (typeof user == "undefined") return res.badRequest({err: "Invalid email/password combination."}, "login");

			// Check their password
			bcrypt.compare(password, user.password, function(err, valid) {
				if (!valid) return res.badRequest({err: "Invalid email/password combination."}, "login");

				// Set session vars and redirect
				req.session.username = user.username;
				req.session.subscribed_feeds = user.subscribed_feeds;
				req.session.msg = "Successfully logged in.";
				return redirect(req, res, "/user/profile");
			});
		});
	},

	/**
	 * `UserController.logout()`
	 */
	logout: function (req, res) {
		req.session.destroy(function(err) {
			// There is accordingly a bug with destroying sessions where if you redirect there is a chance it won't destroy fully
			// As a result, we need a "logout" view
			res.ok({}, "logout");
		});
	},

	/**
	 * `UserController.signup()`
	 */
	signup: function (req, res) {
		// Not logged in, and not trying to...
		if (req.method != "POST") return res.view("signup");

		// Import things & load request vars
		var email = req.param("email");
		var password = req.param("password");
		var username = req.param("username");

		// Verify these details
		if (!_.isString(email) || !_.isString(password) || !_.isString(username)) return res.badRequest({err: "Invalid input data"}, "signup");
		if (email.length < 5) return res.badRequest({err: "Email Address too short."}, "signup");
		if (password.length < 8) return res.badRequest({err: "Password too short."}, "signup");
		if (username.length < 4) return res.badRequest({err: "Username too short."}, "signup");

		// Generate the password hash
		bcrypt.hash(password, null, null, function(err, hash) {
			if (err) return res.serverError({err: err}, "signup");

			// Add new user to the database
			User.create({
				username: username,
				email: email,
				subscribed_feeds: [],
				password: hash
			})

			// Do stuff with the new data
			.exec(function (err, user) {

				// Catch errors
				if (err) return res.badRequest({err: err}, "signup");

				G2g.create({
					username: username,
					feeds: []
				}).exec(function (err, data) {

					// Catch errors
					if (err) return res.badRequest({err: err}, "signup");

					// Log the user in
					req.session.username = username;
					req.session.subscribed_feeds = [];
					req.session.msg = "Signup successful. Welcome!";
					return redirect(req, res, "/user/profile");
				});
			});
		});
	},

	/**
	 * `UserController.profile()`
	 */
	profile: function(req, res) {
		return res.ok({}, "profile");
	}

};
