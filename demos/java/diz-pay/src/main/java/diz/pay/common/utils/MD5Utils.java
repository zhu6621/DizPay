package diz.pay.common.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.UUID;

public class MD5Utils {
    public static String encode(String inStr) {
        MessageDigest md5 = null;
        try {
            md5 = MessageDigest.getInstance("MD5");
        } catch (Exception e) {
            e.printStackTrace();
            return "";
        }
        char[] charArray = inStr.toCharArray();
        byte[] byteArray = new byte[charArray.length];

        for (int i = 0; i < charArray.length; i++)
            byteArray[i] = (byte) charArray[i];
        byte[] md5Bytes = md5.digest(byteArray);
        StringBuffer hexValue = new StringBuffer();
        for (int i = 0; i < md5Bytes.length; i++) {
            int val = ((int) md5Bytes[i]) & 0xff;
            if (val < 16)
                hexValue.append("0");
            hexValue.append(Integer.toHexString(val));
        }
        return hexValue.toString();

    }


    private static final Logger LOGGER = LoggerFactory.getLogger(MD5Utils.class);

    static MessageDigest getDigest() {
        try {
            return MessageDigest.getInstance("MD5");
        } catch (NoSuchAlgorithmException e) {
            LOGGER.error("MD5 getDigest failed:", e);
            throw new RuntimeException(e);
        }
    }

    private static byte[] md5(byte[] data) {
        return getDigest().digest(data);
    }

    private static byte[] md5(String data, String charset) throws UnsupportedEncodingException {
        String useCharset = charset == null ? "UTF8" : charset;
        String realData = data == null ? "" : data;
        return md5(realData.getBytes(useCharset));
    }

    public static String md5Hex(byte[] data, boolean uppercase) {
        return toHexString(md5(data), uppercase);
    }

    public static String md5Hex(String data, String charset, boolean uppercase) {
        try {
            return toHexString(md5(data, charset), uppercase);
        } catch (Exception e) {
            LOGGER.error("md5Hex {}, with {} failed:", data, charset, e);
        }
        return "";
    }

    public static String md5Hex(String data, boolean uppercase) {
        return md5Hex(data, null, uppercase);
    }

    private static final String HEX_CHARS = "0123456789abcdef";
    private static final String HEX_CHARS_UPPER = "0123456789ABCDEF";

    public static String toHexString(byte[] data, boolean uppercase) {
        StringBuilder sb = new StringBuilder(data.length * 2);
        String seed = (uppercase ? HEX_CHARS_UPPER : HEX_CHARS);
        for (int d : data) {
            sb.append(seed.charAt(d >>> 4 & 0xF));
            sb.append(seed.charAt(d & 0xF));
        }
        return sb.toString();
    }

    public static String rand(String seed, boolean upper) {
        return md5Hex(StrUtils.concat(seed, UUID.randomUUID().toString()), upper);
    }


}
