/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {

    username: {
      type: 'string',
      required: true
    },
    email: {
      type: 'string',
      required: true,
      unique: true
    },
    hashed_password: {
      type: 'string'
    },
    password_salt: {
      type: 'string'
    },
    subscribed_feeds: {
      type: 'array'
    },

    signup: function (inputs, cb) {
      // Create a user
      User.create({
        name: inputs.name,
        email: inputs.email,
        // TODO: But encrypt the password first
        password: inputs.password
      })
        .exec(cb);
    },
    attemptLogin: function (inputs, cb) {
      // Create a user
      User.findOne({
        email: inputs.email,
        // TODO: But encrypt the password first
        password: inputs.password
      })
      .exec(cb);
    }

  }
};
