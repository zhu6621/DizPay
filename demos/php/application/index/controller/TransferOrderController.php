<?php

namespace app\index\controller;

use app\index\model\TransferOrder;
use app\index\service\ApiService;
use app\index\service\TransferOrderService;
use app\index\service\WalletService;

class TransferOrderController extends CommonController {

    private $user_id = 0;

    public function initialize() {
        $user_id = $this->checkLogin();
        if (!$user_id) {
            $this->redirect('Wallet/index');
        }
        $this->user_id = $user_id;
    }

    public function createTransactionOrder() {
        $currency = input('param.currency');
        $amount = input('param.amount');
        $fee = input('param.fee');
        $currency = strtoupper($currency);
        if (empty($currency)) {
            throw new \Exception("currency does not exist", 10002);
        }
        $wallet = WalletService::getWallet($this->user_id, $currency);
        if (!$wallet) {
            throw new \Exception("currency does not exist", 10002);
        }
        $number = TransferOrderService::getOrderNumber();
        $object = TransferOrder::create([
            'number'      => $number,
            'user_id'     => $this->user_id,
            'currency_id' => $currency,
            'amount'      => $amount,
            'fee'         => $fee
        ]);
        ApiService::createTransactionOrder($number, $fee, $amount, $wallet['address']);
        $res = ApiService::payOrder($number);
        $this->responseSuccess($res);
    }


}