package diz.pay.dao.entity;

public class QueryWalletDTO {

    public String currency_id = "";
    public String balance = "";
    public String icon = "";
    public String address_qr_code = "";
    public String address = "";

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getAddress_qr_code() {
        return address_qr_code;
    }

    public void setAddress_qr_code(String address_qr_code) {
        this.address_qr_code = address_qr_code;
    }

    public String getCurrency_id() {
        return currency_id;
    }

    public void setCurrency_id(String currency_id) {
        this.currency_id = currency_id;
    }

    public String getBalance() {
        return balance;
    }

    public void setBalance(String balance) {
        this.balance = balance;
    }

    public String getIcon() {
        return icon;
    }

    public void setIcon(String icon) {
        this.icon = icon;
    }
}
