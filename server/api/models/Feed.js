/**
 * Feed.js
 *
 * @description :: Generic model for all feeds on the site
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/rss.md
 */

module.exports = {
  tableName: 'feed',

  attributes: {

    url: {
      type: 'string',
      required: true,
      unique: true
    },
    items: {
      type: 'array',
      defaultsTo: []
    }

  }
};

