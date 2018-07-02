# QuickStart
## 接入方式
商户需通过联系[dizpay支付平台](https://www.dizpay.com/en/contact)申请账户然后获取app_key和app_id。接口BASE_URL:http://api.cryptopay.icaicloud.com, 所有支付接口均采用post。
## 生成签名
POST 参数增加 app_id、app_key 并按照字母顺序排列成 k1=v1&k2=v2 …… 字符串，求字符串的 md5 值（小写）即签名。注意中文需要 utf8 编码！
例 POST 参数：
```json
{
  "number": "8eb9bc53-75ea-4142-8a91-af89d2246379",
  "address": "1DLVkXuZrSVhw9Ymm72csp99A8wufe76F8",
  "to_address": "1DLVkXuZrSVhw9Ymm72csp99A8wufe76F8",
  "amount": "1",
  "fee": "0.002"
}
```
生成列表：
`address=1DLVkXuZrSVhw9Ymm72csp99A8wufe76F8&amount=1&app_id=dp9vC69mdA3QG2VPRe&app_key=e145d582c31928ca103d262b200e882d&fee=0.002&number=8eb9bc53-75ea-4142-8a91-af89d2246379&to_address=1DLVkXuZrSVhw9Ymm72csp99A8wufe76F8`

计算 md5 值（小写）：
`f433acfea90730724f8261fdb0d502e1`
`f433acfea90730724f8261fdb0d502e1`为签名（signature）
最终 POST 参数：
```json
{
  "app_id":"dp9vC69mdA3QG2VPRe",
  "signature":"f433acfea90730724f8261fdb0d502e1",
  "number": "8eb9bc53-75ea-4142-8a91-af89d2246379",
  "address": "1DLVkXuZrSVhw9Ymm72csp99A8wufe76F8",
  "to_address": "1DLVkXuZrSVhw9Ymm72csp99A8wufe76F8",
  "amount": "1",
  "fee": "0.002"
}
```

## python实例
### 创建api类（对所有接口进行统一处理生成签名）
```python
# -*- coding: utf-8 -*-
import hashlib
import requests


class ApiError(Exception):
    def __init__(self, http_status_code, code, message):
        self.http_status_code = http_status_code
        self.code = code
        self.message = message


class Api(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def post(self, url, data):
        data['app_id'] = self.app_id
        data['app_key'] = self.app_key
        items = data.items()
        kv_pair_list = []
        for k, v in items:
            kv_pair_list.append('{}={}'.format(k, v.encode('utf-8') if hasattr(v, 'encode') else v))
        kv_pair_list.sort()
        signature = hashlib.md5('&'.join(kv_pair_list)).hexdigest()
        data.pop('app_key')
        data['signature'] = signature
        r = requests.post(url, json=data, timeout=5)
        if r.status_code == requests.codes.ok:
            if r.encoding is None or r.encoding == 'ISO-8859-1':
                r.encoding = 'UTF-8'
            return r.json()
        elif r.status_code == 400:
            error_data = r.json()
            raise ApiError(r.status_code, error_data['code'], error_data['message'])
        else:
            raise ApiError(r.status_code, -1, {})


merchantApi = Api(YOUR_APP_ID, YOUR_APP_KEY)
```
### 充值
通过充值的方式来完成一次支付，支付场景：用户首先往自己的钱包充值，然后用自己的余额去购买商品，完成一次交易。优点：支付高效快捷可控制，用户能及时得到反馈信息；缺点：用户必须先向商户充值。
#### 1.创建用户钱包
* 在您的用户注册或者登陆后为他们分配数字货币钱包地址。
* 可通过接口`/member/create_wallet`去为每个用户配置数字货币钱包。
* currency_list可以传入你想支持的货币列表，比如`"BTC, ETH"`, 不传会默认创建`BTC LTC DOGE DASH BTG BCH USDT ETH`
```python
url = '{}/member/create_wallet'.format(BASE_URL)
wallet_list = merchant_api.post(url, {'currency_list': None})
```
* 然后把`wallet_list`存入当前用户下。（到此，为用户创建好了钱包）
* 为会员创建好钱包后，引导会员去充值。
#### 2.创建订单
* 可通过接口`/member/create_transaction_order`去创建一个订单。
* `number`字段由商户自己生成（全局唯一），可以通过`uuid.uuid4()`来生成订单号。
* `address`为用户自己的钱包地址（dizpay支付网关可自动识别币种）。
* `to_address`交易目标地址，如果不传递，默认支付给商户
* `fee`如果商户想收取用户的手续费可通过该字段去实现，如设置`{"amount": "100", "fee": "1"}`将会扣掉用户101。
* extra为附带信息。
```python
import uuid


url = '{}/member/create_transaction_order'.format(BASE_URL)
params = {
    'number': uuid.uuid4(),
    'address': '1sLahdrYh4YAFAdrHVUTAuCw8RzDFmn7M',
    'amount': '1',
    'fee': '0',
     'extra': ''
}
res = merchant_api.post(url, params)
```
* 到此用户可以成功创建了一个订单。
#### 3.支付订单
* 创建完订单，我们可根据订单号，接收方钱包地址来完成此次交易。
* 通过接口`/member/pay_order`来支付订单。
* `number`订单号，全局唯一。
```python
import uuid


url = '{}/member/pay_order'.format(base_url)
params = {
    'number': uuid.uuid4()
}
result = merchant_api.post(url, params)
```
* 到此我们就完成了用户之间一次完整的支付
#### 多次支付订单
为了一些特殊的业务场景，我们提供了多次支付订单。例如创建一个红包（相当于一个订单），然后会随机分配给n个人，那么付款的时候需要多次支付，分别付给每个人。如果您愿意，也可以用到其他的一些支付场景。
(1)创建一个多次支付订单。
* 接口：`/member/create_multi_pay_order`。
* `number`字段由商户自己生成（全局唯一），可以通过uuid.uuid4()来生成订单号。
* `address`为用户自己的钱包地址（dizpay支付网关可自动识别币种）。
* `amount`支付金额（多次支付订单的总金额）。
* `fee`如果商户想收取用户的手续费可通过该字段去实现，如设置{"amount": "100", "fee": "1"}将会扣掉用户101。
* `extra`为附带信息。
```python
import uuid


url = '{}/member/create_multi_pay_order'.format(BASE_URL)
params = {
    'number': uuid.uuid4(),
    'address': '1sLahdrYh4YAFAdrHVUTAuCw8RzDFmn7M',
    'amount': '1',
    'fee': '0',
    'extra': ''
}
res = merchant_api.post(url, params)
```
* 这样我们成功创建了一个多次支付订单。
(2)支付多次订单
* 接口： `/member/pay_multi_pay_order`
* `multi_pay_order_number`是用户创建一个订单时的订单号。
* `order_number`是随机生成的订单号全局唯一，当一个订单需要多次支付的时候就需要根据`order_number`去区分，例如创建一个红包（相当于一个订单），然后会随机分配给n个人（那么每个人都相当于会有一个订单号即`order_number`）。
* `to_address`每次支付的目标地址。
* `amount`每此支付的金额。
* `fee`如果商户想收取用户的手续费可通过该字段去实现，如设置{"amount": "100", "fee": "1"}将会扣掉用户101。
* `extra`为附带信息。

```python
import uuid


url = '{}/member/pay_order'.format(base_url)
params = {
    'multi_pay_order_number': 'YOUR_MULTI_ORDER_NUMBER',
    'order_number': uuid.uuid4(),
    'to_address': '1sLahdrYh4YAFAdrHVUTAuCw8RzDFmn7M',
    'amount': '0.5',
    'fee': 0,
    'extra': ''
}
result = merchant_api.post(url, params)
```
* 多次支付此订单。

### 收款
通过收款的方式来完成支付，优点：用户可以将数字货币存储在任意地方，在需要支付的时候再转进商户。缺点：商户不好控制想要收取的金额；而且由于数字货币实时性的限制，用户无法及时得到此次支付的反馈信息（支付成功或者失败）。
#### 通过创建收款订单来完成支付（快速支付）
* 创建一个收款订单，通过api接口`/member/create_charge_order`
* `number`订单编号（全局唯一）
* `amount` 法币金额（您可以自己设定法币的种类，如：USD、CNY） 
* `payments` "BTC=0.001;ETH=0.12"数字货币支付信息，分号分割（数字货币根据法币金额实时兑换）
* `extra` 附加信息
```python
import uuid


url = '{}/member/create_charge_order'.format(base_url)
params = {
    'number': str(uuid.uuid4()),
    'amount': '10',
    'payments': 'BTC=0.001;ETH=0.12',
    'extra': ''
}
result = merchant_api.post(url, params)
```
* 创建完了订单会得到一个支付信息（具体见api 文档）主要是一个收款地址address，然后用户向此地址打款，完成此次支付。支付二维码生成规则：{base_url}/currency_address_qr_code/{address}。
* 具体示例请登录[dizpay](https://www.dizpay.com)查看Accept Payments。
* 查询订单状态可通过接口`/member/query_charge_order`
* 传入订单号`number`根据结果返回的status去查看订单状态：# 1 支付中  2 完成  4 已撤单
```python
url = '{}//member/query_charge_order'.format(base_url)
result = merchant_api.post(url, {'number': 'YOUR_ORDER_NUMBER'})
```

# Documentation
You can find the dizpay api documentation [on the website](https://www.dizpay.com/en/developer)
