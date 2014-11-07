Minimal flask app
=================

Simple db management without ORM or external modules.
All CRUD operations should be implemented.

To initialize the DB use `sqlite3 test.db < schema.sql`

   * simple-db - just initialize the db, provides some basic functions to deal
     with sqlite db and two endpoints to visualize and add entries
     
   * better-db - same as the other but uses a better html template, same page to
     display and add entry, endpoint to update and delete entries, some
     javascript logic on the frontend.
     It also uses a separate functions to insert/update/delete values from db,
     decoupling this logic from views.

TODO
----
