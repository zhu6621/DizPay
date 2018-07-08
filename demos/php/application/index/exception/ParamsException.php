<?php

namespace app\index\exception;

use think\Exception;
use Throwable;


class ParamsException extends Exception {

    public function __construct($message = "params error~", $code = 1, Throwable $previous = null) {
        parent::__construct($message, $code, $previous);
    }
}