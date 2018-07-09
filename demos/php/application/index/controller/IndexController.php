<?php

namespace app\index\controller;

use app\index\exception\ParamsException;
use app\index\service\UserService;
use think\facade\Env;
use think\facade\Session;

class IndexController extends CommonController {

    public function qr() {
        require(Env::get('extend_path') . 'qr/qrlib.php');
        $data = input('param.address/s', '', 'trim');
        header("Content-Type: image/jpeg; charset=utf-8");
        $errorCorrectionLevel = 'L';
        $matrixPointSize = 4;
        \QRcode::png($data, false, $errorCorrectionLevel, $matrixPointSize, 2);
    }

    public function index() {
        if ($this->checkLogin()) {
            $this->redirect('Index/main');
        } else {
            $this->assign('isShowBack', false);
            $this->assign('isShowExit', false);
            return view();
        }
    }

    public function main() {
        if ($this->checkLogin()) {
            $this->assign('isShowBack', false);
            $this->assign('isShowExit', false);
            return view();
        } else {
            $this->redirect('Index/index');
        }
    }

    public function doLogin() {
        $mobile = input('post.mobile/s', '', 'trim');
        $password = input('post.password/s', '', 'trim');
        if (empty($mobile) || empty($password)) {
            throw new ParamsException();
        }
        $user = UserService::getUserByMobile($mobile);
        if (!$user) {
            $id = UserService::addUser($mobile, $password);
            $this->setLogin($id);
            $this->responseSuccess();
        } else {
            if ($user['password'] == md5($password)) {
                $this->setLogin($user['id']);
                $this->responseSuccess();
            } else {
                throw new \Exception("Incorrect password", 10001);
            }
        }
    }

    public function setLogin($id) {
        $data['id'] = $id;
        Session::set('user', $data);
    }

}