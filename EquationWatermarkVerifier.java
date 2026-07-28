import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;

public final class EquationWatermarkVerifier {

    public static String computeEquationHash(String latexEquation) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] encodedhash = digest.digest(latexEquation.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(encodedhash);
    }

    public static String computeNestedWatermarkHash(String imageMeta, String latexEquation) throws NoSuchAlgorithmException {
        String baseEquationHash = computeEquationHash(latexEquation);
        String combinedPayload = imageMeta + "::" + baseEquationHash + "::" + latexEquation;
        
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] encodedhash = digest.digest(combinedPayload.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(encodedhash);
    }

    private static String bytesToHex(byte[] hash) {
        StringBuilder hexString = new StringBuilder(2 * hash.length);
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
}
