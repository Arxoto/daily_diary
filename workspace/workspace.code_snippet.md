# vscode 代码片段

## 教程

1. 文件-首选项-配置代码片段
1. input a name and edit file
1. see [VisualStudioCode-snippet](https://code.visualstudio.com/docs/editor/userdefinedsnippets)
1. a help website [snippet-generator](https://snippet-generator.app/?description=&tabtrigger=&snippet=%0A&mode=vscode)

## Example

workspace
```json
{
	"c_include_once":{
		"scope": "c,cpp",
		"prefix": "include_once",
		"body": [
			"#pragma once",
			"#ifndef ${1:__MACRO_NAME__}",
			"#define ${1:__MACRO_NAME__}",
			"",
			"$0",
			"",
			"#endif",
		],
		"description": "避免文件被 include 多次 1. `ifndef` 是语言标准，兼容性好且灵活，但依赖宏名不冲突 2. `pragma once` 部分老编译器不支持，优点是编译快，不会扫描全文件"
	},
	"rust_test_mod": {
		"scope": "rust",
		"prefix": "test_mod",
		"body": [
			"",
			"#[cfg(test)]",
			"mod tests {",
			"    use super::*;",
			"",
			"    $0",
			"}",
			""
		],
		"description": ""
	},
	"rust_test_fn": {
		"scope": "rust",
		"prefix": "test_fn",
		"body": [
			"",
			"#[test]",
			"fn ${1:test_func}() {",
			"    $0",
			"}",
			""
		],
		"description": ""
	},
	"python_main": {
		"scope": "python",
		"prefix": "main",
		"body": [
			"",
			"",
			"def ${1:main}():",
			"    ${2:pass}$0",
			"",
			"",
			"if __name__ == \"__main__\":",
			"    ${1:main}()",
			""
		],
		"description": ""
	},
	"python_log_get": {
		"scope": "python",
		"prefix": "log_get",
		"body": [
		    "import logging",
		    "",
		    "",
		    "LOG = logging.getLogger()",
		    "",
		    "",
		    ""
		],
		"description": ""
	},
	"python_log_init": {
		"scope": "python",
	    "prefix": "log_init",
	    "body": [
	      	"logging.basicConfig(",
	      	"    format=\"%(asctime)s [%(name)s::%(levelname)s] %(message)s\",",
	      	"    level=logging.INFO,",
	      	")",
			"",
			""
	    ],
	    "description": ""
	}
}
```
