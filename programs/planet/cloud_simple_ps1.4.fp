#include "earth_params.h"
#include "../config.h"
#include "../stdlib.h"

#define inCloudCoord gl_TexCoord[0]
#define inGroundCoord gl_TexCoord[1]
#define inShadowCoord gl_TexCoord[2]
#define inNoiseCoord gl_TexCoord[3]

varying vec3 varTSLight;
varying vec3 varTSView;
varying vec3 varWSNormal;
varying vec3 varScatter;
varying vec3 varCloudLayerDensitySVC;

uniform sampler2D cosAngleToDepth_20;
uniform sampler2D cloudMap_20;
uniform sampler2D noiseMap_20;
uniform sampler2D cityLights_20;
uniform samplerCube envMap;


float  atmosphereLighting(float fNDotL) { return saturatef(min(1.0,2.0*fAtmosphereContrast*fNDotL)); }
float  groundLighting(float fNDotL) { return saturatef(min(1.0,2.0*fGroundContrast*fNDotL)); }

vec4 atmosphericScatter(vec4 dif, float fNDotV, float fNDotL, float fVDotL)
{
   vec4 rv;
   rv.rgb = regamma( dif.rgb + varScatter );
   rv.a = dif.a;
   return rv;
}


void main()
{    
   vec2 CloudCoord = inCloudCoord.xy;
   vec2 GroundCoord = inGroundCoord.xy;
   vec2 ShadowCoord = inShadowCoord.xy;
   vec2 NoiseCoord = inNoiseCoord.xy;

   vec3 L = normalize(varTSLight);
   vec3 V = normalize(varTSView);
   vec3 N = varWSNormal;
   
   float  fNDotL           = saturatef( L.z ); 
   float  fNDotV           = saturatef( V.z );
   float  fVDotL           = dot(L, V);

   // Attack angle density adjustment   
   vec3 CloudLayerDensitySVC  = varCloudLayerDensitySVC;
  
   // Sample cloudmap
   vec2 gc1              =      CloudCoord                                         ;
   vec2 gc4              = lerp(CloudCoord,GroundCoord,0.75 * fCloudLayerThickness);
   vec4 fvCloud1         = texture2D( cloudMap_20, gc1 );
   vec4 fvCloud4         = texture2D( cloudMap_20, gc4 );
   
   vec2 sc4              = lerp(gc4,ShadowCoord,0.75 * fCloudLayerThickness);
   float  fCloudShadow4  = texture2D( cloudMap_20, sc4, 1.5 ).a;
   
   // Mask heights
   fvCloud1.a            = saturatef((fvCloud1.a-0.5000)*1.0); // 0.5000 - 1.0000
   fvCloud4.a            = saturatef((fvCloud4.a       )*2.0); // 0.0000 - 0.5000
   
   // Simplified for ps2.a
   const vec2 shadowStep4 = vec2(0.125, 0.708);
   fCloudShadow4          = saturatef( (fCloudShadow4 - shadowStep4) * 0.75 );
   
   // Compute self-shadowed cloud color
   vec4 fvBaseColor        = gl_Color;
   vec3 fvCloud1s,fvCloud4s;
   vec4 fvCloud;
   fvCloud1s               = fvCloud1.rgb;
   fvCloud4s               = fvCloud4.rgb*lerp(vec3(1.0),fvCloudSelfShadowColor.rgb,saturatef(fCloudShadow4*CloudLayerDensitySVC.x));
   fvCloud.a               = fvBaseColor.a*dot(fvCloudLayerMix,vec4(fvCloud1.a,fvCloud1.a,fvCloud4.a,fvCloud4.a));
   fvCloud.rgb             = fvCloud4s;
   fvCloud.rgb             = lerp(fvCloud.rgb,fvCloud1s,saturatef(fvCloud1.a*CloudLayerDensitySVC.y));
   fvCloud.rgb            *= fvBaseColor.rgb;

   gl_FragColor = atmosphericScatter( fvCloud, fNDotV, fNDotL, fVDotL );
}

