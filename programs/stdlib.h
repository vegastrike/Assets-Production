#include "config.h"

#define GAMMA_OFFSET 0.0
#define GAMMA_OFFSET2 (GAMMA_OFFSET*GAMMA_OFFSET)

#if DEGAMMA
vec4  degammac( in vec4 a ) { a.rgb *= a.rgb; return a; }
vec4  degamma( in vec4 a ) { return a*a; }
vec3  degamma( in vec3 a ) { return a*a; }
vec2  degamma( in vec2 a ) { return a*a; }
float degamma( in float a) { return a*a; }
#else
vec4  degammac( in vec4 a ) { return a; }
vec4  degamma( in vec4 a ) { return a; }
vec3  degamma( in vec3 a ) { return a; }
vec2  degamma( in vec2 a ) { return a; }
float degamma( in float a) { return a; }
#endif

#if REGAMMA
vec4  regammac( in vec4 a ) { a.rgb = sqrt(a.rgb+vec3(GAMMA_OFFSET2))-vec3(GAMMA_OFFSET); return a; }
vec4  regamma( in vec4 a ) { return sqrt(a+vec4(GAMMA_OFFSET2))-vec4(GAMMA_OFFSET); }
vec3  regamma( in vec3 a ) { return sqrt(a+vec3(GAMMA_OFFSET2))-vec3(GAMMA_OFFSET); }
vec2  regamma( in vec2 a ) { return sqrt(a+vec2(GAMMA_OFFSET2))-vec2(GAMMA_OFFSET); }
float regamma( in float a) { return sqrt(a+GAMMA_OFFSET2)-GAMMA_OFFSET; }
#else
vec4  regammac( in vec4 a ) { return a; }
vec4  regamma( in vec4 a ) { return a; }
vec3  regamma( in vec3 a ) { return a; }
vec2  regamma( in vec2 a ) { return a; }
float regamma( in float a) { return a; }
#endif

#if DEGAMMA_ENVIRONMENT
    #define degamma_env degammac
#else
    #define degamma_env 
#endif

#if DEGAMMA_SPECULAR
    #define degamma_spec degamma
#else
    #define degamma_spec
#endif

#if DEGAMMA_GLOW_MAP
    #define degamma_glow degammac
#else
    #define degamma_glow
#endif

#if DEGAMMA_LIGHTS
    #define degamma_light degammac
#else
    #define degamma_light
#endif

#if DEGAMMA_TEXTURES
    #define degamma_tex degamma
#else
    #define degamma_tex
#endif

vec4  sqr( in vec4 a )     { return a*a; }
vec3  sqr( in vec3 a )     { return a*a; }
vec2  sqr( in vec2 a )     { return a*a; }
float sqr( in float a )    { return a*a; }


float lerp(float a, float b, float t) { return a+t*(b-a); }
vec2 lerp(vec2 a, vec2 b, float t) { return a+t*(b-a); }
vec3 lerp(vec3 a, vec3 b, float t) { return a+t*(b-a); }
vec4 lerp(vec4 a, vec4 b, float t) { return a+t*(b-a); }

float  saturatef(float x) { return clamp(x,0.0,1.0); }
vec2   saturate(vec2 x) { return clamp(x,0.0,1.0); }
vec3   saturate(vec3 x) { return clamp(x,0.0,1.0); }
vec4   saturate(vec4 x) { return clamp(x,0.0,1.0); }

float fresnel(float fNDotV, float fresnelEffect)
{
   return sqr(1.0-lerp(0.0,fNDotV,fresnelEffect));
}

float  luma(vec3 color) { return dot( color, vec3(1.0/3.0, 1.0/3.0, 1.0/3.0) ); }

vec4 expand(vec4 x)   { return x*2.0-1.0; }
vec3 expand(vec3 x)   { return x*2.0-1.0; }
vec2 expand(vec2 x)   { return x*2.0-1.0; }
float  expand(float  x)   { return x*2.0-1.0; }

vec4 bias(vec4 x)     { return x*0.5+0.5; }
vec3 bias(vec3 x)     { return x*0.5+0.5; }
vec2 bias(vec2 x)     { return x*0.5+0.5; }
float  bias(float  x)     { return x*0.5+0.5; }

float  self_shadow(float x) { return (x>0.0)?1.0:0.0; }
float  self_shadow_smooth(float x) { return saturatef(2.0*x); }
float  self_shadow_smooth_ex(float x) { return saturatef(4.0*x); }

float soft_min(float m, float x)
{
   const float hpi_i = 0.63661977236758134307553505349006;
   return min(m,m*1.25*hpi_i*atan(x/m));
}



