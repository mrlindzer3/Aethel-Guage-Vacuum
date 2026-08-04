#include "RixInterfaces.h"
#include <cmath>

class AethelOpaPattern : public RixPattern {
public:
    AethelOpaPattern() {}
    virtual ~AethelOpaPattern() {}

    virtual int Init(RixContext *ctx, char const *pluginpath) { return 0; }
    virtual void Finalize(RixContext *ctx) {}

    virtual bool ComputeOutputParams(RixShadingContext const *sCtx,
                                     RtPointer instanceData,
                                     RixParameterList *params) 
    {
        // Retrieve shading context evaluation points (e.g., P coordinates)
        RtPoint3 const *P;
        sCtx->GetPrimVar(RixShadingContext::k_P, &P);

        // Retrieve uniform inputs
        float steeringAngle;
        float wavelength;
        params->GetParam(0, &steeringAngle);
        params->GetParam(1, &wavelength);

        // Output buffer pointers
        RtColorRGB *resultColor;
        params->GetOutputParam(0, (void **)&resultColor);

        bool const *micromask = sCtx->GetBuiltinVar(RixShadingContext::k_LpeMask);
        int npts = sCtx->numPts;

        sCtx->ParallelFor(0, npts, [=](int i) {
            float k = 6.28318530718 / wavelength;
            float spatial_projection = P[i].x * std::sin(steeringAngle);
            float phase_delay = std::fmod(k * spatial_projection, 6.28318530718);

            resultColor[i] = RtColorRGB(
                std::sin(phase_delay + 0.0) * 0.5f + 0.5f,
                std::sin(phase_delay + 2.094) * 0.5f + 0.5f,
                std::sin(phase_delay + 4.188) * 0.5f + 0.5f
            );
        });

        return true;
    }
};

// Factory methods required by RenderMan RIS
RIX_PLUGIN_MARK
START_CREATOR(AethelOpaPattern)
{
    return new AethelOpaPattern();
}
END_CREATOR(AethelOpaPattern)
