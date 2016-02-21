/**
 * G2gController
 *
 * @description :: Displays feeds from the G2G Database
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {
	index: function (req, res) {

		// Get the values from the database
		G2g.findOne({username: req.session.username}).exec(function (err, data) {
			if (err || typeof data == "undefined") return res.serverError({err: "Something went wrong finding your feeds"});

			// That's about it...display the page
			return res.ok({feeds: data.feeds}, "g2g_index");
		});
	}
};

