conn = new Mongo("localhost:9001");
db = conn.getDB("feedlark");

db.createUser(
  {
    user: "masterlark",
    pwd: "huehuehuehuehuehuehuehue",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
);
