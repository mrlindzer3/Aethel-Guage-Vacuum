import java.security.NoSuchAlgorithmException;

public class EquationTest {
    public static void main(String[] args) {
        try {
            String eq = "E = mc^2";
            String eqHash = EquationWatermarkVerifier.computeEquationHash(eq);
            String nestedHash = EquationWatermarkVerifier.computeNestedWatermarkHash("meta_v1", eq);
            System.out.println("Eq Hash: " + eqHash);
            System.out.println("Nested Hash: " + nestedHash);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }
}
