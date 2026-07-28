// [AETHEL-MESH-PIPELINE] Owner: mrlindzer3 | Checkpoint: 48df1716c09d4bfe4762dc63e60e3103c1f25d58f151b82fc79861f7f70217d5
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
