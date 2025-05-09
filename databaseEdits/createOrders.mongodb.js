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
// MongoDB Playground script to create an "orders" collection with synthetic data

/* global use, db */
// MongoDB Playground script to create an "orders" collection with synthetic data

use('Ecommerceplatform');

// Helper function: Parse a price string by removing non-numeric characters (except the decimal point)
function parsePrice(priceStr) {
  return parseFloat(priceStr.replace(/[^0-9.]/g, ""));
}

// Drop the 'orders' collection if it exists, to start fresh.
if (db.getCollectionNames().includes('orders')) {
  db.getCollection('orders').drop();
  print("Dropped existing 'orders' collection. A new one will be created.");
}

// Get all products from the 'products' collection once into an array.
// This array will be used to select a random product for each order.
var sampleProducts = db.getCollection('products').find({}).toArray();
if (sampleProducts.length === 0) {
  print("No products found in the 'products' collection.");
}

// Get all users from the 'users' collection.
var users = db.getCollection('users').find({}).toArray();
if (users.length === 0) {
  print("No users found in the 'users' collection.");
}

// Iterate over each user to create an order.
users.forEach(function(user) {
  // Select a random product from the products array.
  var randomIndex = Math.floor(Math.random() * sampleProducts.length);
  var product = sampleProducts[randomIndex];

  // Generate a synthetic order_id.
  var order_id = "ORD" + Math.floor(Math.random() * 100000);

  // Generate a random quantity between 1 and 5.
  var quantity = Math.floor(Math.random() * 5) + 1;

  // Parse the product's actual price from its string value.
  var actualPrice = parsePrice(product.actual_price);

  // Calculate the total cost as quantity multiplied by the actual price.
  var total_cost = parseFloat((quantity * actualPrice).toFixed(2));

  // Randomly decide on a delivery status: "Delivered" or "Out for delivery".
  var delivery_status = (Math.random() < 0.5) ? "Delivered" : "Out for delivery";

  // Set the delivery date.
  var today = new Date();
  var delivery_date;
  if (delivery_status === "Delivered") {
    // For delivered orders, choose a past date (between 7 and 30 days ago).
    var daysAgo = Math.floor(Math.random() * 23) + 7;
    delivery_date = new Date(today.getTime() - daysAgo * 24 * 60 * 60 * 1000);
  } else {
    // For orders out for delivery, choose a future date (within the next 7 days).
    var daysAhead = Math.floor(Math.random() * 7);
    delivery_date = new Date(today.getTime() + daysAhead * 24 * 60 * 60 * 1000);
  }

  // Create the order document.
  var orderDocument = {
    user_id: user.user_id,
    order_id: order_id,
    product_id: product.product_id,
    product_ordered: product.product_name,
    quantity: quantity,
    total_cost: total_cost,
    delivery_status: delivery_status,
    delivery_date: delivery_date
  };

  // Insert the order document into the "orders" collection.
  db.getCollection('orders').insertOne(orderDocument);
  print("Inserted order for user: " + user.user_id + " with product: " + product.product_id);
});

print("Order creation complete. Check the 'orders' collection for the generated entries.");
