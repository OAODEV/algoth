# Cut-Rate Status Collector

Simple service to send and retrieve "current status" messages. Keeps only the latest message from a given handle.

### URL

 `/` or `/status` or `/<nickname>`

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


* 'nickname' is an arbitrary handle for the service that's sending its status. Should be something you'll recognize later, and brief.
* 'code' is optional, and determines the color of the display on the UI page
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
