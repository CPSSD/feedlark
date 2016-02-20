/**
 * FeedController
 *
 * @description :: Server-side logic for managing Feeds
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

function redirect(req, res, url) {
	if (req.wantsJSON) return res.ok("Success");
	return res.redirect(url);
}

module.exports = {

	/**
	 * `FeedController.add()`
	 */
	add: function (req, res) {
		// User want's the input form?
		if (req.method != "POST") return res.ok({}, "feed_add");

		var url = req.param("url").toLowerCase();

		// TODO: Check if we need to manually check for duplicates
		Feed.create({
			url: url,
			items: []
		}).exec(function (err, feed) {
			if (err) return res.serverError({err: "Failed to add feed to database"});

			// Add URL to user's subscribed feeds
			User.findByUsername(req.session.username).exec(function (err, user) {
				user = user[0];
				if (err || typeof user == "undefined") return res.serverError({err: "Something went wrong finding your user"});

				// Append the URL to their subscribed urls
				if (user.subscribed_feeds.indexOf(url) == -1) user.subscribed_feeds.push(url);

				user.save(function (err, ret_user) {
					if (err) return res.serverError({err: "Failed to add feed to your user"});

					// Return to feed manager page
					req.session.msg = "Successfully added feed!";
					req.session.subscribed_feeds = user.subscribed_feeds;
					return redirect(req, res, "/feed/manage");
				});
			});
		});
	},

	/**
	 * `FeedController.remove()`
	 */
	remove: function (req, res) {
		// User want's the input form?
		if (req.method != "GET") return res.badRequest({err: "Invalid request type"});

		var url = req.param("url").toLowerCase();

		// Remove URL from user's subscribed feeds
		// TODO: Remove feed from feed db if this was the last user using it?
		User.findByUsername(req.session.username).exec(function (err, user) {
			user = user[0];
			if (err || typeof user == "undefined") return res.serverError({err: "Something went wrong finding your user"});

			var index = user.subscribed_feeds.indexOf(url)
			if (index > -1) user.subscribed_feeds.splice(index, 1);

			user.save(function (err, ret_user) {
				if (err) return res.serverError({err: "Failed to remove feed from your user"});

				// Return to feed manager page
				req.session.msg = "Successfully removed feed!";
				req.session.subscribed_feeds = user.subscribed_feeds;
				return redirect(req, res, "/feed/manage");
			});
		});
	},

	/**
	 * `FeedController.manage()`
	 */
	manage: function (req, res) {
		// Get all the feeds for the current user
		User.findByUsername(req.session.username).exec(function (err, user) {
			user = user[0];
			if (err || typeof user == "undefined") return res.serverError({err: "Something went wrong finding your user"});

			// Go to feed manager page
			return res.ok({}, "feed_manage");
		});
	}
};
