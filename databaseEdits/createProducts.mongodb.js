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

/* global use, db */
// MongoDB Playground script to clean up the 'products' collection by removing extraneous fields

use('Ecommerceplatform');

// Define an object with the fields to remove (set to an empty string with $unset).
var fieldsToRemove = {
  review_id: "",
  user_id: "",
  user_name: "",
  review_title: "",
  review_content: "",
  review_ids: ""
};

// Update all documents in the 'products' collection by unsetting the specified fields.
db.getCollection('products').updateMany(
  {},
  { $unset: fieldsToRemove }
);

print("Extraneous review fields have been removed from the 'products' collection.");

