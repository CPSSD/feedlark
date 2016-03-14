const app = require("../../app");
const assert = require('assert');
const request = require('supertest');
const lodash = require('lodash');

describe('StreamController', _ => {
  var agent = request.agent(app);

  var user_details_base = {
    username: "rmss",
    email: "rms@gnu.org",
    password: "gnuisnotlinux"
  }

  describe('#index()', _ => {
    it("Stream is unavailable to users logged out", done => {
      agent
        .get('/stream')
        .expect(403, done);
    });
    it('User can login', done => {
      agent
        .post('/user/login')
        .type('form')
        .send(user_details_base)
        .expect(302, done);
    });
    it("Stream is available to users", done => {
      agent
        .get('/stream')
        .expect(200, done);
    });
  });

  describe('#plaintext()', _ => {
    var api_key = null;
    it("Able to generate api token", done => {
      agent
        .get('/token/add')
        .expect(302, done);
    });

    it("Able to fetch api token", done => {
      agent
        .get('/token/list')
        .expect(200)
        .end( (err, res) => {
          if (err) throw err;
          api_key = Object.keys(res.body)[0];
          if ( lodash.isString(api_key) ) {
            done();
          }
          else {
            done("Key doesn't exist");
          }
        });
    });

    it("Able to get plaintext", done => {
      agent
        .get('/plaintext?username=' + user_details_base.username + "&token=" + api_key)
        .expect(200, done);
    });
  });
});
