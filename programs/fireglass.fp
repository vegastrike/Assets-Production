#include "fplod.h"

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
uniform sampler2D damageMap;
uniform sampler2D detail0Map;
uniform sampler2D detail1Map;
uniform vec4 cloaking;
uniform vec4 damage;
uniform vec4 envColor;
uniform vec4 pass_num;


//UTILS
vec3 matmul(vec3 tangent, vec3 binormal, vec3 normal,vec3 lightVec) {
  return vec3(dot(lightVec,tangent),dot(lightVec,binormal),dot(lightVec,normal));
}
vec3 imatmul(vec3 tangent, vec3 binormal, vec3 normal,vec3 lightVec) {
  return normalize(lightVec.xxx*tangent+lightVec.yyy*binormal+lightVec.zzz*normal);
}


//OUTLINE SMOOTHING (by lowering alpha at corners on the periphery)
float is_periphery( in vec3 view, in vec3 rawvnorm, in float is_perimeter )
{
  /*float temp1 = dot( view, rawvnorm );
  return clamp( 1.0-(temp1)*(1.0-is_perimeter), 0.0, 1.0 );*/
  return is_perimeter;
}
float is_near_vert( in vec3 rawvnorm )
{
  return clamp(length(rawvnorm),0.8,1.0);
}
float is_near_vert_on_periphery( in vec3 view, in vec3 rawvnorm, in float is_perimeter )
{
  /*float temp1 = dot( view, rawvnorm );
  float temp2 = 1.0 - temp1*temp1;
  temp1 = temp2 * is_perimeter;*/
  //float temp = (1.0-is_perimeter(view,rawvnorm)) * (1.0-is_near_vert(vnorm));
  //return 1.0 - temp * temp;
  return pow( is_periphery(view,rawvnorm,is_perimeter) * is_near_vert(rawvnorm), CORNER_TRIMMING_POW );
}
float outline_smoothing_alpha( in vec3 view, in vec3 rawvnorm, in float is_perimeter )
{
  float temp = 1.0 - is_near_vert_on_periphery( view, rawvnorm, is_perimeter );
  return temp * temp * temp;
}


//GLOSS class
void GLOSS_init( inout vec4 mat_gloss, in float gloss_in  )
{
  //decrease resolution at high end of input range; --LOD 0 to LOD 1 difference is hardly noticeable
  //except on glossy AND very flat surfaces; whereas at the low end the resolution is more critical
  //See the forum posts indicate at the top of this file for the math derivation
  mat_gloss.x = 0.5 * ( gloss_in + gloss_in*gloss_in ); //relinearized input
  mat_gloss.y  = max( 0.0, 7.288828847 * ( 1.0 - mat_gloss.x ) ); //mip bias
  mat_gloss.z = PI_OVER_3 * pow( 2.5, (mat_gloss.y-8.0) ); //blur radius angle
  mat_gloss.w = TWO_PI * ( 1.0 - cos(mat_gloss.z) ); //blur solid angle
}
//private:
float GLOSS_power( in float mat_gloss_sa, in float light_solid_angle ) //const
{
  // shininess = ( 0.5 * pi / SolidAngle ) - 0.810660172
  const float MAGIC_TERM = 0.810660172;
  return max(0, ( HALF_PI / (mat_gloss_sa + light_solid_angle + 0.0005) ) - MAGIC_TERM);
}
//public:
vec3 GLOSS_env_reflection( in vec4 mat_gloss, in vec3 direction ) //const
{
  //ENV MAP FETCH:
  vec3 result = textureCubeLod( envMap, direction, mat_gloss.y ).rgb;
  return degamma_env(result);
}
float GLOSS_phong_reflection( in float mat_gloss_sa, in float RdotL, in float light_solid_angle ) //const
{
  float shininess = GLOSS_power( mat_gloss_sa, light_solid_angle );
  //Below, multiplying by 3.621 would be correct; but the brightness is ridiculous in practice...
  //Well, no; correct only if we assume a chalk sphere and a chrome sphere throw the same total
  //ammount of light into your eye...
  return max( 0.0, pow( RdotL, shininess ) * 0.27 * shininess );
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
   in float mat_gloss_sa, in float nD,
   inout vec3 light_acc, inout vec3 specular_acc)
{
   vec3  light_pos = normalize(lightinfo.xyz);
   float light_sa = lightinfo.w;
   vec3  light_col = degamma_light(raw_light_col.rgb);
   float VNdotLx4= saturatef( 4.0 * diffuse_soft_dot(vnormal,light_pos,light_sa) );
   float RdotL = clamp( dot(reflection,light_pos), 0.0, VNdotLx4 );
   light_acc += light_col;
   specular_acc += ( GLOSS_phong_reflection(mat_gloss_sa,RdotL,light_sa) * light_col );
}
#define lighting(name, lightno_gl, lightno_tex) \
void name( \
   in vec3 normal, in vec3 vnormal, in  vec3 reflection, \
   in float mat_gloss_sa, in float nD, \
   inout vec3 light_acc, inout vec3 specular_acc) \
{ \
   lightingLight( \
      gl_TexCoord[lightno_tex], normal, vnormal, reflection, \
      gl_LightSource[lightno_gl].diffuse, \
      mat_gloss_sa, nD, \
      light_acc, specular_acc); \
}
lighting(lighting0, 0, 5)
lighting(lighting1, 1, 6)


//REFLECTION
/*
 GAR stands for Gloss-Adjusted Reflection. It addresses the problem that a reflection vector off
  a finite gloss material represents a blur cone. But at very shallow angles, near the periphery
  of objects, when the reflection vector approaches colinearity with the view vector, that cone
  would extend to areas of the sky behind the object!, which makes no sense. The reflection cone
  must span up to 1 blur radius less than 180 degrees from the view vector; and it must dim also
  as it approaches maximum reflection angle.
*/
void GAR( in vec3 eye, in vec3 normal, in float blur_radius, out vec3 GAreflection )
{
  vec3 adjnormal = normalize( normal + 0.5 * blur_radius * eye );
  GAreflection = normalize(-reflect(eye,adjnormal));
}


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

  //supplement the vnormal with face normal before normalizing
  float supplemental_fraction=(1.0-length(iNormal));
  vec3 vnormal = normalize( iNormal + supplemental_fraction*face_normal );

  vec3 normal=imatmul(iTangent,iBinormal,iNormal,normalmap_decode(texture2D(normalMap,nm_tex_coord)));

  // Other vectors
  vec3 eye = gl_TexCoord[4].xyz;
  float is_perimeter = gl_TexCoord[4].w;
  
  //compute a periphery smoothing alpha
  float PSalpha = outline_smoothing_alpha( eye, iNormal, is_perimeter );
  
  // Sample textures
  vec4 damagecolor = degamma_tex (texture2D(damageMap , tex_coord));
  vec4 diffcolor   = degamma_tex (texture2D(diffuseMap, tex_coord));
  vec4 speccolor   = degamma_spec(texture2D(specMap   , tex_coord));
  vec4 glowcolor   = degamma_glow(texture2D(glowMap   , tex_coord));
  
  //better apply damage lerps before de-gamma-ing
  //COMMENTED OUT because I don't think anyone would bother to create a damage texture
  //for transparent parts, and it would look like crap, anyways.
  //  diffcolor.rgb  = lerp(damage.x, diffcolor, damagecolor).rgb;
  //  speccolor  *= (1.0-damage.x);
  //  glowcolor.rgb  *= (1.0-damage.x);
  
  //materials
  vec4 mtl_gloss;
  float alpha, nD, UAO;

  const float GLASS_REFRACTIVE_CONSTANT = 1.48567;
  nD = GLASS_REFRACTIVE_CONSTANT;
  //grab alpha channels  
  alpha = diffcolor.a;
  UAO = glowcolor.a;
  GLOSS_init( mtl_gloss, speccolor.a );

  vec3 reflection;

  //GAR( eye, normal, mtl_gloss.z, reflection );
  reflection = -reflect( eye, normal );
  
  //DIELECTRIC REFLECTION
  float fresnel_refl = saturatef(full_fresnel( dot( reflection, normal), nD ));
  float fresnel_refr = 1.0 - fresnel_refl;

  // Init lighting accumulators
  vec3 light_acc    = vec3(0.0);
  vec3 specular_acc = vec3(0.0);

  // Do lighting for every active light
  float mtl_gloss_sa = mtl_gloss.w;
  if (light_enabled[0] != 0)
     lighting0(normal, vnormal, reflection, mtl_gloss_sa, nD, light_acc, specular_acc);
  if (light_enabled[1] != 0)
     lighting1(normal, vnormal, reflection, mtl_gloss_sa, nD, light_acc, specular_acc);

  //Light in a lot of systems is just too dark.
  //Until the universe generator gets fixed, this hack fixes that:
  float crank_factor = 2.0;
  specular_acc *= crank_factor;
  
  //Gather all incoming light:
  //NOTE: "Incoming" is a misnomer, really; what it means is that of all incoming light, these are the
  //portions expected to reflect specularly and/or diffusely, as per angle and shininess; --but not yet
  //modulated as per fresnel reflectivity or material colors. So I put them in quotes in the comments.
  //"Incoming specular":
  vec3 incoming_specular_light = GLOSS_env_reflection(mtl_gloss,reflection);

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


