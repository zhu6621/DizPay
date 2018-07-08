<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006~2018 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: liu21st <liu21st@gmail.com>
// +----------------------------------------------------------------------

return [
    'type'            => 'mysql',
    'hostname'        => env('database.hostname', '127.0.0.1'),
    'database'        => env('database.database', 'dizpay_demo'),
    'username'        => env('database.username', 'root'),
    'password'        => env('database.password', 'root'),
    'hostport'        => env('database.hostport', '3306'),
    'dsn'             => '',
    'params'          => [],
    'charset'         => 'utf8',
    'prefix'          => '',
    'debug'           => true,
    'deploy'          => 0,
    'rw_separate'     => false,
    'master_num'      => 1,
    'slave_no'        => '',
    'read_master'     => false,
    'fields_strict'   => true,
    'resultset_type'  => 'array',
    'auto_timestamp'  => false,
    'datetime_format' => 'Y-m-d H:i:s',
    'sql_explain'     => false,
    'builder'         => '',
    'query'           => '\\think\\db\\Query',
    'break_reconnect' => false,
    'break_match_str' => [],
];
