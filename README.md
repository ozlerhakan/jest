# Jest

Jest is a IPython magic tool to make us one or more HTTP request(s) in a cell.

## How it works

```
$ pip install pyjest
```

## Examples

Please take a look at the `examples` folder about how Jest can be used in a Jupyter notebook in more detail. The snippets below represent a sequence of three cells each of which shows how we can construct a jest call along with required fields for two HTTP calls in one run.   

```
[1] %load_ext jest

[2] consumes = [
    dict(original_keyword='iphone'),
    dict(original_keyword='phone')
]
```

The `consumes` variable holds a list of dictionary. Two different items will be used while jesting a request with a request body.  

```
[3] %%jest --var responses --params consumes 

{
    "url": "http://localhost:8080/path",
    "request": "post",
    "body": {
      "field": "@original_keyword",
      "field": 1
    },
    "headers": {
        "Content-Type": "application/json", 
        "Authorization": "Bearer ASDASADAS",
        "Cookie": "auth_cookie=ASDADASDA"
    }
}
```

Jest saves the response in to the `responses` field. We use `--params` to add that Jest will use it to load data from. The request body references a field name with suffix `@`. So that Jest understands that the referenced field must be in each item of `consumes`. 

```
len(responses) # 2 for each item of `consumes`
```

After having a successful request, we can react the result via `responses`.

## License

MIT
