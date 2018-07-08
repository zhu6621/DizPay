package diz.pay.service.order;

import diz.pay.common.JsonResult;
import diz.pay.common.enums.ResultEnums;
import diz.pay.common.exception.PayException;
import diz.pay.common.utils.DateUtils;
import diz.pay.common.utils.JsonUtils;
import diz.pay.common.utils.StrUtils;
import diz.pay.dao.entity.CreateOrderDTO;
import diz.pay.dao.entity.PayOrderDTO;
import diz.pay.dao.entity.domain.TransaferOrder;
import diz.pay.dao.entity.domain.Wallet;
import diz.pay.dao.entity.mapper.TransaferOrderMapper;
import diz.pay.service.base.impl.BaseServiceImpl;
import diz.pay.service.wallet.WalletService;
import org.apache.commons.lang3.RandomUtils;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.net.PortUnreachableException;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class OrderService extends BaseServiceImpl {

    @Autowired
    TransaferOrderMapper mapper;

    @Autowired
    WalletService walletService;

    public JsonResult transferOrder(Integer userId, String currency, String amount, String fee) {

        CreateOrderDTO createOrderDTO = createOrder(userId, currency, amount, fee);

        PayOrderDTO payOrderDTO = payOrder(createOrderDTO.getNumber());

        TransaferOrder order = new TransaferOrder();
        order.setNumber(payOrderDTO.getNumber());
        order.setUserId(userId + "");
        order.setCurrencyId(payOrderDTO.getCurrency_id());
        order.setAmount(BigDecimal.valueOf(Double.valueOf(payOrderDTO.getAmount())));
        order.setFee(BigDecimal.valueOf(Double.valueOf(payOrderDTO.getFee())));
        /*
        1 Processing
        2 Complete
        4 Cancel
         */
        order.setStatus(Short.valueOf(payOrderDTO.getStatus()));
        order.setCreatedAt(new Date());
        order.setUpdatedAt(new Date());
        mapper.insertSelective(order);

        return JsonResult.setReturn(ResultEnums.OK);
    }

    private PayOrderDTO payOrder(String number) {
        Map<String, String> params = new HashMap<>();
        params.put("number", number);
        String resp = post(URL_PAY_ORDER, params);

        return JsonUtils.toObj(resp, PayOrderDTO.class);
    }

    private CreateOrderDTO createOrder(Integer userId, String currency, String amount, String fee) {
        Wallet wallet = walletService.getWallet(userId, currency);
        Map<String, String> params = new HashMap<>();
        params.put("number", getOrderNumber());
        params.put("fee", fee);
        params.put("amount", amount);
        params.put("address", wallet.getAddress());
        params.put("to_address", "");
        params.put("extra", "");
        String resp = post(URL_CREATE_TRANSACTION_ORDER, params);

        return JsonUtils.toObj(resp, CreateOrderDTO.class);
    }

    public String getOrderNumber() {
        return StrUtils.concat(DateUtils.dateToStr(new Date(), "yyMMddHHmmss"), RandomUtils.nextInt(1000, 9999));
    }
}
