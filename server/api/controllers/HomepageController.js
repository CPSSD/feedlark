/**
 * HomepageController
 *
 * @description :: Server-side logic for managing homepages
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {

	/**
	 * `HomepageController.homepage()`
	 */
	homepage: function(req, res) {
		if (!req.session.authenticated) return res.ok({}, "homepage");
		// Check if a user is logged in, return username if possible
		User.findByEmail(req.session.authenticated).exec(function (err, user) {
			if (err) return res.negotiate(err);

			// Load values needed for page display
			return res.ok({username: user[0].username}, "homepage");
		});
	}
};

