package diz.pay.common.exception;

import diz.pay.common.JsonResult;
import diz.pay.common.utils.DateUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.NoHandlerFoundException;

import javax.servlet.http.HttpServletRequest;

@ControllerAdvice
public class GlobalExceptionHandler {
    private Logger LOGGER = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(value = Exception.class)
    @ResponseBody
    public JsonResult defaultErrorHandler(HttpServletRequest req, Exception e) throws Exception {
        printError(e);
        JsonResult result = new JsonResult();
        result.setMsg(e.getMessage());
        if (e instanceof NoHandlerFoundException) {
            result.setCode(HttpStatus.NOT_FOUND.value());
        } else {
            result.setCode(HttpStatus.INTERNAL_SERVER_ERROR.value());
        }
        result.setTimestamp(DateUtils.currTimestampS() + "");
        return result;
    }

    @ExceptionHandler(value = PayException.class)
    @ResponseBody
    public JsonResult defaultPayErrorHandler(HttpServletRequest req, PayException e) throws Exception {
        printError(e);
        JsonResult result = new JsonResult();
        result.setMsg(e.getMessage());
        result.setCode(e.getCode() == null ? 500 : e.getCode());
        result.setTimestamp(DateUtils.currTimestampS() + "");
        return result;
    }

    private void printError(Exception e) {
        LOGGER.error(e.getMessage(), e);
    }
}
