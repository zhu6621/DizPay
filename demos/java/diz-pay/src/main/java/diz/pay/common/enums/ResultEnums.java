package diz.pay.common.enums;

public enum ResultEnums {
    OK(0, "success"),
    EXCEPTION(500, "SYSTEM EXCEPTION");

    private int code;
    private String msg;

    ResultEnums(int code, String msg) {
        this.code = code;
        this.msg = msg;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

}
