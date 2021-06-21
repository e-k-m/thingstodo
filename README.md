# thingstodo

![](https://github.com/e-k-m/thingstodo/workflows/main/badge.svg)

> service for managing TODOs

[Installation and Usage](#installation-and-usage) | [Environment Variables](#environment-variables) | [Getting Up And Running](#getting-up-and-running) | [API](#api) | [Benchmarks](#benchmarks) | [See Also](#see-also)

The main feature are:

- Manages TODOs

## Installation and Usage

```bash
pip install .
# set env var
thingstodo-utils db upgrade
<your favorite wsgi server> thingstodo:app
```

## Environment Variables

- THINGS_TODO_DATABASE: SQLAlchemy database connection URL e.g.
postgresql://postgres:mysecretpassword@localhost/thingstodo or
sqlite:///todo.db.

- THINGS_TODO_SECRET: A secret. 

- THINGS_TODO_LOG_LEVEL: Log level to be used, defaults to
WARNING. Possible values are DEBUG INFO WARNING ERROR, CRITICAL or
NOTSET.

## Getting Up and Running

```bash
nox -l
```

## API

```yml 
openapi: 3.0.0
info:
  title: TODO API
  description: Service for managing TODOs
  version: 0.0.0.dev
servers:
  - url: "https://todo.infra3d.ch/api/v0.0"
    description: Production server
  - url: "https://todo.devel.infra3d.ch/api/v0.0"
    description: Development server
paths:
  /todos:
    get:
      summary: Get TODOs
      parameters:
        - $ref: "#/components/parameters/page"
        - $ref: "#/components/parameters/limit"
        - $ref: "#/components/parameters/count"
        - $ref: "#/components/parameters/order"
        - $ref: "#/components/parameters/filter"
      responses:
        '200':
          description: TODOs
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Todos"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
    post:
      summary: Create TODO
      requestBody:
        description: TODO
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Todo'
      responses:
        '201':
          description: TODO
          headers:
            Location:
              description: Location
              schema:
                type: string
                format: uri
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Todo"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /todos/{id}:
    get:
      summary: Get TODO
      parameters:
        - name: id
          in: path
          required: true
          description: TODO ID
          schema:
            type: string
      responses:
        '200':
          description: TODO
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Todo"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
    put:
      summary: Update TODO
      parameters:
        - name: id
          in: path
          required: true
          description: TODO ID
          schema:
            type: string
      requestBody:
        description: TODO
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Todo'
      responses:
        '201':
          description: TODO
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Todo"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
    delete:
      summary: Delete TODO
      parameters:
        - name: id
          in: path
          required: true
          description: TODO ID
          schema:
            type: string
      responses:
        '204':
          description: Null response
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Todo"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
components:
  parameters:
    # pagination
    page:
      name: page
      in: query
      description: "N-th Page of max N collection items."
      required: false
      schema:
        type: integer
        format: int32
    limit:
      name: limit
      in: query
      description: "Max N collection items to return."
      required: false
      schema:
        type: integer
        format: int32
        maximum: 100
    count:
      name: count
      in: query
      description: "If total collection items count should be returned."
      required: false
      schema:
        type: boolean
    # sorting
    order:
      name: order
      in: query
      description: "Collection order with: property [asc | desc] {, property [asc | desc]}."
      required: false
      schema:
        type: string
    # filtering
    filter:
      name: filter
      in: query
      description: "Collection filter with: property operator value {, property [asc | desc]}."
      required: false
      schema:
        type: string
  schemas:
    Todo:
      type: object
      required:
        - text
      properties:
        id:
          type: string
          readOnly: true
        text:
          type: string
        iscompleted:
          type: boolean
          default: false
    Todos:
      type: object
      properties:
        "@nextLink":
          type: string
          format: uri
        count:
          type: integer
          format: int32        
        value:
          type: array
          items:
            $ref: "#/components/schemas/Todo"
    ErrorResponse:
      type: object
      required:
        - error
      properties:
        error:
          $ref: "#/components/schemas/Error"
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string
        target:
          type: string
        details:
          type: array
          items:
            $ref: "#/components/schemas/Error"
        innererror:
          $ref: "#/components/schemas/InnerError"
    InnerError:
      type: object
      additionalProperties: true
      properties:
        code:
          type: string
        innererror:
          $ref: "#/components/schemas/InnerError"

```

## Benchmarks

```text
Postgres 9.3, gunicorn -w 3 -k gevent
wrk -t12 -c400 -d30s http://127.0.0.1:5000/api/v0.0/todos
Running 30s test @ http://127.0.0.1:5000/api/v0.0/todos
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     6.10ms    1.17ms  24.97ms   98.03%
    Req/Sec   326.09    137.00   520.00     34.58%
  14753 requests in 30.07s, 116.10MB read
  Socket errors: connect 0, read 0, write 0, timeout 5
Requests/sec:    490.63
Transfer/sec:      3.86MB
```

## See Also

- [things](https://github.com/e-k-m/things): A frontend using this service.

- [thingstodo](https://github.com/e-k-m/thingsusers): A service that runs in conjuction with this service.

- [wtoolzargs](https://github.com/e-k-m/wtoolzargs) and [wtoolzexceptions](https://github.com/e-k-m/wtoolzexceptions): Libraries used
  in this service.
