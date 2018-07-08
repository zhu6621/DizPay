<?php

namespace app\index\service;

class TransferOrderService extends CommonService {
    public static function getOrderNumber() {
        return date('ymdHis') . rand(1000,9999);
    }
}