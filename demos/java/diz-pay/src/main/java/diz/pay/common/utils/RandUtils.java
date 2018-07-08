package diz.pay.common.utils;

import org.apache.commons.lang3.RandomUtils;

import java.util.UUID;

public class RandUtils extends RandomUtils {

	public static String getMd5Nonce() {
		String uuid = getUUID();
		return MD5Utils.md5Hex(uuid, false);
	}

	public static String getUUID() {
		return UUID.randomUUID().toString().trim();
	}
}
