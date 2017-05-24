# About
The aim of this project is to develop an encrypted chat messaging and file sharing system.

Currently under construction.

# Building Instructions
To install dependencies and run tests the following instructions should be followed

## Installing Dependencies

```
make deps
```

## Running Tests

```
make test
```

# Project Structure
All tests should go in the `tests` directory. The first part of a `test` file should start with `test_*` where start is the rest of the file. This allows `py.test` to detect where tests are supposed to run.

The files of the project have the following functions

* `crypto.py` - all cryptographic utilities should go in this file
* `server.py` - all code related to running the central chat server should go in this file
* `client.py` - all code related to running the central client server should go in this file
