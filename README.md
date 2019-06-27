# washinc

[![Build Status](https://travis-ci.org/krigar1184/washinc.svg?branch=master)](https://travis-ci.org/krigar1184/washinc)

`make test` to run the test suite.

`make up` to have the app up and running on port 5000.

The following entrypoints are available:
- [GET] /products -- get list of products
- [PUT] /products -- add new product
- [GET] /product/<id> -- see information on a product with specified id
- [PUT] /product/<id> -- update a product
- [DELETE] /product/<id> -- delete a product
- [PUT] /reservation/<product_id> -- reserve a product for a current user
- [DELETE] /reservation/<product_id> -- cancel a reservation
- [GET] /reservations/ -- get list of current user's reserved products
