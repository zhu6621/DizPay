package diz.pay.service.login;

import diz.pay.common.JsonResult;
import diz.pay.common.enums.ResultEnums;
import diz.pay.common.utils.DateUtils;
import diz.pay.common.utils.MD5Utils;
import diz.pay.common.utils.StrUtils;
import diz.pay.dao.entity.domain.User;
import diz.pay.dao.entity.domain.UserExample;
import diz.pay.dao.entity.mapper.UserMapper;
import diz.pay.service.base.impl.BaseServiceImpl;
import diz.pay.service.wallet.WalletService;
import org.apache.commons.lang3.RandomUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpSession;
import java.util.Date;
import java.util.List;

@Service
public class LoginService extends BaseServiceImpl {

    @Autowired
    UserMapper userMapper;

    @Autowired
    WalletService walletService;

    public void createUser(String mobile, String password) {
        User user = new User();
        user.setMobile(mobile);
        user.setPassword(MD5Utils.encode(password));
        user.setToken(getToken());
        user.setCreatedAt(new Date());
        user.setUpdatedAt(new Date());
        userMapper.insertSelective(user);

        walletService.createWallet(user.getId());
    }

    public static String getToken() {
        return MD5Utils.encode(StrUtils.concat(DateUtils.currTimestampS(), RandomUtils.nextInt(100000, 999999)));
    }

    public JsonResult passwordLogin(HttpSession session, String mobile, String password) {
        UserExample queryUserExample = new UserExample();
        queryUserExample.createCriteria()
                .andMobileEqualTo(mobile);
        List<User> userList = userMapper.selectByExample(queryUserExample);
        if (userList.isEmpty()) {
            createUser(mobile, password);
        } else {
            User user = userList.get(0);
            if (!user.getPassword().equals(MD5Utils.encode(password))) {
                return JsonResult.setReturn(1002, "Incorrect password");
            } else {
                session.setAttribute("user", user.getId());
            }
        }

        return JsonResult.setReturn(ResultEnums.OK);
    }
}
