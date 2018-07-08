package diz.pay.common.base;

import diz.pay.common.config.AppConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.ModelAttribute;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

public abstract class BaseController {

    @Autowired
    public AppConfig appConfig;

    public HttpServletRequest request;
    public HttpServletResponse response;
    public HttpSession session;

    @ModelAttribute
    public void getRequestResponse(HttpServletRequest request, HttpServletResponse response, HttpSession session) {
        this.request = request;
        this.response = response;
        this.session = session;
    }

}
