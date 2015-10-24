# Cut-Rate Status Collector

Simple service to send and retrieve "current status" messages. Keeps the single most recent message from a given handle.

### URL

`/` or `/<nickname>`
 
HTML of all current statuses at `/view`.

### Method

`GET` | `POST` 
  

### Data Params

``` 
{
    "nickname": "example",
    "status": "This is an update message",
    "code": "ok",
    "token": "<secret>"
}
```


* 'nickname' is an arbitrary handle for the service that's sending its status. Should be something you'll recognize later, and brief. (Can either post to `/` as part of the data payload, or to `/<nickname>` in which case leave it out of the post.)
* 'code' is optional, and determines the color of the display on the HTML page
* 'token' is just a shibboleth used to verify that posts are legit. See TYM for the value.

### Success Response

**Code:** 201 <br />
**Content:** `
    {
  "at": "2015-10-24 08:45:19.086997",
  "code": "info",
  "nickname": "example",
  "status": "update message"
}`

 
### Error Response:

**Code:** 403 <br />
**Content:** `"invalid token"`

### Note:

`POST` to existing nickname changes the code and status values, and updates the timestamp. Any new nickname (assuming a valid token) gets added to the stack.

`GET` from `/` returns all statuses in a JSON array. `GET /<nickname>` returns status of that nick.

`/view` route provides an HTML page with all current statuses.

![view-screenshot](https://dl.dropboxusercontent.com/s/l2ynhntyuk94q4v/view-screen.png?dl=0)