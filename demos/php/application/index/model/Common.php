<?php

namespace app\index\model;

use think\Model;

class Common extends Model {
    protected $autoWriteTimestamp = 'datetime';
    protected $createTime = 'created_at';
    protected $updateTime = 'updated_at';
}