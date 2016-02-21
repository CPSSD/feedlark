/**
 * G2g.js
 *
 * @description :: Basic model for referencing the Good-to-Go aggregated feeds
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

module.exports = {
	tableName: 'g2g',

	username: {
		type: 'alphanumericdashed',
		required: true,
		unique: true,
		minLength: 4,
		maxLength: 254
	},
	feeds: {
		type: 'array',
		defaultsTo: []
	}
};

