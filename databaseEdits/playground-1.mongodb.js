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

// Select the database to use.
use('Ecommerceplatform');

//db.getCollection('reviews').deleteMany({})
db.getCollection('products').find({}).forEach(function(product) {
  // Check if the product has the required review fields
  if (product.review_id && product.user_id && product.user_name && product.review_title && product.review_content) {
    // Split the comma-separated values into arrays.
    var reviewIDs      = product.review_id.split(",");
    var userIDs        = product.user_id.split(",");
    var userNames      = product.user_name.split(",");
    var reviewTitles   = product.review_title.split(",");
    var reviewContents = product.review_content.split(",");

    // Loop through each set of review data to create a new review document.
    for (var i = 0; i < reviewIDs.length; i++) {
      var reviewDocument = {
        review_id: reviewIDs[i].trim(),
        user_id: userIDs[i].trim(),
        user_name: userNames[i].trim(),
        review_title: reviewTitles[i].trim(),
        review_content: reviewContents[i].trim(),
        product_link: product.product_link,  // Reference product link from the product document.
        img_link: product.img_link,          // Reference image link if needed.
        product_id: product.product_id       // Optionally include the product_id for easier linking.
      };

      // Insert this review document into the "reviews" collection.
      db.getCollection('reviews').insertOne(reviewDocument);
    }

    // Update the product document to include an array of cleaned review IDs.
    var cleanedReviewIDs = reviewIDs.map(function(id) { return id.trim(); });
    db.getCollection('products').updateOne(
      { _id: product._id },
      { $set: { review_ids: cleanedReviewIDs } }
    );

    print("Processed product with product_id: " + product.product_id + " (" + reviewIDs.length + " reviews inserted)");
  } else {
    print("Skipping product " + product.product_id + " (missing review data)");
  }
});