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

/*
float shininessMap(float shininess, vec4 spec_col) // alpha-based shininess modulation
{
  float result = clamp(spec_col.a*shininess,1.0,255.0);
  return result * result;
}
*/ 
float shininessMap(float shininess, vec3 spec_col) // luma-based shininess modulation
{
  vec3 temp = spec_col.rgb;
  temp *= spec_col.rgb;
  temp *= spec_col.rgb;
  temp *= spec_col.rgb;
  temp.b = (temp.r+temp.g)*0.5;
  return clamp( temp.b*shininess, 1.0, 255.0 );
}

float limited_shininessMap(float shininess, vec3 spec_col)
{
  float shine = shininessMap(shininess,spec_col);
  float limit = 30.0; //50^2 is 2500. 2500*0.001 = 2.5 --enough risk of saturation!
  return (shine*limit)/(shine+limit);
}

float shininess2Lod(float shininess) { return max(0.0,7.0-log2(shininess+1.0)); }

float shininess_to_brightness(float shininess)
{
  return 0.001 * shininess * shininess;
}

float lightspot_brightness( float shininess, vec3 spec_col )
{
  return limited_shininessMap( shininess, spec_col ) * shininess_to_brightness( shininess );
}

void lightingLight(
   in vec3 light, in vec3 normal, in vec3 vnormal, in vec3 eye, in vec3 reflection, 
   in vec4 lightDiffuse, in float lightAtt, 
   in vec4 diffusemap, in vec3 spec_col, in float shininess,
   in vec4 ambientProduct,
   inout vec3 diffuse, inout vec3 specular)
{
   float VNdotLx4= clamp( 4.0 * dot(vnormal,light), 0.0, 1.0 );
   float NdotL = clamp( dot(normal,light), -1.0, VNdotLx4 );
   float RdotL = clamp( dot(reflection,light), 0.0, VNdotLx4 );
   float s = 1.0 - (NdotL*NdotL); //soft penumbra stuff
   //float selfshadow = selfshadowStep(VNdotL); // <-***** removed
   float temp = clamp( NdotL - (0.94 * s * s * s * s * NdotL) + 0.005, 0.0, 1.01 ); //soft penumbra
   specular += ( pow( RdotL, lightspot_brightness(shininess,spec_col)) * lightDiffuse.rgb ); //* lightAtt );
   diffuse  += ( temp * lightDiffuse.rgb ); //* lightAtt );
}

#define lighting(name, lightno_gl, lightno_tex) \
void name( \
   in vec3 normal, in vec3 vnormal, in vec3 eye, in  vec3 reflection, \
   in vec4 diffusemap, in vec3 spec_col, \
   inout vec3 diffuse, inout vec3 specular) \
{ \
   lightingLight( \
      normalize(gl_TexCoord[lightno_tex].xyz), normal, vnormal, eye, reflection, \
      gl_FrontLightProduct[lightno_gl].diffuse, \
      gl_TexCoord[lightno_tex].w, \
      diffusemap, spec_col, gl_FrontMaterial.shininess, \
      gl_FrontLightProduct[lightno_gl].ambient, \
      diffuse, specular); \
}

lighting(lighting0, 0, 5)
lighting(lighting1, 1, 6)

vec3 lightingClose(in vec3 diffuse, in vec3 specular, in vec4 diffusemap, in vec3 spec_col )
{
   return (diffuse*diffusemap.rgb) + (specular*spec_col);
}

vec3 envMapping(in vec3 reflection, in float gloss, in vec3 spec_col)
{
   float envLod = shininess2Lod(gloss);//shininessMap(shininess,spec_col));
   return texture2DLod(envMap, EnvMapGen(reflection), envLod).rgb * spec_col * vec3(2.0);
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
  vec3 diffuse = vec3(0.0);
  vec3 specular= vec3(0.0);
  
  // Sample textures
  vec4 damagecolor = texture2D(damageMap , gl_TexCoord[0].xy);
  vec4 diffusecolor= texture2D(diffuseMap, gl_TexCoord[0].xy);
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
  //fresnel_alpha *= fresnel_alpha;

  vec4 diffusemap  = lerp(damage.x, diffusecolor, damagecolor);
  vec3 spec_col     = speccolor.rgb;
  //float specdamage = clamp(1.0 - dot(damagecolor.xyz,vec3(1.0/3.0)) * damage.x * 2.0, 0.0, 1.0);
  //spec_col.rgb     *= specdamage;
  spec_col.rgb     *= (1.0-damage.x);
  //spec_col.a       *= bias(specdamage);
  float gloss      = shininessMap(gl_FrontMaterial.shininess,spec_col);
  
  fresnel_alpha = clamp( 0.0625 + ( 0.9375 * fresnel_alpha ), alpha, 1.0 );
  //fresnel_alpha = 1.0-fresnel_alpha;
  //fresnel_alpha *= fresnel_alpha; //to account for inner surface reflection
  //fresnel_alpha = 1.0-fresnel_alpha;

  // Do lighting for every active light
  if (light_enabled[0] != 0)
     lighting0(normal, vnormal, eye, reflection, diffusemap, spec_col, diffuse, specular);
  if (light_enabled[1] != 0)
     lighting1(normal, vnormal, eye, reflection, diffusemap, spec_col, diffuse, specular);

  vec4 result;
  //specular *= fresnel_alpha;
  vec3 final_specular_color = lerp( alpha, vec3( fresnel_alpha ), spec_col );

  result.a = fresnel_alpha;
  result.rgb  = lightingClose(diffuse, specular, diffusemap, final_specular_color)
              + fresnel_alpha*glowcolor.rgb
              + (envMapping(reflection,gloss,final_specular_color)*fresnel_alpha);
  result *= cloaking.rrrg;
  gl_FragColor = result;
}
