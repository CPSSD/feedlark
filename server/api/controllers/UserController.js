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
		// Not logged in, and not trying to...
		if (req.method != "POST") return res.view("login");
		// Logged in
		if (typeof req.session.username != "undefined") return redirect(req, res, "/user/profile");

		// Import things & load request vars
		var email = req.param("email");
		var password = req.param("password");

		// Find the user with this email address
		// Using "Dynamic Finders"
		// TODO: Make sure the email address is safe for use here
		User.findByEmail(email).exec(function (err, user) {
			user = user[0];

			// Catch actual db errors
			// res.negotiate does all the wantsJSON and view selecting itself
			// If a view is provided, "data" (the error) is passed onto it
			if (err) return res.serverError({err: err}, "login");

			// Is the user name valid? (DB query returns nothing if not)
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
				if (err) return res.badRequest({err: "Oops, look like that email or username is already taken."}, "signup");

				// Log the user in
				req.session.username = username;
				req.session.subscribed_feeds = [];
				req.session.msg = "Signup successful. Welcome!";
				return redirect(req, res, "/user/profile");
			});
		});
	},

	/**
	 * `UserController.profile()`
	 */
	profile: function(req, res) {
		// Get the user data
		// TODO: Make sure the email address is safe for use here
		User.findByUsername(req.session.username).exec(function (err, user) {
			if (err) return res.serverError({err: err}, "login");

			user = user[0];
			if (typeof user == "undefined") return res.redirect("/user/login");

			// Load values needed for page display
			return res.ok({}, "profile");
		});
	}

};
