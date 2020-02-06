#include "config.h"
#include "stdlib.h"
#include "normalmap.h"

uniform int light_enabled[gl_MaxLights];
uniform int max_light_enabled;
uniform sampler2D diffuseMap;
uniform samplerCube envMap;
uniform sampler2D specMap;
uniform sampler2D glowMap;
uniform sampler2D normalMap;
uniform sampler2D detail0Map;
uniform sampler2D detail1Map;
uniform vec4 cloaking;
uniform vec4 envColor;
uniform vec4 pass_num;


//UTILS
vec3 matmul(vec3 tangent, vec3 binormal, vec3 normal,vec3 lightVec) {
  return vec3(dot(lightVec,tangent),dot(lightVec,binormal),dot(lightVec,normal));
}
vec3 imatmul(vec3 tangent, vec3 binormal, vec3 normal,vec3 lightVec) {
  return normalize(lightVec.xxx*tangent+lightVec.yyy*binormal+lightVec.zzz*normal);
}



//public:
vec3 GLOSS_env_reflection( in float shininess, in vec3 direction ) //const
{
  //ENV MAP FETCH:
  return degamma_env(textureCube( envMap, direction, 8.0 - shininess/8.0 ).rgb);
}

float GLOSS_phong_reflection( in float shininess, in float RdotL, in float light_solid_angle ) //const
{
  //Below, multiplying by 3.621 would be correct; but the brightness is ridiculous in practice...
  //Well, no; correct only if we assume a chalk sphere and a chrome sphere throw the same total
  //ammount of light into your eye...
  return max( 0.0, pow( RdotL, shininess ) * sqrt(shininess) );
}


float diffuse_soft_dot(in vec3 normal, in vec3 light, in float light_sa)
{
    float NdotL = dot(normal, light);
    float normalized_sa = light_sa / TWO_PI;
    return (NdotL + normalized_sa) / (1.0 + normalized_sa);
}

//PER-LIGHT STUFF
void lightingLight(
   in vec4 lightinfo, in vec3 normal, in vec3 vnormal, in vec3 reflection, 
   in vec4 raw_light_col,
   in float shininess, in float nD,
   inout vec3 light_acc, inout vec3 specular_acc)
{
   vec3  light_pos = normalize(lightinfo.xyz);
   float light_sa = lightinfo.w;

   vec3 light_col = degamma_light(raw_light_col.rgb);

   float VNdotLx4= saturatef( 4.0 * diffuse_soft_dot(vnormal,light_pos,light_sa) );
   float RdotL = clamp( dot(reflection,light_pos), 0.0, VNdotLx4 );
   light_acc += light_col;
   specular_acc += ( GLOSS_phong_reflection(shininess,RdotL,light_sa) * light_col );
}
#define lighting(name, lightno_gl, lightno_tex) \
void name( \
   in vec3 normal, in vec3 vnormal, in  vec3 reflection, \
   in float shininess, in float nD, \
   inout vec3 light_acc, inout vec3 specular_acc) \
{ \
   lightingLight( \
      gl_TexCoord[lightno_tex], normal, vnormal, reflection, \
      gl_LightSource[lightno_gl].diffuse, \
      shininess, nD, \
      light_acc, specular_acc); \
}
lighting(lighting0, 0, 5)



//FINALLY... MAIN()
void main() 
{
  // Retreive texture coordinates
  vec2 tex_coord = gl_TexCoord[0].xy;
  vec2 nm_tex_coord = NM_FREQ_SCALING * tex_coord;
  
  // Retrieve vectors
  vec3 iNormal=gl_TexCoord[1].xyz;
  vec3 iTangent=gl_TexCoord[2].xyz;
  vec3 iBinormal=gl_TexCoord[3].xyz;
  vec3 position = gl_TexCoord[7].xyz;
  vec3 face_normal = normalize( cross( dFdx(position), dFdy(position) ) );

  vec3 vnormal = normalize( iNormal );

  vec3 normal=imatmul(iTangent,iBinormal,iNormal,normalmap_decode(texture2D(normalMap,nm_tex_coord)));

  // Other vectors
  vec3 eye = gl_TexCoord[4].xyz;
  float is_perimeter = gl_TexCoord[4].w;
  
  //compute a periphery smoothing alpha
  float PSalpha = sqr(is_perimeter);
  
  // Sample textures
  vec4 diffcolor = degamma_tex (texture2D(diffuseMap, tex_coord));
  vec4 speccolor = degamma_spec(texture2D(specMap   , tex_coord));
  vec4 glowcolor = degamma_glow(texture2D(glowMap   , tex_coord));
  
//  vec3 diff_col, glow_col;
  float alpha, nD, UAO;

  const float GLASS_REFRACTIVE_CONSTANT = 1.48567;
  nD = GLASS_REFRACTIVE_CONSTANT;
  //grab alpha channels  
  alpha = diffcolor.a;
  UAO = glowcolor.a;

  vec3 reflection = -reflect( eye, normal );
  
  //DIELECTRIC REFLECTION
  float fresnel_refl = saturatef(fresnel( dot(eye, normal), nD ));
  float fresnel_refr = 1.0 - fresnel_refl;

  // Init lighting accumulators
  vec3 light_acc    = vec3(0.0);
  vec3 specular_acc = vec3(0.0);

  // Do lighting for every active light
  float shininess = sqr(speccolor.a) * 128.0;
  if (light_enabled[0] != 0)
     lighting0(normal, vnormal, reflection, shininess, nD, light_acc, specular_acc);
   
  //Gather all incoming light:
  //NOTE: "Incoming" is a misnomer, really; what it means is that of all incoming light, these are the
  //portions expected to reflect specularly and/or diffusely, as per angle and shininess; --but not yet
  //modulated as per fresnel reflectivity or material colors. So I put them in quotes in the comments.
  //"Incoming specular":
  vec3 incoming_specular_light = GLOSS_env_reflection(shininess,reflection);
  incoming_specular_light += specular_acc;
  
  //Gather the reflectivities:
  vec3 dielectric_specularity = vec3(1.0);
  vec3 total_specularity = dielectric_specularity; // + metallic_specularity;
 
  //Multiply and Add:
  //we multiply by pass_num so that in pass 0 there's no env mapping or specular lights; but in
  // pass 1 there are; so that the far side appears to reflect only the (presumably) darker interior
  vec3 final_reflected = UAO * UAO * pass_num.x * incoming_specular_light * total_specularity;
  
  //FINAL PIXEL WRITE:
  //Restore gamma, add alpha, and Commit:
  float final_alpha = fresnel_refl;

  //trim the corners around the outline
  final_alpha *= PSalpha;
  //final_reflected = vec3(0.0,1.5,0.0);
  gl_FragColor = vec4( regamma(final_reflected*final_alpha), final_alpha );// * cloaking.rrrg;
  //Finitto!
}


