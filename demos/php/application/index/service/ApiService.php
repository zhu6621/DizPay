<?php

namespace app\index\service;

use app\index\exception\ParamsException;
use think\facade\Log;

class ApiService extends CommonService {

    const URL_COIN_MARKET_CAP = 'https://api.coinmarketcap.com/v1/ticker/';
    const URL_CREATE_WALLET = '/member/create_wallet';
    const URL_INQUIRY_WALLET = '/member/query_wallet';
    const URL_CREATE_TRANSACTION_ORDER = '/member/create_transaction_order';
    const URL_PAY_ORDER = '/member/pay_order';

    /**
     * @param string $currency_list
     * @return mixed
     * @throws ParamsException
     */
    public static function createWallet($currency_list = '') {
        $pay_config = config('pay.');
        if (!$currency_list) {
            $currency_list = $pay_config['currency_list'];
        }
        $data = [
            'currency_list' => $currency_list
        ];
        $wallet_list = self::post(self::URL_CREATE_WALLET, $data);
        return $wallet_list;
    }

    /**
     * @param $address_list
     * @return mixed
     * @throws ParamsException
     */
    public static function inquiryWallet($address_list) {
        $data = [
            'address_list' => $address_list
        ];
        $list = self::post(self::URL_INQUIRY_WALLET, $data);
        return $list;
    }

    /**
     * @param $number
     * @param $fee
     * @param $amount
     * @param $address
     * @param string $to_address
     * @param string $extra
     * @return mixed
     * @throws ParamsException
     */
    public static function createTransactionOrder($number, $fee, $amount, $address, $to_address = '', $extra = '') {
        $data = [
            'number'     => $number,
            'fee'        => $fee,
            'amount'     => $amount,
            'address'    => $address,
            'to_address' => $to_address,
            'extra'      => $extra,
        ];
        $res = self::post(self::URL_CREATE_TRANSACTION_ORDER, $data);
        return $res;
    }

    /**
     * @param $number
     * @return mixed
     * @throws ParamsException
     */
    public static function payOrder($number) {
        $data = [
            'number' => $number
        ];
        $res = self::post(self::URL_PAY_ORDER, $data);
        return $res;
    }

    /**
     * @param $coin
     * @return bool|mixed
     */
    public static function currencyConvert($coin) {
        $coins = [
            'BTC' => 'bitcoin',
            'ETH' => 'ethereum',
            'LTC' => 'litecoin'
        ];
        $url = self::URL_COIN_MARKET_CAP . $coins[strtoupper($coin)] . '/';
        $res = self::curlGet($url);
        return $res;
    }


    /**
     * @param $url
     * @param $data
     * @return mixed
     * @throws ParamsException
     */
    private static function post($url, $data) {
        $pay_config = config('pay.');
        if ($pay_config['app_id'] == '' || $pay_config['app_key'] == '') {
            throw new ParamsException("please config app_id and app_key !", 10001);
        }
        $data['app_id'] = $pay_config['app_id'];
        $data['app_key'] = $pay_config['app_key'];
        ksort($data);
        $new_data = [];
        foreach ($data as $key => $value) {
            $new_data[] = $key . '=' . $value;
        }
        $str = implode('&', $new_data);
        $signature = md5($str);
        unset($data['app_key']);
        $data['signature'] = $signature;
        $request_url = $pay_config['base_url'] . $url;
        $res = self::curlPost($request_url, $data);
        return json_decode($res, 1);
    }

    /**
     * @param $url
     * @param $data
     * @throws \Exception
     */
    private static function curlPost($url, $data) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        $result = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_errno = curl_errno($ch);
        Log::debug("url={$url},http_code={$http_code}, data=" . json_encode($data) . ", res=" . $result);
        if ($curl_errno) {
            $errorMessage = serialize(curl_error($ch));
            Log::error("[POST] Network error!url={$url},http_code={$http_code}, data=" . json_encode($data) . ", errorMessage={$errorMessage}");
            curl_close($ch);
            throw new \Exception("network error~", 40000);
        }
        curl_close($ch);
        //200 OK Successful request
        //400 Bad Request Returns JSON with the error message, refer to Error Codes
        //{"message": {"number": "order does not exist"}, "code": 1001}
        //{"message": {"balance": "current balance < 0.00116721"}, "code": 1008}
        //1000	Field Format Error(Required, Range, Type)
        //1001	Something does not exist
        //1002	Something does not match
        //1003	Something is invalid
        //1008	Balance is not enough
        //1051	Wallet Server went wrong
        //401 Unauthorized Couldn’t authenticate your request
        //500 Internal Server Error Something went wrong
        switch ($http_code) {
            case 200:
                return $result;
                break;
            case 400:
                $resArray = json_decode($result, 1);
                $errorCode = $resArray['code'];
                if ($errorCode == 1008) {
                    throw new \Exception("Balance is not enough", 40000 + $resArray['code']);
                } else {
                    throw new \Exception(implode("\t", $resArray['message']), 40000 + $resArray['code']);
                }
                break;
            case 401:
                throw new \Exception("Unauthorized Couldn’t authenticate your request", 40401);
                break;
            case 500:
                throw new \Exception("Unauthorized Couldn’t authenticate your request", 50000);
                break;
            default:
                throw new \Exception("net work exception", 500);
                break;
        }
    }

    /**
     * @param $url
     * @return bool|mixed
     */
    private static function curlGet($url) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        $result = curl_exec($ch);
        Log::debug("{$url} res:" . $result);
        if (curl_errno($ch)) {
            $errorMessage = serialize(curl_error($ch));
            Log::error("Access network error<http status " . curl_errno($ch) . ">, method:get,url:  {$url} ,error: {$errorMessage} ");
            return false;
        }
        curl_close($ch);
        return $result;
    }

}