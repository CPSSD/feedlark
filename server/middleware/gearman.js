/**
 * gearman.js
 *
 * @description :: Server-side logic for managing Feeds
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

const gearman = require("gearman");
const client = new gearman.Gearman("localhost", 4730 , {timeout: 3000});
const bson = require("bson");
const BSON = new bson.BSONPure.BSON();

// TODO: remove timeout messages when client isn't connected
client.on('timeout', () => {
  console.log("gearman client timed out");
  client.close();
});

client.on('WORK_COMPLETE', (job) => {
    console.log('job completed, result:', job.payload.toString());
    client.close();
});

module.exports = {
  startJob: (job_name, job_data, job_options, next) => {
    /*
      Start a Gearman Job.

      job_data is expected to be standard javascript objects, which will be
      serialized to bson.
    */
    if (!job_options) {
      job_options = {
        background: true,
        encoding: "utf-8"
      };
    }
    client.connect( () => {
      if ('SECRETKEY' in process.env) {
        job_data.key = process.env.SECRETKEY;
      }
      var bson_data = BSON.serialize(job_data, false, true, false);
      client.submitJob( job_name, data=bson_data , options=job_options);
      next();
      client.close();
    });
  }
};
