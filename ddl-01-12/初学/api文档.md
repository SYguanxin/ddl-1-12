---
title: 个人项目 v1.0.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.17"
---
# 个人项目

> v1.0.0

Base URLs:

* <a href="http://127.0.0.1:5000">测试环境: http://127.0.0.1:5000</a>

# 示例项目

## GET 通过id查询事项

GET /items/{id}

### 请求参数


| 名称 | 位置 | 类型   | 必选 | 说明     |
| ---- | ---- | ------ | ---- | -------- |
| id   | path | string | 是   | item的id |

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "id": 0,
        "title": "string",
        "body": "string",
        "ifdone": false,
        "href": "string",
        "insert_time": "string",
        "ddl": "string"
      }
    ]
  },
  "msg": "string"
}
```

### 返回结果


| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

### 返回数据结构

状态码 **200**


| 名称               | 类型                  | 必选  | 约束 | 中文名   | 说明                    |
| ------------------ | --------------------- | ----- | ---- | -------- | ----------------------- |
| » code            | integer               | true  | none |          | none                    |
| » data            | object                | false | none |          | none                    |
| »» items         | [[Item](#schemaitem)] | true  | none |          | none                    |
| »»» id          | integer               | true  | none |          | none                    |
| »»» title       | string¦null          | true  | none | 标题     | none                    |
| »»» body        | string¦null          | true  | none | 内容     | none                    |
| »»» ifdone      | boolean¦null         | true  | none | 是否完成 | 是的话为True，否为False |
| »»» href        | string¦null          | true  | none | 地址     | none                    |
| »»» insert_time | string                | true  | none | 添加时间 | none                    |
| »»» ddl         | string¦null          | true  | none | 截止时间 | none                    |
| » msg             | string                | true  | none |          | none                    |

## DELETE 根据id删除事项

DELETE /items/{id}

### 请求参数


| 名称 | 位置 | 类型   | 必选 | 说明 |
| ---- | ---- | ------ | ---- | ---- |
| id   | path | string | 是   | none |

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}
```

### 返回结果


| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

### 返回数据结构

状态码 **200**


| 名称    | 类型    | 必选 | 约束 | 中文名 | 说明 |
| ------- | ------- | ---- | ---- | ------ | ---- |
| » code | integer | true | none |        | none |
| » msg  | string  | true | none |        | none |
| » data | object  | true | none |        | none |

## POST 添加一条新的待办事项

POST /items

> Body 请求参数

```json
{
  "title": "string",
  "body": "string",
  "ddl": "string"
}
```

### 请求参数


| 名称     | 位置 | 类型   | 必选 | 说明             |
| -------- | ---- | ------ | ---- | ---------------- |
| body     | body | object | 否   | none             |
| » title | body | string | 是   | none             |
| » body  | body | string | 是   | none             |
| » ddl   | body | string | 是   | 以"datetime"形式 |

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "body": "string",
        "ddl": "string",
        "href": "string",
        "id": 0,
        "ifdone": true,
        "insert_time": "string",
        "title": "string"
      }
    ]
  },
  "msg": "string"
}
```

### 返回结果


| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

### 返回数据结构

状态码 **200**


| 名称               | 类型     | 必选  | 约束 | 中文名 | 说明 |
| ------------------ | -------- | ----- | ---- | ------ | ---- |
| » code            | integer  | true  | none |        | none |
| » data            | object   | true  | none |        | none |
| »» items         | [object] | true  | none |        | none |
| »»» body        | string   | false | none |        | none |
| »»» ddl         | string   | false | none |        | none |
| »»» href        | string   | false | none |        | none |
| »»» id          | integer  | false | none |        | none |
| »»» ifdone      | boolean  | false | none |        | none |
| »»» insert_time | string   | false | none |        | none |
| »»» title       | string   | false | none |        | none |
| » msg             | string   | true  | none |        | none |

## GET 通过其他方式查询多条事项

GET /items

若不填ifdone和sch则分页查询全部数据

### 请求参数


| 名称   | 位置  | 类型    | 必选 | 说明                                     |
| ------ | ----- | ------- | ---- | ---------------------------------------- |
| ifdone | query | integer | 否   | 通过是否完成查询，如果不用这种方式请不填 |
| page   | query | integer | 否   | 默认值为1                                |
| sch    | query | string  | 否   | 通过关键词查询，不用请不填               |

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "id": 0,
        "title": "string",
        "body": "string",
        "ifdone": false,
        "href": "string",
        "insert_time": "string",
        "ddl": "string"
      }
    ],
    "page": 0,
    "total_result": 0
  },
  "msg": "string"
}
```

### 返回结果


| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

### 返回数据结构

状态码 **200**


| 名称               | 类型                  | 必选 | 约束 | 中文名   | 说明                    |
| ------------------ | --------------------- | ---- | ---- | -------- | ----------------------- |
| » code            | integer               | true | none |          | none                    |
| » data            | object                | true | none |          | none                    |
| »» items         | [[Item](#schemaitem)] | true | none |          | none                    |
| »»» id          | integer               | true | none |          | none                    |
| »»» title       | string¦null          | true | none | 标题     | none                    |
| »»» body        | string¦null          | true | none | 内容     | none                    |
| »»» ifdone      | boolean¦null         | true | none | 是否完成 | 是的话为True，否为False |
| »»» href        | string¦null          | true | none | 地址     | none                    |
| »»» insert_time | string                | true | none | 添加时间 | none                    |
| »»» ddl         | string¦null          | true | none | 截止时间 | none                    |
| »» page          | integer               | true | none |          | none                    |
| »» total_result  | integer               | true | none |          | none                    |
| » msg             | string                | true | none |          | none                    |

## PUT 将待办改成已完成或已完成改成待办

PUT /items

### 请求参数


| 名称 | 位置  | 类型   | 必选 | 说明                                    |
| ---- | ----- | ------ | ---- | --------------------------------------- |
| code | query | string | 是   | code可为“true”，“false”，不分大小写 |

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "id": 0,
        "title": "string",
        "body": "string",
        "ifdone": false,
        "href": "string",
        "insert_time": "string",
        "ddl": "string"
      }
    ],
    "page": 0,
    "total_result": 0
  },
  "msg": "string"
}
```

### 返回结果


| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

### 返回数据结构

状态码 **200**


| 名称               | 类型                  | 必选 | 约束 | 中文名   | 说明                    |
| ------------------ | --------------------- | ---- | ---- | -------- | ----------------------- |
| » code            | integer               | true | none |          | none                    |
| » data            | object                | true | none |          | none                    |
| »» items         | [[Item](#schemaitem)] | true | none |          | none                    |
| »»» id          | integer               | true | none |          | none                    |
| »»» title       | string¦null          | true | none | 标题     | none                    |
| »»» body        | string¦null          | true | none | 内容     | none                    |
| »»» ifdone      | boolean¦null         | true | none | 是否完成 | 是的话为True，否为False |
| »»» href        | string¦null          | true | none | 地址     | none                    |
| »»» insert_time | string                | true | none | 添加时间 | none                    |
| »»» ddl         | string¦null          | true | none | 截止时间 | none                    |
| »» page          | integer               | true | none |          | none                    |
| »» total_result  | integer               | true | none |          | none                    |
| » msg             | string                | true | none |          | none                    |

## DELETE 根据完成状态删除或全删除

DELETE /items

### 请求参数


| 名称     | 位置  | 类型   | 必选 | 说明                                           |
| -------- | ----- | ------ | ---- | ---------------------------------------------- |
| del_code | query | string | 否   | true表示删除已完成，false删除未完成，all全删除 |

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}
```

### 返回结果


| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

### 返回数据结构

状态码 **200**


| 名称    | 类型    | 必选 | 约束 | 中文名 | 说明 |
| ------- | ------- | ---- | ---- | ------ | ---- |
| » code | integer | true | none |        | none |
| » msg  | string  | true | none |        | none |
| » data | object  | true | none |        | none |

## PUT 通过id更改事项完成状态

PUT /item/{id}

### 请求参数


| 名称 | 位置 | 类型   | 必选 | 说明 |
| ---- | ---- | ------ | ---- | ---- |
| id   | path | string | 是   | none |

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "body": "string",
        "ddl": "string",
        "href": "string",
        "id": 0,
        "ifdone": true,
        "insert_time": "string",
        "title": "string"
      }
    ]
  },
  "msg": "string"
}
```

### 返回结果


| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

### 返回数据结构

状态码 **200**


| 名称               | 类型     | 必选  | 约束 | 中文名 | 说明 |
| ------------------ | -------- | ----- | ---- | ------ | ---- |
| » code            | integer  | true  | none |        | none |
| » data            | object   | true  | none |        | none |
| »» items         | [object] | true  | none |        | none |
| »»» body        | string   | false | none |        | none |
| »»» ddl         | string   | false | none |        | none |
| »»» href        | string   | false | none |        | none |
| »»» id          | integer  | false | none |        | none |
| »»» ifdone      | boolean  | false | none |        | none |
| »»» insert_time | string   | false | none |        | none |
| »»» title       | string   | false | none |        | none |
| » msg             | string   | true  | none |        | none |

# 数据模型

<h2 id="tocS_Item">Item</h2>

<a id="schemaitem"></a>
<a id="schema_Item"></a>
<a id="tocSitem"></a>
<a id="tocsitem"></a>

```json
{
  "id": 0,
  "title": "string",
  "body": "string",
  "ifdone": false,
  "href": "string",
  "insert_time": "string",
  "ddl": "string"
}

```

### 属性


| 名称        | 类型          | 必选 | 约束 | 中文名   | 说明                    |
| ----------- | ------------- | ---- | ---- | -------- | ----------------------- |
| id          | integer       | true | none |          | none                    |
| title       | string¦null  | true | none | 标题     | none                    |
| body        | string¦null  | true | none | 内容     | none                    |
| ifdone      | boolean¦null | true | none | 是否完成 | 是的话为True，否为False |
| href        | string¦null  | true | none | 地址     | none                    |
| insert_time | string        | true | none | 添加时间 | none                    |
| ddl         | string¦null  | true | none | 截止时间 | none                    |
