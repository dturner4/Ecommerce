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
// MongoDB Playground script to create a "discounts" collection

use('Ecommerceplatform');

// Drop the 'discounts' collection if it exists, to recreate it fresh.
if (db.getCollectionNames().includes('discounts')) {
  db.getCollection('discounts').drop();
  print("Dropped existing 'discounts' collection. A new one will be created.");
}

// Iterate over each product in the 'products' collection.
db.getCollection('products').find({}).forEach(function(product) {
  // Create a discount document with the desired fields.
  var discountDocument = {
    product_id: product.product_id,
    product_name: product.product_name,
    actual_price: product.actual_price,
    discount_percentage: product.discount_percentage,
    discounted_price: product.discounted_price
  };
  
  // Insert the document into the 'discounts' collection.
  db.getCollection('discounts').insertOne(discountDocument);
  
  print("Inserted discount data for product: " + product.product_id);
});

// Optional: To verify the inserted documents, you can run:
// db.getCollection('discounts').find().toArray();
