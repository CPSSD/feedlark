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
      type: 'url',
      required: true,
      unique: true,
      minLength: 8,
      maxLength: 25564
    },
    items: {
      type: 'array',
      defaultsTo: []
    }

  }
};

