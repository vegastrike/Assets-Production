
varying vec3 varTSLight;
varying vec3 varTSView;
varying vec3 varWSNormal;

uniform vec4 fGroundContrast_SelfShadowFactor_MinMaxScatterFactor;

#define fGroundContrast fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.x
#define fSelfShadowFactor fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.y
#define fMinScatterFactor fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.z
#define fMaxScatterFactor fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.w

uniform vec4 fAtmosphereExtrusionType_Thickness_Contrast_LAOffs; 
    //type indexes the t coordinate on cosAngleToDepth, cosAngleToAbsorption, cosAngleToScatter
    //thickness scales cosAngleToDepth
    //contrast is a lighting parameter

#define fAtmosphereType fAtmosphereExtrusionType_Thickness_Contrast_LAOffs.x
#define fAtmosphereThickness fAtmosphereExtrusionType_Thickness_Contrast_LAOffs.y
#define fAtmosphereContrast fAtmosphereExtrusionType_Thickness_Contrast_LAOffs.z
#define fAtmosphereAbsorptionOffset fAtmosphereExtrusionType_Thickness_Contrast_LAOffs.w

uniform vec4 fAtmosphereAbsorptionColor;
uniform vec4 fAtmosphereScatterColor;

uniform vec4 fReyleighRate_Amount;

#define fReyleighRate fReyleighRate_Amount.x
#define fReyleighAmount fReyleighRate_Amount.y

uniform vec4 fAtmosphereExtrusionNDLScaleOffsSteepThick;

#define fAtmosphereExtrusionNDLScaleOffs fAtmosphereExtrusionNDLScaleOffsSteepThick.xy
#define fAtmosphereExtrusionSteepness fAtmosphereExtrusionNDLScaleOffsSteepThick.z
#define fAtmosphereExtrusionThickness fAtmosphereExtrusionNDLScaleOffsSteepThick.w

uniform sampler2D cosAngleToDepth_20;
uniform samplerCube envMap;

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

vec4 degamma_glow(vec4 glow)
{
    glow.rgb = degamma_tex(degamma_tex(glow.rgb));
    return glow;
}


float lerp(float a, float b, float t) { return a+t*(b-a); }
vec2 lerp(vec2 a, vec2 b, float t) { return a+t*(b-a); }
vec3 lerp(vec3 a, vec3 b, float t) { return a+t*(b-a); }
vec4 lerp(vec4 a, vec4 b, float t) { return a+t*(b-a); }


float  saturatef(float x) { return clamp(x,0.0,1.0); }
vec2   saturate(vec2 x) { return clamp(x,0.0,1.0); }
vec3   saturate(vec3 x) { return clamp(x,0.0,1.0); }
vec4   saturate(vec4 x) { return clamp(x,0.0,1.0); }

float  luma(vec3 color) { return dot( color, vec3(1.0/3.0, 1.0/3.0, 1.0/3.0) ); }
float  sqr(float x)       { return x*x; }
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
float  cityLightTrigger(float fNDotLB) { return saturatef(4.0*fNDotLB); }
float  self_shadow_smooth_ex(float x) { return saturatef(4.0*x); }


float cosAngleToAlpha(float fNDotV)
{
   vec2 res = vec2(1.0) / vec2(1024.0,128.0);
   vec2 mn = res * 0.5;
   vec2 mx = vec2(1.0)-res * 0.5;
   return texture2D(cosAngleToDepth_20,clamp(vec2(fNDotV,fAtmosphereType),mn,mx)).a;
}

float soft_min(float m, float x)
{
   const float hpi_i = 0.63661977236758134307553505349006;
   return min(m,m*1.25*hpi_i*atan(x/m));
}

float  atmosphereLighting(float fNDotL) { return saturatef(soft_min(1.0,2.0*fAtmosphereContrast*fNDotL)); }
float  groundLighting(float fNDotL) { return saturatef(soft_min(1.0,2.0*fGroundContrast*fNDotL)); }

float scaleAndOffset(float v)
{
   return saturatef( dot(vec2(v,1.0), fAtmosphereExtrusionNDLScaleOffs) );
}

vec4 atmosphericScatter(vec4 ambient, float fNDotV, float fNDotL, float fLDotV)
{
   float ralpha = cosAngleToAlpha(fNDotV);
   vec4 rv;
   rv.rgb = regamma(ambient + atmosphereLighting(scaleAndOffset(fNDotL))*1.414*fAtmosphereScatterColor.rgb );
   rv.a = ralpha;
   return rv;
}

void main()
{      
   vec3 L = normalize(varTSLight);
   vec3 V = normalize(varTSView);
   
   vec4 rv = atmosphericScatter( gl_LightSource[0].ambient, V.z, L.z, dot(L,V) );
   gl_FragColor.rgb = (rv.rgb);
   gl_FragColor.a = rv.a;
}


