<?php

namespace app\index\controller;

use app\index\service\ApiService;
use app\index\service\WalletService;
use think\facade\Session;

class WalletController extends CommonController {
    private $user_id = 0;

    public function initialize() {
        $user_id = $this->checkLogin();
        if (!$user_id) {
            $this->redirect('Wallet/index');
        }
        $this->user_id = $user_id;
    }

    public function index() {
        $this->assign('isShowBack', true);
        $this->assign('isShowExit', true);

        return view();
    }

    public function acceptPayment() {
        $this->assign('isShowBack', true);
        $this->assign('isShowExit', false);

        return view();
    }

    public function walletList() {
        $wallet_list = WalletService::getWalletByUserId($this->user_id);
        foreach ($wallet_list as $key => $value) {
            $value['address_qr_code'] = url('index/qr', ['address' => $value['address']]);
            $wallet_list[$key] = $value;
        }
        $this->responseSuccess(['wallet_list' => $wallet_list]);
    }

    public function logout() {
        Session::set('user', null);
        $this->responseSuccess();
    }

    public function currencyConvert() {
        $coins = [
            'BTC',
            'ETH',
            'LTC'
        ];
        $data = [];
        foreach ($coins as $coin) {
            $res = ApiService::currencyConvert($coin);
            if ($res) {
                $array = json_decode($res, 1);
                $data[] = $array[0];
            }
        }
        $this->responseSuccess($data);
    }

    public function createChargeOrder() {
        $amount = input('param.amount');
        $res = ApiService::createChargeOrder($amount);
        $this->responseSuccess($res);
    }
}