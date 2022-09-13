# Christian Memes API Backend

## Description

This is the backend code for the Christian Meme website I am working on. Eventually I would like to have a site similar to this: https://giphy.com/explore/happy, where memes about Christianity can be posted and searched through via titles or tags, and there is a default page where all memes are available. I work as a pastor and while there are some great memes about Christianity and/or making fun of it, finding a location where they are all housed AND filed in a way that makes it easy to find something on a particular topic is not. I would like for this site to be that, and this backend is the first step to that.

## Future Work

I plan to expand this project in the following ways in the future:
- Create a Front End
- Implement Search features
- Implement User functionality so that a user can post, patch, and delete their own memes

## Getting Started

### Installing Dependencies

#### Python 3.9.14

Follow instructions to install the version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It's good practise to work within a virtual environment whenever using Python. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we use to handle cross origin requests from the frontend server. 

## Database Setup

On first run of this application, uncomment out this method in app.py, then recomment in if you would like the database to stay persistent:
```
db_drop_and_create_all()
```
## Running the server locally

From within the root directory first ensure you are working using your created virtual environment.

To run the server, in bash execute the following
```
chmod +x setup.sh
source setup.sh
export FLASK_DEBUG=1
flask run
```

## Testing
To run tests on the basic functionality of the endpoints, in a separate bash window run:
```
chmod +x setup.sh
source setup.sh
export FLASK_DEBUG=1
python test_app.py
```

To test the permissions, import the postman collection located at [./christian_meme_tests.postman_collection.json](christian_meme_tests.postman_collection.json) in Postman. This contains tests for all roles, and for non-logged in user. 

## Live server

> Find a live version of this site here: `https://myapp-663697908123456.herokuapp.com/`


# API Endpoints

> Base URL `https://myapp-663697908123456.herokuapp.com/`

URI|Method|Action|Curl example|return example
---|---|---|---|---
/meme|GET|Fetches all the memes as a List|`curl https://myapp-663697908123456.herokuapp.com/meme`|`{"memes": [ { "id": 1, "title": "NT Funny", "url": "ntfunny.com" }, { "id": 2, "title": "OT Funny", "url": "otfunny.com" }, { "id": 3, "title": "Bible Funny", "url": "biblefunny.com" } ], "success": true }`
/meme|POST|Creates a new meme|`curl -X POST 'https://myapp-663697908123456.herokuapp.com/meme' -H 'Content-Type: application/json' -H 'Authorization: Bearer <Token>' --data-raw '{ "title": "Test Post 1663019101", "url": "test.post.1663019101.com", "tags": [] }'`|`{"meme_id": 4, "success": true }`|
/meme|PATCH/(id)|Modifies the contents of a stored meme|`curl -X PATCH 'https://myapp-663697908123456.herokuapp.com/meme/1' -H 'Authorization: Bearer <Token>' -H 'Content-Type: text/plain' --data-raw '{ "title": "editTitle" }'`|`{ "meme": { "id": 1, "title": "editTitle", "url": "ntfunny.com" }, "success": true }`|
/meme|DELETE/(id)|Deletes the meme with specified id|`curl -X DELETE 'https://myapp-663697908123456.herokuapp.com/meme/1' -H 'Authorization: Bearer <Token>'`|`{ "deleted": 1, "success": true }`|
/tag|GET|Fetches all the tags as a List|`curl https://myapp-663697908123456.herokuapp.com/tag`|`{ "success": true, "tags": [ { "id": 1, "name": "New Testament" }, { "id": 2, "name": "Old Testament" } ] } `
/tag|POST|Creates a new tag|`curl -X POST 'https://myapp-663697908123456.herokuapp.com/meme' -H 'Content-Type: application/json' -H 'Authorization: Bearer <Token>' --data-raw '{ "name": "test tag"}'`|`{ "success": true, "tag_id": 3 }`|
/tag|PATCH/(id)|Modifies the contents of a stored meme|`curl -X PATCH 'https://myapp-663697908123456.herokuapp.com/tag/1' -H 'Authorization: Bearer <Token>' -H 'Content-Type: text/plain' --data-raw '{ "name": "edit_name" }'`|`{ "success": true, "tag": { "id": 1, "name": "edit_name" } }`|
/tag|DELETE/(id)|Deletes the meme with specified id|`curl -X DELETE 'https://myapp-663697908123456.herokuapp.com/meme/1' -H 'Authorization: Bearer <Token>'`|`{ "deleted": 1, "success": true }`|



## Test tokens:

#### Christian Meme User

`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRJM0RmdmpfSVVFNUFxbjA1cU5IbyJ9.eyJpc3MiOiJodHRwczovL2Rldi02Z2kweXB5Yi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxY2VkYTIyOTA4NTU4NzcyMjZlZjJkIiwiYXVkIjoiY2hyaXN0aWFuLW1lbWUtYXBpIiwiaWF0IjoxNjYzMDkxMTAzLCJleHAiOjE2NjMxNzc1MDMsImF6cCI6IkhPOWtpMnRHT0JLbFMwVzUwOVkyaWZIWUdFZ0l1aVkwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6bWVtZSIsImdldDp0YWciLCJwb3N0Om1lbWUiLCJwb3N0OnRhZyJdfQ.MKmPV-a_qPSNIL0NHdfm6065vEys04VA71roOGavqX-0pwgVlmVcR5QqnqhpPJ01ufIJwUelqFMTa_5pYBrHUW7wr_brDXACwNcKF5Y8boOOKAKjO59OMNiC5qP5M99Yoc28mpNvInnMh0VI77Po-zSxmO6jnQT98uhZrMOk_orfkzBQ5JhUKzbEdr3x5CxV2DBneyxvgZe9NLDhfkVIoruK-t4B7uUOc9YaoULCR1EHkdd-w1tdNDmoPlBrqNIYaCNjhmnKmBG2OuD0jLDyG4ORPidcpiIMTtXOPKhNjHKSxpDbv_enmtSGP7YJuuwhgXVC3_WrBNOxLZ0bjig_qQ`

#### Christian Meme Owner

`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRJM0RmdmpfSVVFNUFxbjA1cU5IbyJ9.eyJpc3MiOiJodHRwczovL2Rldi02Z2kweXB5Yi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxMGNlMjg4NDAyMjFkMWQyMzE2OWIwIiwiYXVkIjoiY2hyaXN0aWFuLW1lbWUtYXBpIiwiaWF0IjoxNjYzMDkwOTg2LCJleHAiOjE2NjMxNzczODYsImF6cCI6IkhPOWtpMnRHT0JLbFMwVzUwOVkyaWZIWUdFZ0l1aVkwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6bWVtZSIsImRlbGV0ZTp0YWciLCJnZXQ6bWVtZSIsImdldDp0YWciLCJwYXRjaDptZW1lIiwicGF0Y2g6dGFnIiwicG9zdDptZW1lIiwicG9zdDp0YWciXX0.drQlq9JMy-6GNHqK4lYmp9r6ILwS1neJho59Zxr0KC9fEe-sSXxql9Bzx6rjlyMyMzOBbFTkGjbFNwZC1KoYW3yEdcqYuaE0ImqQXwQLcc1MQBqYsxyKAK2bM-L1CpLcooGi8tgehv8nfsdFf1xZW_Xs40gl-BEc7W4Awp48LP-PWNMpLhcSf7AUAmd6fox6qgzGsu2oYvKbBS3VGmDJIS56pfY6CN57TvB5V62S-KtHIDuxDGazLPqd4aDmPk7SWCmqmnPKNMKKSbdCcC-1j01IxBlFnV48A05eWwUzU7don3HKLcIpGnapbio9AMpmqV9RnepnPQUrsSKnFg28CA`


## Permissions

Permissions|Details
---|---
get:meme|Gets access to all memes
get:tag|Gets access to all tags
post:meme|Can add memes to the DB
post:tag|Can add tags to the DB
delete:meme|Can delete memes from the DB
delete:tag|Can delete tags from the DB
patch:meme|Can modify memes from the DB
patch:tag|Can modify tags from the DB

## Roles

Role|Permissions
---|---
Christian Memes User| get:meme, get:tag, post:meme, post:tag
Chrsitian Memes Owner| get:meme, get:tag, post:meme, post:tag, patch:meme, patch:tag, delete:meme, delete:tag