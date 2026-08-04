using NUnit.Framework;
using UnityEngine;

public class TestOpaIntegration
{
    [Test]
    public void TestGraphicsBufferAllocation()
    {
        int nodeCount = 256;
        GraphicsBuffer nodeBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, nodeCount, sizeof(float) * 2);
        GraphicsBuffer phaseBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, nodeCount, sizeof(float));

        Assert.IsNotNull(nodeBuffer, "Node GraphicsBuffer failed to instantiate.");
        Assert.IsNotNull(phaseBuffer, "Phase GraphicsBuffer failed to instantiate.");
        
        Assert.AreEqual(nodeBuffer.count, nodeCount);
        Assert.AreEqual(phaseBuffer.count, nodeCount);

        nodeBuffer.Release();
        phaseBuffer.Release();
    }
}
