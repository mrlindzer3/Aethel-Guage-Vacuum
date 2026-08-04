using UnityEngine;

public class QuasicrystalDisplayController : MonoBehaviour
{
    public ComputeShader opaComputeShader;
    public Material targetMaterial;
    
    private GraphicsBuffer nodeBuffer;
    private GraphicsBuffer phaseBuffer;
    private int kernelIndex;
    private int nodeCount = 4096;

    void Start()
    {
        // 1. Initialize node position data
        Vector2[] rawNodes = GenerateQuasicrystalCPU(nodeCount);
        
        // 2. Allocate GPU Graphics Buffers (Structured Buffers)
        nodeBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, nodeCount, sizeof(float) * 2);
        nodeBuffer.SetData(rawNodes);
        
        phaseBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, nodeCount, sizeof(float));

        // 3. Bind to Compute Shader
        kernelIndex = opaComputeShader.FindKernel("Main");
        opaComputeShader.SetBuffer(kernelIndex, "node_positions", nodeBuffer);
        opaComputeShader.SetBuffer(kernelIndex, "phase_outputs", phaseBuffer);
    }

    void Update()
    {
        // Pass dynamic uniforms (oscillating steering angle over time)
        float steeringAngle = Mathf.Sin(Time.time) * 0.2618f; // ~15 degrees max
        opaComputeShader.SetFloat("u_steering_angle", steeringAngle);
        opaComputeShader.SetFloat("u_wavelength", 0.55f);

        // Dispatch compute threads
        int threadGroups = Mathf.CeilToInt(nodeCount / 256f);
        opaComputeShader.Dispatch(kernelIndex, threadGroups, 1, 1);

        // Expose phase buffer directly to the material graph for rendering
        targetMaterial.SetBuffer("_PhaseBuffer", phaseBuffer);
    }

    void OnDestroy()
    {
        nodeBuffer?.Dispose();
        phaseBuffer?.Dispose();
    }

    Vector2[] GenerateQuasicrystalCPU(int count)
    {
        Vector2[] pts = new Vector2[count];
        for(int i = 0; i < count; i++) {
            pts[i] = new Vector2(Random.Range(-15f, 15f), Random.Range(-15f, 15f));
        }
        return pts;
    }
}
