# washinc

[![Build Status](https://travis-ci.org/krigar1184/washinc.svg?branch=master)](https://travis-ci.org/krigar1184/washinc)

`make test` to run the test suite.

`make up` to have the app up and running on port 5000.

The following entrypoints are available:
- [GET] /price/retail - get the current retail price
- [PUT] /price/retail - update the current retail price
- [GET] /reservations/get - get current reservations number
- [PUT] /reservation/create - make a reservation (increment the counter by 1)
- [DELETE] /reservations/cancel - cancel a reservation (decrement the counter by 1)
