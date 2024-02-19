# Changelog

All notable changes to this project will be documented in this file.

## v1.0.3 - Unreleased

- Support other languages
- Restrict users' access to system level commands
- Add rate limit

## v1.0.2 - Unreleased

- Separate function uploading and executing channels
- Separate dependencies for each function
- Separate functions between users, allow same function name for different users

## v1.0.1 - 2024-02-18

### Added

- In-app package installation (through pip)
- Add Timeout and Memory Limit for each function
- Limit upload file size
- Add simple UI for the application

## v1.0.0 - 2024-02-07

### Added

- Allow user to CREATE invokee function in Python
- Users can EXECUTE the function
- Users can GET all functions, GET a function by its name
- Users can MODIFY existing functions and DELETE a function
- Functions are stored distributedly in the file system
- Added logging for each function
- Supported Docker & Docker Compose
