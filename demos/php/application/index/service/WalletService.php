<?php

namespace app\index\service;

use app\index\model\Wallet;

class WalletService extends CommonService {

    public static function getCurrencyAddressByUserId($user_id) {
        return Wallet::where('user_id', '=', $user_id)->column ('address');
    }

    public static function createWallet($user_id) {
        $wallet_list = ApiService::createWallet();
        if (is_array($wallet_list) && isset($wallet_list['objects'])) {
            $currency_list = $wallet_list['objects'];
            foreach ($currency_list as $value) {
                self::addOneCurrency($user_id, $value['currency_id'], $value['address']);
            }
        } else {
            throw new \Exception("network error");
        }
    }

    public static function getWalletByUserId($user_id) {
        $address = self::getCurrencyAddressByUserId($user_id);
        $wallet_list = ApiService::inquiryWallet(implode(',', $address));
        if(is_array($wallet_list) && isset($wallet_list['objects'])){
            return $wallet_list['objects'];
        } else {
            return [];
        }
    }

    public static function getWallet($user_id, $currency_id) {
        return Wallet::where([['user_id', '=', $user_id], ['currency_id', '=', $currency_id]])->find();
    }

    public static function addOneCurrency($user_id, $currency_id, $address) {
        $data = [
            'user_id'     => $user_id,
            'currency_id' => $currency_id,
            'address'     => $address
        ];
        return Wallet::create($data)->id;
    }

}