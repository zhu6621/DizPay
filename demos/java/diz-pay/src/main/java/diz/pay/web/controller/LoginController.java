package diz.pay.web.controller;

import diz.pay.common.JsonResult;
import diz.pay.common.base.BaseController;
import diz.pay.service.login.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class LoginController extends BaseController {

    @Autowired
    LoginService loginService;

    @RequestMapping("/")
    public String index() {
        if (checkLogin()) {
            return "wallet";
        } else {
            return "login";
        }
    }

    private boolean checkLogin() {
        return session.getAttribute("user") != null;
    }

    @RequestMapping("/api/password_login")
    @ResponseBody
    public JsonResult passwordLogin(String mobile, String password) {
        return loginService.passwordLogin(session, mobile, password);
    }

}
