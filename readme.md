# develop

- create pages using python file in `pages` folder
- use template in `templates` folder
- pack web files in `public` using `build.py`

```shell
pypy _scripts/build.py
```

- run serve.py` to serve at `127.0.0.1:8000` with hot reload enabled

```shell
pypy _scripts/serve.py
```

# deploy

- use github actions to deploy