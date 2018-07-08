package diz.pay.common.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Value("${app.id}")
    public String appId;

    @Value("${app.key}")
    public String appKey;

    @Value("${base.url}")
    public String baseUrl;

    @Value("${currency.list}")
    public String currencyList;

}
