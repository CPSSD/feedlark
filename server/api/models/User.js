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
    password: {
      type: 'string'
    },
    subscribed_feeds: {
      type: 'array'
    },

    toJSON: function() {
      var obj = this.toObject();
      delete obj.password;
      delete obj.entry_password;
      delete obj._csrf;
      return obj;
    },

    beforeCreate: function(values, next) {
      require('bcrypt').hash(values.entry_password, 8, function(err, hash) {
          if (err) {
            console.log(err);
            next(err);
          }
          values.password = hash;
          next(values);
      });
    },

    attemptLogin: function (inputs, cb) {
      // note that the login response will encrypt the password
      User.findOne({
        email: inputs.email,
        password: inputs.password
      })
      .exec(cb);
    }

  }

};
