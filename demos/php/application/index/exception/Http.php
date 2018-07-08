<?php

namespace app\index\exception;

use think\exception\Handle;
use think\facade\Log;
use think\facade\Request;
use think\facade\Response;

class Http extends Handle {

    public function render(\Exception $e){
        Log::error(['message' => $e->getMessage(), 'code' => $e->getCode(), 'file' => $e->getFile(), 'line' => $e->getLine()]);
        $code = $e->getCode();
        $message = $e->getMessage();
        if ($code === 0) {
            $code = 500;
            $message = "sorry, something is wrong~";
        }
        if (Request::isAjax()) {
            return json(['code' => $code, 'message' => $message, 'timeStamp' => time()]);
        } else{
            $template = config('http_exception_template_404');
            $dialogError = input('param.dialogError/d', 0, 'intval');
            if($dialogError){
                $template = config('http_exception_template_dialog404');
            }
            return Response::create($template, 'view', 200)->assign(['message' => $message]);
        }
    }
}