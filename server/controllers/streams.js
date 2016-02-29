/**
 * streams
 *
 * @description :: Displays feeds from the G2G Database
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

import router from "express";
import getFeeds from "../models/stream";
import isAuthed from "../middleware/auth";

// Stream page
router.get("/", (req, res) => {
  getFeeds(req.session.username, (feeds) => res.render("stream_index", {feeds: feeds}));
});
