/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

use('Ecommerceplatform');

// Drop the 'users' collection if it exists to start fresh.
if (db.getCollectionNames().includes('users')) {
  db.getCollection('users').drop();
  print("Dropped existing 'users' collection. A new one will be created.");
}

// Iterate over each product document to extract user data.
db.getCollection('products').find({}).forEach(function(product) {
  // Check if product has both user_id and user_name fields.
  if (product.user_id && product.user_name) {
    // Split the comma-separated user_ids and user_names into arrays.
    var userIDs = product.user_id.split(",");
    var userNames = product.user_name.split(",");

    // Loop through each user entry.
    for (var i = 0; i < userIDs.length; i++) {
      var trimmedUserID = userIDs[i].trim();
      var trimmedUserName = userNames[i].trim();

      // Upsert the user into the 'users' collection to ensure uniqueness.
      db.getCollection('users').updateOne(
        { user_id: trimmedUserID },
        { $set: { user_id: trimmedUserID, user_name: trimmedUserName } },
        { upsert: true }
      );
    }
  }
});

print("User table creation complete. The 'users' collection now contains unique user entries.");