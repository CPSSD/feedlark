module.exports = function login(inputs) {
  inputs = inputs || {};

  var req = this.req;
  var res = this.res;

  require('bcrypt').hash(inputs.password, 8, function(err, hash) {
    if (err) return res.negotiate(err);
    User.attemptLogin({
      email: inputs.email,
      password: hash
    }, function (err, user) {
      if (err) return res.negotiate(err);
      if (!user) {
        if (req.wantsJSON || !inputs.invalidRedirect) {
          return res.badRequest('Invalid username/password combination.');
        }
        return res.redirect(inputs.invalidRedirect);
      }
      req.session.me = user.id;
      if (req.wantsJSON || !inputs.successRedirect) {
        return res.ok();
      }
      return res.redirect(inputs.successRedirect);
    });
  });
};
