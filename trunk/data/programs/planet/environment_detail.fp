#include "../fplod.h"

#include "earth_params.h"
#include "../config.h"
#include "../stdlib.h"

uniform sampler2D diffuseMap;
uniform samplerCube envMap;
uniform sampler2D specMap;
uniform sampler2D cloudMap;
uniform sampler2D cityMap;
uniform sampler2D cityDetail;
uniform sampler2D cosAngleToDepth_20;


vec3 ambientMapping( in vec3 direction, in float cloudmap )
{
   return degamma_env(textureCubeLod(envMap, direction, 8.0)).rgb * (1.0 - cloudmap);
}

vec3 specEnvMapping( in float shininess, in vec3 direction, in vec3 citymap, in float cloudmap ) //const
{
  float mipbias = max(0.0, 8.0 - shininess * shininess * 16.0);
  vec4 result = textureCubeLod( envMap, direction, mipbias );
  result = degamma_env(result);
  
  return lerp(result.rgb, citymap, cloudmap);
}

float fresnel(float fNDotV)
{
   return fresnel(fNDotV,fFresnelEffect.x);
}

float  cityLightTrigger(float fNDotL) { return clamp(4.0*(-fNDotL + fCityLightTriggerBias.x), 0.0, 1.0); }

float cosAngleToAlpha(float fNDotV)
{
   vec2 res = vec2(1.0) / vec2(1024.0,128.0);
   vec2 mn = res * 0.5;
   vec2 mx = vec2(1.0)-res * 0.5;
   return texture2D(cosAngleToDepth_20,clamp(vec2(fNDotV,fAtmosphereType),mn,mx)).a;
}

void main() 
{
  // Compute relevant vectors
  vec2 texcoord    = gl_TexCoord[0].xy;
  vec2 shadowcoord = gl_TexCoord[4].xy;
  vec2 refgndcoord = gl_TexCoord[5].xy;
  vec3 eye         = normalize(gl_TexCoord[3].xyz);
  vec3 diffusecol  = gl_Color.rgb;
  vec3 speccol     = gl_SecondaryColor.rgb;
  vec3 normal      = normalize(gl_TexCoord[1].xyz);
  vec3 lightpos    = normalize(gl_TexCoord[2].xyz);
  vec3 reflection  = normalize(-reflect(eye,normal));
  float cityLightFactor = fCloud_Dens_Thick_CLF_SSF.z;

  // Sample textures
  vec4 specmap     = texture2D(specMap, texcoord);
  vec4 diffusemap  = texture2D(diffuseMap, texcoord);
  vec4 citymap     = texture2DLod(cityMap, refgndcoord, 2.0);
  vec4 gcitymap    = texture2D(cityMap, texcoord);
  vec4 gcitydetail = texture2D(cityDetail, texcoord * 256.0);
  vec4 gcitydetail2= texture2D(cityDetail, texcoord * 1024.0);
  vec4 cloudmap    = texture2D(cloudMap, shadowcoord);
  cloudmap.a       = saturatef(cloudmap.a * fCloudLayerDensity);
  
  diffusemap.rgb   = degamma_tex(diffusemap.rgb);
  specmap.rgb      = degamma_tex(specmap.rgb);
  citymap.rgb      = degamma_tex(citymap.rgb);
  gcitymap.rgb     = degamma_tex(gcitymap.rgb);
  gcitydetail.rgb  = degamma_tex(gcitydetail.rgb);
  gcitydetail2.rgb = degamma_tex(gcitydetail2.rgb);

  // Compute specular factor
  float shininess  = fShininess.r * specmap.a;
  float fNDotV     = dot(normal, eye);
  float fNDotL     = dot(normal, lightpos);
  vec3 specular    = fresnel(fNDotV) * speccol * specmap.rgb;
  
  // Make citymap night-only
  vec3 trigger     = cityLightTrigger(fNDotL) * fvCityLightColor.rgb * cityLightFactor;
  citymap.rgb     *= trigger;
  gcitymap.rgb    *= trigger;

  float cityDetailAmount = 1.0 - gcitymap.a;
  float cityAmp;
  
  if (cityDetailAmount > 0.01) {
    gcitydetail += gcitydetail2 * 0.3;
    
    // Apply citymap detail
    float cityDetailAmp = dot(gcitydetail.rgb, vec3(1.0/3.0));
    float cityDetailOffset = sqr(1.0 - saturatef(dot(gcitymap.rgb, vec3(1.0/3.0))));
    float cityDetailScale  = saturatef(cityDetailAmp - 0.5) * 3.0 + 0.25;
    cityAmp = saturatef(cityDetailAmp - cityDetailOffset) * cityDetailScale;
    cityAmp = lerp(1.0, cityAmp, cityDetailAmount);
    gcitydetail.rgb = lerp(vec3(1.0), gcitydetail.rgb, cityDetailAmount);
  } else {
    cityAmp = 1.0;
    gcitydetail.rgb = vec3(1.0);
  }
  
  // degamma twice, it's a glowmap and we need a lot of precision near darkness
  gcitymap.rgb = sqr(gcitymap.rgb); 
  
  // Do lighting
  vec3 result;
  result = diffusecol * diffusemap.rgb * ambientMapping(normal, cloudmap.a) 
         + specEnvMapping(shininess, reflection, citymap.rgb * cloudmap.rgb, cloudmap.a) * specular
         + gcitymap.rgb * gcitydetail.rgb * cityAmp;
  
  // Do silhouette alpha
  float  alpha     = saturatef(2.0 * (cosAngleToAlpha(fNDotV) - 0.5));
  
  // re-gamma and return
  gl_FragColor.a = diffusemap.a * alpha;
  gl_FragColor.rgb = regamma(result * alpha);
}
