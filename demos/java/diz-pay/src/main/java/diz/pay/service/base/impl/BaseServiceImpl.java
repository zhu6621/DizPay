package diz.pay.service.base.impl;


import diz.pay.common.config.AppConfig;
import diz.pay.common.utils.HttpUtils;
import diz.pay.common.utils.JsonUtils;
import diz.pay.common.utils.MD5Utils;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public abstract class BaseServiceImpl {

    @Autowired
    public AppConfig appConfig;

    public static String URL_COIN_MARKET_CAP = "https://api.coinmarketcap.com/v1/ticker/";
    public static String URL_CREATE_WALLET = "/member/create_wallet";
    public static String URL_INQUIRY_WALLET = "/member/query_wallet";
    public static String URL_CREATE_TRANSACTION_ORDER = "/member/create_transaction_order";
    public static String URL_PAY_ORDER = "/member/pay_order";

    public String post(String url, Map<String, String> params) {
        params.put("app_id", appConfig.appId);
        params.put("app_key", appConfig.appKey);
        String str = genSortStr(params);
        String encode = MD5Utils.encode(str);
        params.put("signature", encode);
        params.remove("app_key");
        return HttpUtils.doPost(appConfig.baseUrl + url, JsonUtils.toJson(params));
    }

    private static String genSortStr(Map<String, String> params) {
        List<String> keys = new ArrayList<String>(params.keySet());
        Collections.sort(keys);
        String prestr = "";
        for (int i = 0; i < keys.size(); i++) {
            String key = keys.get(i);
            String value = params.get(key);
            if (i == keys.size() - 1) {
                prestr = prestr + key + "=" + value;
            } else {
                prestr = prestr + key + "=" + value + "&";
            }
        }

        return prestr;
    }


}
