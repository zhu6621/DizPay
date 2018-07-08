package diz.pay.web.controller;

import diz.pay.common.JsonResult;
import diz.pay.common.base.BaseController;
import diz.pay.common.enums.ResultEnums;
import diz.pay.service.wallet.WalletService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class WalletController extends BaseController {

    private Logger LOGGER = LoggerFactory.getLogger(WalletController.class);

    @Autowired
    WalletService walletService;

    @RequestMapping("/api/wallet")
    @ResponseBody
    public JsonResult getWallet() {
        Integer userId = (Integer) session.getAttribute("user");
        return walletService.getWallet(userId);
    }

    @RequestMapping("/api/currency_convert")
    @ResponseBody
    public String currencyConvert() {
        return walletService.currencyConvert();
    }

    @RequestMapping("/api/log_out")
    @ResponseBody
    public JsonResult logout() {
        session.setAttribute("user", null);
        return JsonResult.setReturn(ResultEnums.OK);
    }
}
