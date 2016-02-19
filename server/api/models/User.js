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
  tableName: 'users',

  attributes: {

    username: {
      type: 'string',
      required: true,
      unique: true
    },
    email: {
      type: 'string',
      required: true,
      unique: true
    },
    password: {
      type: 'string',
      required: true
    },
    subscribed_feeds: {
      type: 'array',
      defaultsTo: []
    },

    toJSON: function() {
      var obj = this.toObject();
      delete obj.password;
      delete obj.entry_password;
      delete obj._csrf;
      return obj;
    },

    // Lifecycle Callbacks
    // Encrypts the password when necessary
    beforeCreate: encrypt,
    beforeUpdate: encrypt
  }

};

