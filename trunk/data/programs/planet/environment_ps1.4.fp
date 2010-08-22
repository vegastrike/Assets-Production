uniform sampler2D diffuseMap;
uniform samplerCube envMap;
uniform sampler2D specMap;
uniform sampler2D cloudMap;
uniform sampler2D cityMap;
uniform sampler2D cosAngleToDepth_20;

uniform vec4 envColor;
uniform vec4 fShininess;
uniform vec4 fFresnelEffect;
uniform vec4 fAtmosphereExtrusion;
uniform vec4 fCloud_Dens_Thick_CLF_SSF;
uniform vec4 fvCityLightColor;
uniform vec4 fCityLightTriggerBias;

uniform vec4 fAtmosphereType_Thickness_Contrast_LAOffs; 
    //type indexes the t coordinate on cosAngleToDepth, cosAngleToAbsorption, cosAngleToScatter
    //thickness scales cosAngleToDepth
    //contrast is a lighting parameter

#define fAtmosphereType fAtmosphereType_Thickness_Contrast_LAOffs.x
#define fAtmosphereThickness fAtmosphereType_Thickness_Contrast_LAOffs.y
#define fAtmosphereContrast fAtmosphereType_Thickness_Contrast_LAOffs.z
#define fAtmosphereAbsorptionOffset fAtmosphereType_Thickness_Contrast_LAOffs.w



/**********************************/
//  CUSTOMIZATION  (EDITABLE)
/**********************************/
#define SHININESS_FROM       GLOSS_IN_SPEC_ALPHA
#define NORMALMAP_TYPE       CINEMUT_NM
#define DEGAMMA              1
#define DEGAMMA_ENVIRONMENT  1
#define DEGAMMA_TEXTURES     1
#define SANITIZE             0
/**********************************/


#if DEGAMMA
vec4  degamma( in vec4 a ) { return a*a; }
vec3  degamma( in vec3 a ) { return a*a; }
float degamma( in float a) { return a*a; }
vec4  regamma( in vec4 a ) { return sqrt(a); }
vec3  regamma( in vec3 a ) { return sqrt(a); }
float regamma( in float a) { return sqrt(a); }
#else
vec4  degamma( in vec4 a ) { return a; }
vec3  degamma( in vec3 a ) { return a; }
float degamma( in float a) { return a; }
vec4  regamma( in vec4 a ) { return a; }
vec3  regamma( in vec3 a ) { return a; }
float regamma( in float a) { return a; }
#endif

#if DEGAMMA_ENVIRONMENT
    #define degamma_env degamma
#else
    #define degamma_env 
#endif

#if DEGAMMA_TEXTURES
    #define degamma_tex degamma
#else
    #define degamma_tex
#endif


float lerp(float a, float b, float t) { return a+t*(b-a); }
vec2 lerp(vec2 a, vec2 b, float t) { return a+t*(b-a); }
vec3 lerp(vec3 a, vec3 b, float t) { return a+t*(b-a); }
vec4 lerp(vec4 a, vec4 b, float t) { return a+t*(b-a); }

float  saturatef(float x) { return clamp(x,0.0,1.0); }
vec2   saturate(vec2 x) { return clamp(x,0.0,1.0); }
vec3   saturate(vec3 x) { return clamp(x,0.0,1.0); }
vec4   saturate(vec4 x) { return clamp(x,0.0,1.0); }

vec3 ambientMapping( in vec3 direction, in float cloudmap )
{
   return gl_LightSource[0].ambient * (1.0 - cloudmap);
}

vec3 specEnvMapping( in float shininess, in vec3 direction, in float cloudmap ) //const
{
  float mipbias = max(0.0, 8.0 - shininess * shininess * 16.0);
  vec3 result = textureCube( envMap, direction, mipbias ).rgb;
  result = degamma_env(result);
  
  return result * (1.0 - cloudmap);
}

float fresnel(float fNDotV)
{
   return degamma(1.0-lerp(0.0,fNDotV,fFresnelEffect.x));
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
  vec4 gcitymap    = texture2D(cityMap, texcoord);
  float cloudmap   = texture2D(cloudMap, shadowcoord).a;
  
  diffusemap.rgb   = degamma_tex(diffusemap.rgb);
  specmap.rgb      = degamma_tex(specmap.rgb);
  gcitymap.rgb     = degamma_tex(gcitymap.rgb);
  gcitymap.rgb     = degamma_tex(gcitymap.rgb); // degamma twice, it's  glowmap and we need a lot of precision near darkness
  
  // Compute specular factor
  float shininess  = fShininess.r * specmap.a;
  float fNDotV     = dot(normal, eye);
  float fNDotL     = dot(normal, lightpos);
  vec3 specular    = fresnel(fNDotV) * speccol * specmap.rgb;
  
  // Make citymap night-only
  float trigger    = cityLightTrigger(fNDotL) * fvCityLightColor.rgb * cityLightFactor;
  gcitymap.rgb    *= trigger;

  // Do lighting
  vec3 result;
  result = diffusecol * diffusemap.rgb * ambientMapping(normal, cloudmap) 
         + specEnvMapping(shininess, reflection, cloudmap) * specular
         + gcitymap.rgb;
  
  // Do silhouette alpha
  float  alpha     = saturatef(2.0 * (cosAngleToAlpha(fNDotV) - 0.5));
  
  // re-gamma and return
  gl_FragColor.a = diffusemap.a * alpha;
  gl_FragColor.rgb = regamma(result * alpha);
}
