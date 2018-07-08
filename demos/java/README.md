## Requirements
- Java
- Spring Boot
- MyBatis
- Gradle
- Mysql

## Prepare Data
Initialization using database scripts from data.sql.

## Authentication
Enter your APP ID and APP KEY in \diz-pay\src\main\resources\config\application-local.properties

## Start Project

- Use the Gradle to import the project

- Start a project with \diz-pay\src\main\java\diz\pay\web\Application

- Open browser input your web url (such as http://127.0.0.1:8080 or http://localhost:8080)

## Exception Handling
If your exception is this: 

org.apache.ibatis.binding.BindingException: Invalid bound statement (not found): diz.pay.dao.entity.mapper.xxxx

please check \diz-pay\out\production\classes\diz\pay\dao\entity\mapper contain \diz-pay\src\main\java\diz\pay\dao\entity\mapper all *Mapper.xml file

If not, be consistent.

(You can use a gradle to help you accomplish this, see the \diz-pay\build.gradle task xmlCopy)

# Documentation
You can find the dizpay api documentation [on the website](https://www.dizpay.com/en/developer)