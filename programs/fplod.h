#include "config.h"

#ifndef GL_NV_fragment_program2
#extension GL_ARB_shader_texture_lod : enable

#ifndef GL_ARB_shader_texture_lod
#define GL_ARB_shader_texture_lod 0
#endif

#if (GL_ARB_shader_texture_lod == 0)
#extension GL_ATI_shader_texture_lod : enable

#ifndef GL_ATI_shader_texture_lod
#define GL_ATI_shader_texture_lod 0
#endif

#if (GL_ATI_shader_texture_lod == 0)
#define NO_TEXTURE_LOD 1
#endif

#endif

#endif


#ifdef NO_TEXTURE_LOD

vec4 texture1DLod(sampler1D sampler, float P, float lod)
{
    // Turn into bias
    return texture1D(sampler, P, lod);
}

vec4 texture2DLod(sampler2D sampler, vec2 P, float lod)
{
    // Turn into bias
    return texture2D(sampler, P, lod);
}

vec4 texture3DLod(sampler3D sampler, vec3 P, float lod)
{
    // Turn into bias
    return texture3D(sampler, P, lod);
}

vec4 textureCubeLod(samplerCube sampler, vec3 P, float lod)
{
    // Turn into bias
    return textureCube(sampler, P, lod);
}

vec4 texture1DGradARB(sampler1D sampler, float P, float dPdx, float dPdy)
{
    return texture1D(sampler, P);
}

vec4 texture2DGradARB(sampler2D sampler, vec2 P, vec2 dPdx, vec2 dPdy)
{
    return texture2D(sampler, P);
}

vec4 texture3DGradARB(sampler3D sampler, vec3 P, vec3 dPdx, vec3 dPdy)
{
    return texture3D(sampler, P);
}

vec4 textureCubeGradARB(samplerCube sampler, vec3 P, vec3 dPdx, vec3 dPdy)
{
    return textureCube(sampler, P);
}

#endif
