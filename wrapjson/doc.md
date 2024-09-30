> HTTP Body

```json
{
  "shell": {
    "env": "python", // string; 硬编码"python"
    "script": "cHJpbnQoIkhlbGxvIFdvcmxkIik=", // string; base64 编码的脚本文件
    "data": {
      "key": "dmFsdWU=", // string; 键值对数据，值是 base64 字符串
    }
  }
}
```

> 其他参数

| 名称    | 参数类型 | 数据类型 | 必填  | 默认值 | 说明          |
| ------- | -------- | -------- | ----- | ------ | ------------- |
| a       | header   | integer  | false | 100    | Header 参数   |
| serial_number | query    | string   | true  | -      | 终端的序列号  |

> 请求成功

```json
{
  "code": "SUCCESS" // string; 响应码
}
```

> 请求失败情景 A


```json
{
  "code": "SHELL_EXEC_FAILED" // string; 指令执行失败
}
```
