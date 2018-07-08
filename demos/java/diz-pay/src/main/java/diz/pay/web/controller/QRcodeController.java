package diz.pay.web.controller;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.EncodeHintType;
import com.google.zxing.MultiFormatWriter;
import com.google.zxing.client.j2se.MatrixToImageWriter;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;
import diz.pay.common.base.BaseController;
import diz.pay.service.login.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.servlet.ServletOutputStream;
import java.util.HashMap;
import java.util.Map;

@Controller
public class QRcodeController extends BaseController {

    @Autowired
    LoginService loginService;

    @RequestMapping("qr")
    public void index(String text) throws Exception {
        ServletOutputStream out = response.getOutputStream();
        Map<EncodeHintType, Object> config = new HashMap<>();
        config.put(EncodeHintType.CHARACTER_SET, "UTF-8");
        config.put(EncodeHintType.ERROR_CORRECTION, ErrorCorrectionLevel.M);
        config.put(EncodeHintType.MARGIN, 0);
        BitMatrix bitMatrix = new MultiFormatWriter().encode(text, BarcodeFormat.QR_CODE, 200, 200, config);
        MatrixToImageWriter.writeToStream(bitMatrix, "png", out);
    }

}
