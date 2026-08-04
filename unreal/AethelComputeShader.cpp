#include "GlobalShader.h"
#include "ShaderParameterStruct.h"
#include "RenderGraphBuilder.h"

class FAethelOpaComputeShader : public FGlobalShader
{
    DECLARE_GLOBAL_SHADER(FAethelOpaComputeShader);
    SHADER_USE_PARAMETER_STRUCT(FAethelOpaComputeShader, FGlobalShader);

    BEGIN_SHADER_PARAMETER_STRUCT(FParameters, )
        SHADER_PARAMETER(float, SteeringAngle)
        SHADER_PARAMETER(float, Wavelength)
        SHADER_PARAMETER(uint32, NumNodes)
        SHADER_PARAMETER_SRV(ShaderResourceView, NodeBuffer)
        SHADER_PARAMETER_UAV(RWShaderResourceView, PhaseBuffer)
    END_SHADER_PARAMETER_STRUCT()
};

IMPLEMENT_GLOBAL_SHADER(FAethelOpaComputeShader, "/ProjectShaders/AethelOpaPass.usf", "AethelOpaComputeMain", SF_Compute);
