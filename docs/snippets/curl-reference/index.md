---
tags:
    - snippets
    - bash
    - one-liners
---

# cURL HTTP Requests

| Title                                            | URL                                                                                                                                                        |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The Art of Scripting HTTP Requests Using cURL    | [https://curl.se/docs/httpscripting.html](https://curl.se/docs/httpscripting.html)                                                                         |
| cURL Docs                                        | [https://curl.se/docs/manpage.html](https://curl.se/docs/manpage.html)                                                                                     |
| The cURL guide to HTTP requests                  | [https://flaviocopes.com/http-curl/](https://flaviocopes.com/http-curl/)                                                                                   |
| The simplest guide to cURL for REST API requests | [https://dev.to/ritaly/the-simplest-guide-to-curl-for-rest-api-requests-35ii](https://dev.to/ritaly/the-simplest-guide-to-curl-for-rest-api-requests-35ii) |
| cURL - The Ultimate Reference Guide              | [https://www.petergirnus.com/blog/curl-command-line-ultimate-reference-guide](https://www.petergirnus.com/blog/curl-command-line-ultimate-reference-guide) |
| How to use cURL on Windows                       | [https://4sysops.com/archives/how-to-use-curl-on-windows/#rtoc-2](https://4sysops.com/archives/how-to-use-curl-on-windows/#rtoc-2)                         |

**NOTE FOR WINDOWS**: The Windows `curl` command does not use `-X` to denote request methods. For example, instead of `-X POST`, Windows expects `-XPOST`.

Alternatively on Windows, use `curl.exe` instead of `curl`, which should have native support and function similarly to the UNIX version of cURL.

## Making Requests with cURL

**Note**: Add `-v` to any cURL request to show verbose output

### GET

```shell
curl https://api.restful-api.dev/objects
```

With params:

```shell
curl https://api.restful-api.dev/objects/1/

OR

curl https://api.restful-api.dev/objects?id=3
```

With multiple params:

```shell
curl "https://dev.to/api/articles?tag=devjournal&top=5&per_page=5"
```

### POST

Use `-X POST` to denote a POST request. Add a body with `-d`.

Add request headers with `-H`.

Add a useragent string with `-A`

```shell
curl -X POST https://api.restful-api.dev/objects \
-H 'Content-Type: application/json' \
-d '{"name":"Apple MacBook Pro 16","data":{"year":2019,"price":2049.99,"CPU model":"Intel Core i9","Hard disk size":"1 TB","color":"silver"}}' 
```

With headers:

```shell
curl -v \
     -H 'Connection: keep-alive' \
     -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
     -H 'Accept-Language: en-GB,en-US;q=0.8,en;q=0.6' \
     https://api.restful-api.dev/objects
```

With headers and a useragent

```shell
curl -v \
     -H 'Connection: keep-alive' \
     -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
     -H 'Accept-Language: en-GB,en-US;q=0.8,en;q=0.6' \
-A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' \
     https://api.restful-api.dev/objects
```

### PUT

Use `-X PUT` to denote a PUT request

```shell
curl -X PUT https://api.restful-api.dev/objects/:id \
     -H 'Content-Type: application/json' \
     -d '{"name":"Apple MacBook Pro 16","data":{"year":2022,"price":2399.99,"CPU model":"M1","Hard disk size":"1 TB","color":"space grey"}}'
```

### PATCH

Use `-X PATCH` to denote a PATCH request

```shell
curl -X PATCH https://api.restful-api.dev/objects/:id \
     -H 'Content-Type: application/json' \
     -d '{"name":"Fruity name"}'
```

### DELETE

Use `-X DELETE` to denote a DELETE request

```shell
curl -X DELETE https://api.restful-api.dev/objects/:id
```

### Save request as .json for inspection

```shell
## File will be saved to ./request.json
curl -X POST https://api.restful-api.dev/objects \
     -d @request.json \
     -H "Content-Type: application/json"
```

### Save response to a .json file

```shell
curl https://api.restful-api.dev/objects -o response.json
```
