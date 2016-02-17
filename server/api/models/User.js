/**
 * User.js
 *
 * @description :: Here is the fundementially important user model. It describes
 *                 what the server thinks a user is.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {
  attributes: {
    username: {
      type: 'string'
    },
    email: {
      type: 'string',
      unique: true
    },
    hashed_password: {
      type: 'string'
    },
    password_salt: {
      type: 'string'
    },
    subscribed_feeds: {
      collection: 'array'
    }
  }
};
