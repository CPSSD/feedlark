/**
 * User.js
 *
 * @description :: Generic model for all users on the site
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/user.md
 */

function encrypt(vals, cb) {
      var bcrypt = require("bcrypt-nodejs");

      bcrypt.hash(vals.password, null, null, function(err, res) {
        // Passing an arg/error to cb is the proper way. I'm not sure what it does though
        if (err) return cb(err);

        vals.password = password;
        cb();
      });
}

module.exports = {
  tableName: 'user',

  attributes: {

    username: {
      type: 'alphanumericdashed',
      required: true,
      unique: true,
      minLength: 4,
      maxLength: 254
    },
    email: {
      type: 'email',
      required: true,
      unique: true,
      minLength: 5,
      maxLength: 254
    },
    password: {
      type: 'string',
      required: true,
      minLength: 8,
      maxLength: 254
    },
    subscribed_feeds: {
      type: 'array',
      defaultsTo: []
    },

    // Lifecycle Callbacks
    // Encrypts the password when necessary
    beforeCreate: encrypt,
    beforeUpdate: encrypt
  }

};

