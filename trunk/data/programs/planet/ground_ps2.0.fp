uniform vec4 fvCityLightColor;
uniform vec4 fvShadowColor;
uniform vec4 fCityLightTriggerBias;
uniform vec4 fShininess;
uniform vec4 fFresnelEffect;
uniform vec4 fGroundContrast_SelfShadowFactor_MinMaxScatterFactor;

#define fGroundContrast fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.x
#define fSelfShadowFactor fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.y
#define fMinScatterFactor fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.z
#define fMaxScatterFactor fGroundContrast_SelfShadowFactor_MinMaxScatterFactor.w

uniform vec4 fAtmosphereType_Thickness_Contrast_LAOffs; 
    //type indexes the t coordinate on cosAngleToDepth, cosAngleToAbsorption, cosAngleToScatter
    //thickness scales cosAngleToDepth
    //contrast is a lighting parameter

#define fAtmosphereType fAtmosphereType_Thickness_Contrast_LAOffs.x
#define fAtmosphereThickness fAtmosphereType_Thickness_Contrast_LAOffs.y
#define fAtmosphereContrast fAtmosphereType_Thickness_Contrast_LAOffs.z
#define fAtmosphereAbsorptionOffset fAtmosphereType_Thickness_Contrast_LAOffs.w

uniform vec4  fAtmosphereAbsorptionColor;
uniform vec4  fAtmosphereScatterColor;
uniform vec4  fAtmosphereShadowInfluence;
uniform vec4  fReyleighRate_Amount;

#define fReyleighRate fReyleighRate_Amount.x
#define fReyleighAmount fReyleighRate_Amount.y

uniform vec4 fAtmosphereExtrusion;
uniform vec4 fvCloudLayerDrift_ShadowRelHeight;
uniform vec4 fCloud_Dens_Thick_CLF_SSF;

#define fCloudLayerDensity      fCloud_Dens_Thick_CLF_SSF.x
#define fCloudLayerThickness    fCloud_Dens_Thick_CLF_SSF.y
#define fCityLightFactor        fCloud_Dens_Thick_CLF_SSF.z
#define fCloudSelfShadowFactor  fCloud_Dens_Thick_CLF_SSF.w

uniform vec4 fBumpScale;

uniform sampler2D specularMap_20;
uniform sampler2D baseMap_20;
uniform sampler2D cityLights_20;
uniform sampler2D cosAngleToDepth_20;
uniform sampler2D cloudMap_20;
uniform sampler2D noiseMap_20;
uniform sampler2D normalMap_20;


varying vec3 varTSLight;
varying vec3 varTSView;


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

float fresnel(float fNDotV)
{
   return degamma(1.0-lerp(0.0,fNDotV,fFresnelEffect.x));
}

float expandPrecision(vec4 src)
{
   return dot(src,(vec4(1.0,256.0,65536.0,0.0)/131072.0));
}

float cosAngleToDepth(float fNDotV)
{
   vec2 res = vec2(1.0) / vec2(1024.0,128.0);
   vec2 mn = res * 0.5;
   vec2 mx = vec2(1.0)-res * 0.5;
   return expandPrecision(texture2DLod(cosAngleToDepth_20,clamp(vec2(fNDotV,fAtmosphereType),mn,mx),0.0)) * fAtmosphereThickness;
}

float cosAngleToAlpha(float fNDotV)
{
   vec2 res = vec2(1.0) / vec2(1024.0,128.0);
   vec2 mn = res * 0.5;
   vec2 mx = vec2(1.0)-res * 0.5;
   return texture2D(cosAngleToDepth_20,clamp(vec2(fNDotV,fAtmosphereType),mn,mx)).a;
}

float soft_min(float m, float x)
{
   return min(m,x);
}

float  atmosphereLighting(float fNDotL) { return saturatef(soft_min(1.0,2.0*fAtmosphereContrast*fNDotL)); }
float  groundLighting(float fNDotL) { return saturatef(soft_min(1.0,2.0*fGroundContrast*fNDotL)); }

vec4 atmosphericScatter(vec4 dif, float fNDotV, float fNDotL, float fVDotL, vec3 fvShadow)
{
   float  vdepth     = cosAngleToDepth(fNDotV);
   float  ldepth     = cosAngleToDepth(fNDotL+fAtmosphereAbsorptionOffset);
   float  alpha      = saturatef(2.0 * (cosAngleToAlpha(fNDotV) - 0.5));
   
   vec3  labsorption = pow(fAtmosphereAbsorptionColor.rgb,vec3(fAtmosphereAbsorptionColor.a*ldepth));
   vec3  vabsorption = pow(fAtmosphereAbsorptionColor.rgb,vec3(fAtmosphereAbsorptionColor.a*vdepth));
   vec3  lscatter    = gl_LightSource[0].diffuse.rgb 
                       * fAtmosphereScatterColor.rgb 
                       * pow(labsorption,vec3(fSelfShadowFactor)) 
                       * (fMinScatterFactor+soft_min(fMaxScatterFactor-fMinScatterFactor,vdepth));
   
   vec4 rv;
   rv.rgb = regamma( (dif.rgb*labsorption*fvShadow)*vabsorption 
                  + atmosphereLighting(fNDotL)
                    *lscatter );
   rv.a = dif.a * alpha;
   return rv;
}

void main()
{      
   vec2 texcoord = gl_TexCoord[0].xy;
   vec4 shadowcoord = gl_TexCoord[1];
   
   vec3 L = normalize(varTSLight);
   vec3 V = normalize(varTSView);
   vec3 tN = expand( texture2D( normalMap_20, texcoord ).rgb ) * vec3(-1.0,1.0,1.0); // Do not normalize, to avoid aliasing
   
   vec2 noise = expand( texture2D( noiseMap_20, texcoord * fBumpScale.y ).xy );
   vec3 dN = normalize( vec3( noise * fBumpScale.z, 1 ) ) - vec3(0.0,0.0,1.0);
   vec3 N = dN + tN;
   
   vec3 R = -reflect(L,N);
   
   float  fNDotL           = saturatef( dot(N,L) ); 
   float  fNDotLs          = saturatef( L.z ); 
   float  fNDotLf          = L.z; 
   float  fNDotLB          = saturatef(-L.z + fCityLightTriggerBias.x);
   float  fRDotV           = saturatef( dot(R,V) );
   float  fNDotV           = saturatef( dot(N,V) );
   float  fNDotVs          = saturatef( V.z );
   float  fVDotL           = dot(L,V);
   
   vec4 fvTexColor         = texture2D( baseMap_20, texcoord );
   fvTexColor.rgb          = degamma_tex(fvTexColor.rgb);
   
   vec4 cnoise             = texture2D(noiseMap_20,gl_TexCoord[2].xy);
   vec3 fvDrift            = fvCloudLayerDrift_ShadowRelHeight.zzw*(cnoise.xyw * 0.25 + cnoise.aaa * 0.75 - vec3(0.0,0.0,0.5)) + vec3(0.0,0.0,1.0);
   shadowcoord            += fvDrift.xyxy;
   
   float  fGShadow         = texture2D( cloudMap_20, shadowcoord.xy ).a;
   fGShadow               *= fvDrift.z*fCloudLayerDensity;
   
   vec3 fvGShadow          = lerp( vec3(1.0), fvShadowColor.rgb, fGShadow );
   
   vec4 fvSpecular         = degamma_tex(texture2D( specularMap_20, texcoord ));
   fvSpecular.rgb         *= fresnel(fNDotV);
   fRDotV                  = pow( fRDotV, fShininess.x*(0.01+0.99*fvSpecular.a)*256.0 );
   fvSpecular              = fvSpecular * gl_SecondaryColor * fRDotV;

   vec4 fvBaseColor;
   fvBaseColor.rgb         = gl_Color.rgb * groundLighting(fNDotL) * self_shadow(fNDotLs);
   fvBaseColor.a           = gl_Color.a;
   
   vec4 fvCityLights       = degamma_glow(texture2D( cityLights_20, texcoord )) * cityLightTrigger(fNDotLB) * fvCityLightColor;
   vec4 dif                = fvBaseColor * fvTexColor;
   vec4 spec               = 4.0*fvSpecular*self_shadow_smooth_ex(fNDotLs);

   gl_FragColor = atmosphericScatter( dif+spec, fNDotVs, fNDotLs, fVDotL, fvGShadow );
}


