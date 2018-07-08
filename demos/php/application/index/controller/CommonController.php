<?php

namespace app\index\controller;

use think\Controller;
use think\facade\Request;
use think\facade\Session;

class CommonController extends Controller {

    protected function checkLogin() {
        $session = Session::get('user');
        if ($session && isset($session['id']) && $session['id'] > 0) {
            return $session['id'];
        } else {
            return false;
        }
    }

    protected function _response($code = 0, $message, $data = []) {
        if (Request::isAjax()) {
            exit(json_encode(['code' => $code, 'message' => $message, 'data' => $data]));
        } else {
            if ($code == 0) {
                $this->success($message);
            } else {
                $this->error($message ?: 'request error');
            }
        }
    }

    public function responseSuccess($data = [], $message = 'success') {
        return $this->_response(0, $message, $data);
    }

    public function responseError($code, $message) {
        return $this->_response($code, $message, []);
    }

    public function responseParamsError($code = 10001, $message = 'params error !') {
        return $this->_response($code, $message, []);
    }
}
