uniform int light_enabled[gl_MaxLights];
uniform int max_light_enabled;
uniform sampler2D diffuseMap;
uniform sampler2D envMap;
uniform sampler2D specMap;
uniform sampler2D glowMap;
uniform sampler2D normalMap;
uniform sampler2D damageMap;
uniform sampler2D detail0Map;
uniform sampler2D detail1Map;
uniform vec4 cloaking;
uniform vec4 damage;
uniform vec4 envColor;

vec3 matmul(vec3 tangent, vec3 binormal, vec3 normal,vec3 lightVec) {
  return vec3(dot(lightVec,tangent),dot(lightVec,binormal),dot(lightVec,normal));
}
vec3 imatmul(vec3 tangent, vec3 binormal, vec3 normal,vec3 lightVec) {
  return lightVec.xxx*tangent+lightVec.yyy*binormal+lightVec.zzz*normal;
}

vec2 EnvMapGen(vec3 f) {
   float fzp1=f.z+1.0;
   float m=2.0*sqrt(f.x*f.x+f.y*f.y+(fzp1)*(fzp1));
   return vec2(f.x/m+.5,f.y/m+.5);
}

float bias(float f){ return f*0.5+0.5; }
vec2  bias(vec2 f) { return f*0.5+vec2(0.5); }
vec3  bias(vec3 f) { return f*0.5+vec3(0.5); }
vec4  bias(vec4 f) { return f*0.5+vec4(0.5); }

float expand(float f){ return f*2.0-1.0; }
vec2  expand(vec2 f) { return f*2.0-vec2(1.0); }
vec3  expand(vec3 f) { return f*2.0-vec3(1.0); }
vec4  expand(vec4 f) { return f*2.0-vec4(1.0); }

float lerp(float f, float a, float b){return (1.0-f)*a+f*b; }
vec2  lerp(float f, vec2 a, vec2 b) { return (1.0-f)*a+f*b; }
vec3  lerp(float f, vec3 a, vec3 b) { return (1.0-f)*a+f*b; }
vec4  lerp(float f, vec4 a, vec4 b) { return (1.0-f)*a+f*b; }

float shininessMap(float shininess, vec4 specmap) // luma-based shininess modulation
{
  vec3 temp = specmap.rgb;
  temp *= specmap.rgb;
  temp *= temp;
  return clamp( dot(temp.rg,vec2(0.5))*shininess, 1.0, 255.0 );
}

float shininess2Lod(float shininess) { return max(0.0,7.0-log2(shininess+1.0)); }

float limited_shininessMap(float shininess, vec4 specmap)
{
  float limit = 50.0; //50^2 is 2500. 2500*0.001 = 2.5 --enough risk of saturation!
  float shine = shininessMap(shininess,specmap);
  return (shine*limit)/(shine+limit);
}

float shininess_to_brightness(float shininess)
{
  return 0.001 * shininess * shininess;
}

float lightspot_brightness( float shininess, vec4 specmap )
{
  return limited_shininessMap( shininess, specmap ) * shininess_to_brightness( shininess );
}

float selfshadowStep(float NdotL)
{
  float s = clamp(1.0 - NdotL, 0.0, 1.0);
  s *= s;
  s *= s;
  s *= s;
  return clamp(1.0 - s, 0.0, 1.0);
}

void lightingLight(
   in vec3 light, in vec3 normal, in vec3 vnormal, in vec3 eye, in vec3 reflection, 
   in vec4 lightDiffuse, in float lightAtt, 
   in vec4 diffusemap, in vec4 specmap, in float shininess,
   in vec4 ambientProduct,
   inout vec3 diffuse, inout vec3 specular)
{
   float VNdotL = 4.0 * dot(vnormal,light);
   float selfshadow = selfshadowStep(VNdotL);
   float NdotL = clamp( dot(normal,light), 0.0, VNdotL );
   float RdotL = clamp( dot(reflection,light), 0.0, VNdotL );
   specular += ( pow( RdotL, lightspot_brightness(shininess,specmap)) * lightDiffuse.rgb * lightAtt * selfshadow );
   diffuse  += ( NdotL * lightDiffuse.rgb * lightAtt * selfshadow );
}

#define lighting(name, lightno_gl, lightno_tex) \
void name( \
   in vec3 normal, in vec3 vnormal, in vec3 eye, in  vec3 reflection, \
   in vec4 diffusemap, in vec4 specmap, \
   inout vec3 diffuse, inout vec3 specular) \
{ \
   lightingLight( \
      normalize(gl_TexCoord[lightno_tex].xyz), normal, vnormal, eye, reflection, \
      gl_FrontLightProduct[lightno_gl].diffuse, \
      gl_TexCoord[lightno_tex].w, \
      diffusemap, specmap, gl_FrontMaterial.shininess, \
      gl_FrontLightProduct[lightno_gl].ambient, \
      diffuse, specular); \
}

lighting(lighting0, 0, 5)
lighting(lighting1, 1, 6)

vec3 lightingClose(in vec3 diffuse, in vec3 specular, in vec4 diffusemap, in vec4 specmap)
{
   return (diffuse*diffusemap.rgb) + (specular*specmap.rgb);
}

vec3 envMapping(in vec3 reflection, in float gloss, in vec4 specmap)
{
   float envLod = shininess2Lod(gloss);//shininessMap(shininess,specmap));
   return texture2DLod(envMap, EnvMapGen(reflection), envLod).rgb * specmap.rgb * envColor.rgb * 2.0;
}

void main() 
{
  // Retrieve normals
  vec3 iNormal=gl_TexCoord[1].xyz;
  vec3 iTangent=gl_TexCoord[2].xyz;
  vec3 iBinormal=gl_TexCoord[3].xyz;
  vec3 vnormal=iNormal;
  //vec3 normal=normalize(imatmul(iTangent,iBinormal,iNormal,expand(texture2D(normalMap,gl_TexCoord[0].xy).yxz)*vec3(-1.0,1.0,1.0)));
  vec3 normal=normalize(imatmul(iTangent,iBinormal,iNormal,expand(texture2D(normalMap,gl_TexCoord[0].xy).wyz)));
  
  // Other vectors
  vec3 eye = gl_TexCoord[4].xyz;
  vec3 reflection = -reflect(eye,normal);
  
  // Init lighting accumulators
  vec3 diffuse = gl_Color.rgb;
  vec3 specular= gl_SecondaryColor.rgb;
  
  // Sample textures
  vec4 diffusecolor= texture2D(diffuseMap, gl_TexCoord[0].xy);
  vec4 damagecolor = texture2D(damageMap , gl_TexCoord[0].xy);
  vec4 speccolor   = texture2D(specMap   , gl_TexCoord[0].xy);
  vec4 glowcolor   = texture2D(glowMap   , gl_TexCoord[0].xy);
  
  //sanity enforcement:
  //float temp = 1.0 - max( diffusecolor.r, max( diffusecolor.g, diffusecolor.b ) );
  //speccolor.r = min( speccolor.r, temp );
  //speccolor.g = min( speccolor.g, temp );
  //speccolor.b = min( speccolor.b, temp );
  
  //Fresnel:
  float alpha = diffusecolor.a * gl_FrontMaterial.diffuse.a;
  float fresnel_alpha = 1.0 - clamp( dot( eye, normal ), 0.0, 1.0 );
  alpha *= alpha;
  fresnel_alpha *= fresnel_alpha;
  alpha *= alpha;

  vec4 diffusemap  = lerp(damage.x, diffusecolor, damagecolor);
  vec4 specmap     = speccolor;
  float specdamage = clamp(1.0 - dot(damagecolor.xyz,vec3(1.0/3.0)) * damage.x * 2.0, 0.0, 1.0);
  specmap.rgb     *= specdamage;
  specmap.a       *= bias(specdamage);
  float gloss      = shininessMap(gl_FrontMaterial.shininess,specmap);
  
  fresnel_alpha = clamp( 0.0625 + ( 0.9375 * fresnel_alpha ), alpha, 1.0 );
  fresnel_alpha = 1.0-fresnel_alpha;
  fresnel_alpha *= fresnel_alpha; //to account for inner surface reflection
  fresnel_alpha = 1.0-fresnel_alpha;

  // Do lighting for every active light
  if (light_enabled[0] != 0)
     lighting0(normal, vnormal, eye, reflection, diffusemap, specmap, diffuse, specular);
  if (light_enabled[1] != 0)
     lighting1(normal, vnormal, eye, reflection, diffusemap, specmap, diffuse, specular);

  vec4 result;
  specular *= fresnel_alpha;

  result.a = diffusemap.a;
  result.rgb  = lightingClose(diffuse, specular, diffusemap, specmap)
              + glowcolor.rgb
              + (envMapping(reflection,gloss,specmap)*fresnel_alpha);
  result *= cloaking.rrrg;
  gl_FragColor = result;
}
