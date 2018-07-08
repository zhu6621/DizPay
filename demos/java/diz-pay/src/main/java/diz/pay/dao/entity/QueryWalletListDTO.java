package diz.pay.dao.entity;

import java.util.List;

public class QueryWalletListDTO {

    private List<QueryWalletDTO> wallet_list;

    public List<QueryWalletDTO> getWallet_list() {
        return wallet_list;
    }

    public void setWallet_list(List<QueryWalletDTO> wallet_list) {
        this.wallet_list = wallet_list;
    }
}
