package diz.pay.web.controller;

import diz.pay.common.JsonResult;
import diz.pay.common.base.BaseController;
import diz.pay.service.order.OrderService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class OrderController extends BaseController {

    private Logger LOGGER = LoggerFactory.getLogger(OrderController.class);

    @Autowired
    OrderService orderService;

    @RequestMapping("/api/transfer_order")
    @ResponseBody
    public JsonResult transferOrder(String currency, String amount, String fee) {
        if (currency.isEmpty()) {
            return JsonResult.setReturn(10002, "currency does not exist");
        }
        Integer userId = (Integer) session.getAttribute("user");
        return orderService.transferOrder(userId, currency, amount, fee);
    }
}
