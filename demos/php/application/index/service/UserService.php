<?php

namespace app\index\service;

use app\index\model\User;
use think\Db;

class UserService extends CommonService {

    public static function getUserByMobile($mobile) {
        $user = User::where('mobile', '=', $mobile)->find();
        return $user;
    }

    public static function addUser($mobile, $password, $token = '') {
        if (!$token) $token = self::getToken();
        Db::startTrans();
        try {
            $user = User::create([
                'mobile'   => $mobile,
                'password' => md5($password),
                'token'    => $token
            ]);
            WalletService::createWallet($user->id);
            Db::commit();
            return $user->id;
        } catch (\Exception $e) {
            Db::rollback();
        }
    }

    public static function getToken() {
        return md5(time() . rand(100000, 999999));
    }


}