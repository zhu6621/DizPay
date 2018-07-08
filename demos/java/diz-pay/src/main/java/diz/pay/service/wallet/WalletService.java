package diz.pay.service.wallet;

import diz.pay.common.JsonResult;
import diz.pay.common.enums.ResultEnums;
import diz.pay.common.utils.DateUtils;
import diz.pay.common.utils.HttpUtils;
import diz.pay.common.utils.JsonUtils;
import diz.pay.dao.entity.QueryConvertDTO;
import diz.pay.dao.entity.QueryWalletDTO;
import diz.pay.dao.entity.QueryWalletListDTO;
import diz.pay.dao.entity.domain.Wallet;
import diz.pay.dao.entity.domain.WalletExample;
import diz.pay.dao.entity.mapper.WalletMapper;
import diz.pay.service.base.impl.BaseServiceImpl;
import org.apache.commons.lang3.StringUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class WalletService extends BaseServiceImpl {

    @Autowired
    WalletMapper walletMapper;

    public void createWallet(Integer id) {
        Map<String, String> params = new HashMap<>();
        params.put("currency_list", appConfig.currencyList);
        String resp = post(URL_CREATE_WALLET, params);

        JSONObject jsonObject = null;
        try {
            jsonObject = new JSONObject(resp);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        JSONArray objects = jsonObject.optJSONArray("objects");
        if (objects != null) {
            int length = objects.length();
            for (int i = 0; i < length; i++) {
                JSONObject obj = objects.optJSONObject(i);
                String currency_id = obj.optString("currency_id");
                String balance = obj.optString("balance");
                String address = obj.optString("address");

                Wallet wallet = new Wallet();
                wallet.setUserId(id + "");
                wallet.setAddress(address);
                wallet.setCurrencyId(currency_id);
                wallet.setCreatedAt(new Date());
                wallet.setUpdatedAt(new Date());
                walletMapper.insertSelective(wallet);
            }
        }

    }

    public JsonResult getWallet(Integer userId) {
        WalletExample example = new WalletExample();
        example.createCriteria().andUserIdEqualTo(userId + "");
        List<Wallet> walletList = walletMapper.selectByExample(example);
        List<String> addressList = new ArrayList<>();
        for (Wallet wallet : walletList) {
            addressList.add(wallet.getAddress());
        }
        String addressStr = StringUtils.join(addressList.toArray(), ",");

        Map<String, String> params = new HashMap<>();
        params.put("address_list", addressStr);
        String resp = post(URL_INQUIRY_WALLET, params);

        List<QueryWalletDTO> netWalletList = new ArrayList<>();

        JSONObject jsonObject = null;
        try {
            jsonObject = new JSONObject(resp);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        JSONArray objects = jsonObject.optJSONArray("objects");
        if (objects != null) {
            int length = objects.length();
            for (int i = 0; i < length; i++) {
                JSONObject obj = objects.optJSONObject(i);
                String currency_id = obj.optString("currency_id");
                String balance = obj.optString("balance");
                String address = obj.optString("address");
                QueryWalletDTO wallet = new QueryWalletDTO();
                wallet.setCurrency_id(currency_id);
                wallet.setAddress_qr_code("/qr?text=" + address);
                wallet.setAddress(address);
                wallet.setBalance(balance);
                netWalletList.add(wallet);
            }
        }

        QueryWalletListDTO queryWalletListDTO = new QueryWalletListDTO();
        queryWalletListDTO.setWallet_list(netWalletList);
        return JsonResult.setReturn(ResultEnums.OK, queryWalletListDTO);
    }

    public Wallet getWallet(Integer userId, String currency) {
        WalletExample example = new WalletExample();
        example.createCriteria()
                .andCurrencyIdEqualTo(currency)
                .andUserIdEqualTo(userId + "");
        List<Wallet> walletList = walletMapper.selectByExample(example);
        return walletList.get(0);
    }

    public String currencyConvert() {

        HashMap<String, String> map = new HashMap<>();
        map.put("BTC", "bitcoin");
        map.put("ETH", "ethereum");
        map.put("LTC", "litecoin");

        List<QueryConvertDTO> queryConvertList = new ArrayList<>();
        Iterator<String> iterator = map.keySet().iterator();
        while (iterator.hasNext()) {
            String key = iterator.next();
            String value = map.get(key);

            String resp = HttpUtils.doGetRequest(URL_COIN_MARKET_CAP + value + "/");
            JSONArray jsonArray = null;
            try {
                jsonArray = new JSONArray(resp);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            QueryConvertDTO queryConvertDTO = JsonUtils.toObj(jsonArray.optJSONObject(0).toString(), QueryConvertDTO.class);
            queryConvertList.add(queryConvertDTO);
        }

        JsonResult ret = new JsonResult();
        ret.setCode(ResultEnums.OK.getCode());
        ret.setMsg(ResultEnums.OK.getMsg());
        ret.setData(queryConvertList);
        ret.setTimestamp(DateUtils.currTimestampS() + "");
        return JsonUtils.toJson(ret);
    }

}
