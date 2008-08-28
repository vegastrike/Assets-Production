uniform int light_enabled[gl_MaxLights];
uniform int max_light_enabled;
//samplers
uniform sampler2D envMap;
uniform sampler2D diffMap;   //1-bit alpha in alpha, for alpha-testing only
uniform sampler2D specMap;   //log256(shininess) in alpha
uniform sampler2D glowMap;   //ambient occlusion in alpha
uniform sampler2D normMap;   //U in .rgb; V in alpha (special encoding; see norm_decode())
uniform sampler2D damgMap;   //"dielectricness" in blue, specular blend in alpha
uniform sampler2D detailMap; //.rgb adds to diffuse, subtracts from spec; alpha mods shininess
uniform sampler2D prtMap;    //PRTP/N encoded into rgba in compressed form
//other uniforms
uniform vec4 ucloaking; //.rg=cloak
uniform vec4 udamage; //.x=damage
#define cloak_alpha ((ucloaking.rrrg))
#define get_damage ((udamage.x))
#define inv_damage ((1.0-get_damage))
//envColor won't be needed, since we're fetching it from the envmap

//NOTE: Since the term "binormal" has been rightly deprecated, I use "cotangent" instead :)

//general subroutines:

float lerp( in float f, in float a, in float b)
{
    return (1.0-f)*a + f*b;
}
vec3 lerp( in float f, in vec3 a, in vec3 b)
{
    return (1.0-f)*a + f*b;
}
/*
vec3 fastnormalize( in vec3 v ) //less accurate than normalize() but should use less instructions
{
    float tmp = dot( v, v );
    tmp = 1.5 - (0.5*tmp);
    return tmp * v;
}*/
float make_signed( in float zero_to_one_signed )
{
    return (zero_to_one_signed - 0.5) * 2.0;
}
vec3 imatmul( in vec3 tan, in vec3 cotan, in vec3 norm, in vec3 texnorm )
{
    return normalize( texnorm.xxx*tan + texnorm.yyy*cotan + texnorm.zzz*norm );
}

//decoding subroutines:

void detail_blend_decode( in float dmgblend, out float bump, out float tex )
{
    //float temp = make_signed(dmgblend);
    float temp = dmgblend - 0.5;
    bump = 0.07*clamp( temp, 0.0, 1.0 );
    tex = 0.5*clamp( -temp, 0.0, 1.0 );
    //bump *= bump;
    //tex *= tex;
}
float DBSRF( in float dielectric_blend_input, in float shininess_input )
{
    float temp1 = dielectric_blend_input * (1.0-dielectric_blend_input);
    float temp2 = shininess_input * (1.0-shininess_input);
    return temp1 / (temp1+temp2+0.0001);
}
/* The LaGrande normalmap noodle does away with the z-term for the normal by encoding U & V
as 0.5*tan( angle ), where angle is arcsin( U ) or arcsin( V ), respectively. To fit that
into a 0-1 range, we multiply by 0.5 once again, and add 0.5.
To reverse the encoding, we first subtract 0.5, then multiply by four, fill the z term with
1.0, and normalize. But multiplying by four is not needed if instead we fill the z term with
0.25, instead; *then* normalize :D
Here we've broken up the normalization, since there's no need to fully denormalize before
adding the normalmap, damage and detail normals. Just subtractin 0.5 is enough. And there's
also no point in normalizing before imatmul(); so normalization is done inside imatmul().
 */
vec2 dUdV_first_decode( vec2 raw_dudv )
{
    return raw_dudv - vec2( 127.0/256.0 );
}
vec3 dUdV_final_decode( vec2 blend_of_first_decode )
{
    vec3 temp;
    temp.rg = blend_of_first_decode;
    temp.b = 0.25;
    return temp; //might as well normalize after imatmul
}
float dielectricblend_decode( in float linear_input )
{
    //float temp1 = linear_input - 0.5;
    //float temp2 = temp1 * temp1;
    //return temp1/(1.8*temp2+0.55) + 0.5;
    return linear_input;
}
float dielectric_decode( in float linear_input )
{
    return (1.0625+linear_input) / (1.0625-linear_input);
    //New formula: 2*(1.125+x)/(1.125-x)-1
    //return 2.0*(1.125+linear_input)/(1.125-linear_input)-1.0;
}
float ambient_LOD( in float dielectric_k )
{
    float temp = 1.0 / dielectric_k;
    return 4.0 * (temp*temp - temp) + 8.0;
    //return 7.0;
}
float is_metal_decode( in float specdiffbalance )
{
    float tmp1 = 19.6444*(specdiffbalance-0.583333);
    float tmp2 = sqrt(1.0+tmp1*tmp1);
    return 0.5*tmp1/tmp2+0.5024772;
}
float nonzerok_decode( in float linear_k_input )
{
    float temp = linear_k_input * linear_k_input;
    temp *= ( temp * 20000.0 );
    return temp / (temp+1.0);
}
void distribute_gloss
(
  in float is_metal, in float is_dielectric, in float gloss_in,
  out vec2 linear_glosses
)
{
    // Shininess CTRL goes to metallic spec for metals; dielectric gloss for non-metals;
    // and the defaults are min for both; except when dielectric k is 0/trivial we want
    // to max-out shininess for fgloss, as it will be used for dual specularity metals
    // rather than for dielectric, Fresnel shininess.
    // This whole routine works with linear, 0-1 values (input representation) in & out,
    // rather than with actual shininess values. Outputs to a vec2 with both glosses
    linear_glosses.x = is_metal * gloss_in;
    linear_glosses.y = lerp( is_metal, gloss_in, sqrt(1.0-is_dielectric) );
}
vec2 lin_gloss_2_LOD( in vec2 lin_gloss )
{
    //The following is an approximation of the true formula. It avoids
    //using a logarithm, plus it makes better use of env-map mipmaps.
    //The true formula would be 8+log2( tan( spotlight radial angle ) )
    //The approximation is 15.2*(x^3+1.07)*(0.92-x) + 8.5*x - 6.0; but
    //we do it for 2 shininesses simultaneously, using vec2 in and out.
    vec2 temp1 = lin_gloss * lin_gloss * lin_gloss + vec2( 1.07 );
    vec2 temp2 = vec2( 0.92 ) - lin_gloss;
    return temp1 * temp2 * 15.2 + lin_gloss * 8.5 - vec2( 6.0 );
}
vec2 lin_gloss_2_exp( in vec2 lin_gloss )
{
    /* The formula used to compute shininess from alpha is just an ad-hoc formula
    that produces *useful* linearites across the alpha range; --with gradual change
    at the bottom of the curve, but rising fast at the top. Almost linear with the
    radius of specular light-spots, but not quite. Input and output are vec2, so
    that two shininesses (one for metallic, one for dielectric specularities) are
    computed in one shot. Using the formula (1.0625+x)/(1.0625-x) cubed. */
    vec2 temp1 = vec2( 1.0625 );
    vec2 temp2 = (temp1+lin_gloss) / (temp1-lin_gloss);
    temp1 = temp2 * temp2 * temp2;
    /*  tests:
     Alpha  Shininess Angular radius of specular highlights
      0/256     1.000 67.08
      1/256     1.022 66.35 1.10% angular decrement
     32/256     2.032 47.06
     33/256     2.078 46.53 1.14%
     64/256     4.215 32.67
     65/256     4.315 32.29 1.18%
     96/256     9.141 22.19
     97/256     9.375 21.91 1.28%
    128/256    21.433 14.49
    129/256    22.051 14.29 1.40%
    160/256    57.385  8.86
    161/256    59.360  8.71 1.72%
    192/256   195.112  4.80
    193/256   203.928  4.70 2.13%
    224/256  1103.370  2.02
    225/256  1182.430  1.95 3.59%
    254/256 24953.974  0.42
    255/256 29791.000  0.39 7.69% */
    /* limit to 1 degree radius (shininess of 4500) by product over sum; so
    that point source lights don't become single pixels on reflections */
    vec2 temp3 = vec2( 7777.0 );
    return temp1 * temp3 / (temp1+temp3);
}

vec2 EnvMapGen(vec3 f) {
    f = normalize(f);
    float fzp1=f.z+1.0;
    float m=2.0*sqrt(f.x*f.x+f.y*f.y+(fzp1)*(fzp1));
    return vec2(f.x/m+.5,f.y/m+.5);
}

vec3 envMappingLOD( in vec3 direction, in float LoD )
{
    vec4 result = texture2DLod( envMap, EnvMapGen(direction), LoD );
    return result.rgb * result.a * 2.0;
}

vec3 prt_pexpand( in vec3 sin )
{
    return clamp(2.0*(sin-vec3(0.5)),0.0,1.0);
}

vec3 prt_nexpand( in vec3 sin )
{
    return clamp(-2.0*(sin-vec3(0.5)),0.0,1.0);
}

vec3 prt_aexpand( in vec3 sin )
{
    return abs(2.0*(sin-vec3(0.5)));
}

/*void prt_decode( in vec4 PRTin, in float ao, out vec3 PRTPout, out vec3 PRTNout )
{
    vec3 first_decode_prtp = prt_pexpand( PRTin.rgb );
    vec3 first_decode_prtn = prt_nexpand( PRTin.rgb );
    vec3 PRTacc = prt_aexpand( PRTin.rgb );
    float PRTsum = dot(PRTacc, vec3(1.0));
    vec3 supplement = (vec3(0.5)-PRTacc) * (PRTin.a * 1.25 - PRTsum) * 0.333;
    vec3 p_suppl = (vec3(1.0)-first_decode_prtp)*supplement;
    vec3 n_suppl = (vec3(1.0)-first_decode_prtn)*supplement;
    PRTPout = first_decode_prtp+p_suppl;
    PRTNout = first_decode_prtn+n_suppl;
    float energy = dot(PRTPout+PRTNout, vec3(1.0));
    float energy_adjust = ao / (0.05+energy);
    PRTPout *= energy_adjust;
    PRTNout *= energy_adjust;
}*/

void prt_decode( in vec4 PRTin, in float eqd_ao,
  out vec3 diffPRTPout, out vec3 diffPRTNout, out vec3 specPRTPout, out vec3 specPRTNout )
{
    vec3 supplement, p_suppl, n_suppl;
    vec3 first_decode_prtp = prt_pexpand( PRTin.rgb );
    vec3 first_decode_prtn = prt_nexpand( PRTin.rgb );
    vec3 PRTacc =
      first_decode_prtp*first_decode_prtp + first_decode_prtn*first_decode_prtn;
    float PRTenergy = sqrt( PRTacc.r + PRTacc.g + PRTacc.b );
    //diffuse prt's
    supplement = (vec3(1.0)-PRTacc) * (PRTin.a - PRTenergy) * 0.333;
    p_suppl = (vec3(1.0)-first_decode_prtp)*supplement;
    n_suppl = (vec3(1.0)-first_decode_prtn)*supplement;
    diffPRTPout = first_decode_prtp+p_suppl;
    diffPRTNout = first_decode_prtn+n_suppl;
    //specular prt's
    supplement = (vec3(1.0)-PRTacc) * (eqd_ao - PRTenergy) * 0.333;
    p_suppl = (vec3(1.0)-first_decode_prtp)*supplement;
    n_suppl = (vec3(1.0)-first_decode_prtn)*supplement;
    specPRTPout = clamp( first_decode_prtp+p_suppl, 0.01, 0.99 );
    specPRTNout = clamp( first_decode_prtn+n_suppl, 0.01, 0.99 );
    //overdo it:
/*    specPRTPout = clamp( (3.0*specPRTPout)-(2.0*diffPRTPout), 0.01, 0.99 );
    specPRTNout = clamp( (3.0*specPRTNout)-(2.0*diffPRTNout), 0.01, 0.99 );*/
}

float prt_sample( in vec3 dir, in vec3 prtp, in vec3 prtn )
{
    dir = normalize(dir);
    vec3 p = clamp(dir, 0.0, 1.0);
    vec3 n = clamp(-dir, 0.0, 1.0);
    return dot(p,prtp) + dot(n,prtn);
}

float prt_diff_shadow( in vec3 dir, in vec3 prtp, in vec3 prtn, in float hardness, in float biasfactor )
{
    float ihardness = 1.0 + 4.0*hardness;
    hardness = 0.125 * hardness * biasfactor;
    return clamp( (prt_sample( dir, prtp, prtn ) - hardness) * ihardness, 0.0, 1.0 );
}
float prt_spec_shadow( in vec3 dir, in vec3 prtp, in vec3 prtn, in float hardness, in float biasfactor )
{
    float ihardness = 1.0 + 4.0*hardness;
    hardness = 0.125 * hardness * biasfactor;
    return clamp( (prt_sample( dir, prtp, prtn ) - hardness) * ihardness, 0.01, 0.99 );
}

float prt_ao( in vec3 prtp, in vec3 prtn )
{
    return dot(prtp + prtn, vec3(1.0));
}

vec3 prt_gi( in vec3 prtp, in vec3 prtn )
{
    const float LOD = 7.0;
    return envMappingLOD( gl_ModelViewMatrixTranspose[0].xyz, LOD) * prtp.x
         + envMappingLOD( gl_ModelViewMatrixTranspose[1].xyz, LOD) * prtp.y
         + envMappingLOD( gl_ModelViewMatrixTranspose[2].xyz, LOD) * prtp.z
         + envMappingLOD(-gl_ModelViewMatrixTranspose[0].xyz, LOD) * prtn.x
         + envMappingLOD(-gl_ModelViewMatrixTranspose[1].xyz, LOD) * prtn.y
         + envMappingLOD(-gl_ModelViewMatrixTranspose[2].xyz, LOD) * prtn.z;
}
/*vec3 prt_gi( in vec3 prtp, in vec3 prtn )
{
    float ao = prt_ao(prtp,prtn);
    float LOD = 8.0 * sqrt( ao );
    vec3 PRT = normalize(prtp-prtn);
    return ao * envMappingLOD( -PRT, LOD);
}*/

vec3 world_to_object( in vec3 world )
{
    return mat3(gl_ModelViewMatrixInverse[0].xyz,
                gl_ModelViewMatrixInverse[1].xyz,
                gl_ModelViewMatrixInverse[2].xyz) * world;
}
//Per-light called subroutines and macros:

float selfshadow_step( in float cosa )
{
    float temp1 = 77.7 * cosa;
    float temp2 = temp1 * temp1;
    return 0.5 * temp1 / sqrt( 1.0 + temp2 ) + 0.5;
}
void soft_penumbra_NdotL
(
  in vec3 normal, in vec3 vnormal, in vec3 light,
  out float selfshadow, out float NdotL, out float vNdotL
)
{
    vec2 result;
    float cosa = dot( vnormal, light );
    result.x = dot( normal, light );
    result.y = cosa;
    float ss = selfshadow_step( cosa );
    result += vec2( 0.02 );
    result *= ( 0.97 * ss );
    vNdotL = clamp( result.y, 0.0, 1.0 );
    selfshadow = ss;
    NdotL = clamp( result.x, 0.0, 2.0*(vNdotL) );
}
float fresnel( in float cosa, in float k )
{
   float tmp1 = sqrt(1.0-(1.0-cosa*cosa)/(k*k));
   float tmp2 = k*cosa;
   float tmp3 = k*tmp1;
   float tmp4 = (tmp1-tmp2)/(tmp1+tmp2+0.0001);
   tmp1 = (cosa-tmp3)/(cosa+tmp3+0.0001);
   return 0.5*(tmp1*tmp1+tmp4*tmp4);
}
void perlite
(
  in vec3 light, in vec3 normal, in vec3 vnormal, in vec3 reflection,
  in vec3 lightDiffuse, in float lightAtt,
  in float fresnel_blend, in float k, in vec2 ltd_glosses,
  inout vec3 DLacc, inout vec3 MSacc, inout vec3 FSacc,
  in vec3 diffprtp, in vec3 diffprtn
)
{
	float selfshadow, NdotL, vNdotL;
	soft_penumbra_NdotL( normal, vnormal, light, selfshadow, NdotL, vNdotL );
	//cos of reflection to light angle
	float RdotL = clamp( dot( reflection, light), 0.0, 4.0*vNdotL );
    //  precalculate some factors used more than once
    vec3 incident_light = lightDiffuse.rgb * lightAtt * selfshadow * prt_diff_shadow(world_to_object(light), diffprtp, diffprtn, 1.0, 1.0);
    float fresnel_refl = fresnel_blend * fresnel( NdotL, k );
//    vec3 reflected_light = incident_light * fresnel_refl;
    vec3 refracted_light = incident_light * (1.0-fresnel_refl);
    float ltd_Mgloss = ltd_glosses.x;
    float ltd_Fgloss = ltd_glosses.y;
    //  * DL - diffuse light: Needs to be multiplied by
    //  (1-fresnel_blend*fresnel reflection), from light vector
    DLacc += ( NdotL * refracted_light );
    //  * MS - metallic specularity: Modulated by
    //  (1-fresnel_blend*fresnel reflection), also, and
    //  metallic shininess phong. And we also multiply by the
    //  shininess, as smaller spots get more light concentration
    MSacc += ( pow( NdotL, ltd_Mgloss ) * sqrt(ltd_Mgloss) * refracted_light ); 
    //  * FS - fresnel specularity: Doesn't need fresnel, really,
    //  as the only fresnel applicable is view-vector-dependent,
    //  which can be applied afterwards, to the accumulated value;
    //  so, we'll multiply the accumulator by view fresnel after...
    FSacc += ( pow( NdotL, ltd_Fgloss ) * sqrt(ltd_Fgloss) ); //*reflected_light);
}
#define lighting(name, lightno_gl, lightno_tex) \
void name( \
   in vec3 normal, in vec3 vnormal, in  vec3 reflection, \
   in float k_blend, in float k_const, in vec2 limited_glosses, \
   inout vec3 DL_acc, inout vec3 MS_acc, inout vec3 FS_acc, \
   in vec3 prtp, in vec3 prtn \
) \
{ \
    perlite( normalize(gl_TexCoord[lightno_tex].xyz), \
      normal, vnormal, reflection, \
      gl_FrontLightProduct[lightno_gl].diffuse.rgb, \
      gl_TexCoord[lightno_tex].w, \
      k_blend, k_const, limited_glosses, \
      DL_acc, MS_acc, FS_acc, \
      prtp, prtn); \
}
lighting(lite0, 0, 5)
lighting(lite1, 1, 6)

//final blend subroutines:

vec3 multibounce_color( in vec3 color, in float refl_factor, in float blend )
{
    /* After light's penetrated the outer dielectric & is about to hit the inner, opaque
    layer below, instead of *= color, use this to account for multiple inner bouncings
    The formula is: *= (c-refL*c)/(1-refL*c), where refL is the fresnel reflectivity and
    c is the color of the material under the dielectric coating. But blended materials,
    such as plastics, are only partially covered by a specular dielectric layer, so we do
    have to allow some pure color reflectivity; thus the "blend" thing... */
    vec3 temp = color * refl_factor;
    return lerp( blend, (color-temp)/(vec3(1.0)-temp), color );
}
vec3 final_blend
(
 in vec3 DLacc, in vec3 MSacc, in vec3 FSacc, //DL=DiffuseLight; MS=MetallicSpec; FS=FresnelSpec
 in vec3 AMBenv, in vec3 MSenv, in vec3 FSenv, //Environment mapped counterparts
 in vec3 view_vec, in vec3 norm_vec, in vec3 refl_vec, in vec3 glow,
 in vec3 diff_color, in vec3 spec_color,
 in float dielectric_blend, in float dielectric_k, /*in float AO,*/
 in float spec_LoD,
 /*in vec3 prtp, in vec3 prtn,*/ in float specAOfactor, in vec3 prt_ambient, in float ao
)
{
/*    float NdotV = clamp( dot( norm_vec, view_vec ), 0.0, 1.0 );
    float AO_fresnel_reflection = (1.0-dielectric_k)/(1.0+dielectric_k );
    AO_fresnel_reflection *= AO_fresnel_reflection;
    float reflections = fresnel( NdotV, dielectric_k );
    //return vec3( reflections );
    float diffAOfactor = sqrt(AO);
    float MspecAOfactor = AO * AO;
    float FspecAOfactor = AO * diffAOfactor;
    //Begin with the accumulated direct light (diffuse lighting)
    vec3 final_acc = (DLacc*diffAOfactor);
    //Add ambient light minus fresnel-reflected (note that amb reflections IS the envmapping)
//    final_acc += ( AMBenv * AO * (1.0-AO_fresnel_reflection) );
    //multiply by the diffuse color
    final_acc *= multibounce_color( diff_color, reflections, dielectric_blend );
    //MSenv is multiplied by 1-fresnel to account for partial reflection on entering dielectric
    final_acc += (  ( MSacc + (MSenv*(1.0-reflections)) ) *
         multibounce_color( spec_color, reflections, dielectric_blend ) * MspecAOfactor  );
    //Both diffuse and metallic spec have to exit the dielectric. So, we'd multiply by the
    //refraction, here. However, multibounce_color() already took care of it, so, nought to do.
    //We just add fresnel specularity and... By the way, NOW we will multiply by fresnel
    //reflectivity from view angle --remember we didn't in perlite():
    final_acc += ( (FSacc+FSenv) * dielectric_blend * reflections * FspecAOfactor );
    return final_acc + glow; */
    
    float NdotV = clamp( dot( norm_vec, view_vec ), 0.0, 1.0 );
    float AO_fresnel_reflection = (1.0-dielectric_k)/(1.0+dielectric_k );
    AO_fresnel_reflection *= (AO_fresnel_reflection*dielectric_blend);
    float reflections = fresnel( NdotV, dielectric_k );
//    float specAOfactor = prt_shadow(world_to_object(refl_vec), prtp, prtn, 1.0/* - clamp(spec_LoD / 8.0, 0.0, 1.0)*/, 2.0);
    float MspecAOfactor = lerp(specAOfactor, ao*sqrt(ao), 1.0);
    float FspecAOfactor = MspecAOfactor;
    
    //Begin with the accumulated direct light (diffuse lighting)
    vec3 final_acc = DLacc;
    //Add ambient light minus fresnel-reflected (note that amb reflections IS the envmapping)
    final_acc += ( prt_ambient * (1.0-AO_fresnel_reflection) );
    //multiply by the diffuse color (filetered by fresnel multiple bounces, if any)
    final_acc *= multibounce_color( diff_color, reflections, dielectric_blend );
    //MSenv is multiplied by 1-fresnel to account for partial reflection on entering dielectric
    final_acc += (  ( MSacc + (MSenv*(1.0-reflections)) ) *
         multibounce_color( spec_color, reflections, dielectric_blend ) * MspecAOfactor  );
    //Both diffuse and metallic spec have to exit the dielectric. So, we'd multiply by the
    //refraction, here. However, multibounce_color() already took care of it, so, nought to do.
    //We just add fresnel specularity and... By the way, NOW we will multiply by fresnel
    //reflectivity from view angle --remember we didn't in perlite():
    final_acc += ( (FSacc+FSenv) * dielectric_blend * reflections * FspecAOfactor );
    return final_acc + glow;
}

//main:

void main()
{
    //READ INTPUT DATA:
    //get interpolated, per-vertex data
    vec2 texcoords2 = gl_TexCoord[0].xy;
    vec3 vnormal_v3 = normalize( gl_TexCoord[1].xyz );
    vec3 tangent_v3 = gl_TexCoord[2].xyz;
    vec3 cotangent_v3 = gl_TexCoord[3].xyz;
    vec3 eye_v3 = normalize(gl_TexCoord[4].xyz);
    //get texture data needed for detail and normal computations first
    vec4 DMG_in4 = texture2D( damgMap,texcoords2 );
    vec4 DET_in4 = texture2D( detailMap,32.0*texcoords2 );
    vec4 NOR_in4 = texture2D( normMap,texcoords2 );
    //then the rest
    vec4 SPC_in4 = texture2D( specMap,texcoords2 );
    vec4 COL_in4 = texture2D( diffMap,texcoords2 );
    vec4 GLO_in4 = texture2D( glowMap,texcoords2 );
    vec4 PRT_in4 = texture2D( prtMap,texcoords2 );
    
    //UNPACK:
    //we use a macro table to ease possible future changes to the texture packing:
    #define _matcolor_in_ ((COL_in4.rgb))
    #define _matalpha_in_ ((COL_in4.a))
    #define _damage_dUdV_ ((DMG_in4.rb))
    #define _detailblend_ ((DMG_in4.g))
    #define _damageAOdrk_ ((DMG_in4.a))
    #define _specdiffbal_ ((SPC_in4.r))
    #define _dielblendin_ ((SPC_in4.g))
    #define _dielectrkin_ ((SPC_in4.b))
    #define _shininessin_ ((SPC_in4.a))
    #define _glowcolorin_ ((GLO_in4.rgb))
    #define _ambientoccl_ ((GLO_in4.a))
    #define _normalmapin_ ((vec2(0.3333*(NOR_in4.r+NOR_in4.g+NOR_in4.b),NOR_in4.a)))
    #define _detail_dUdV_ ((DET_in4.rb))
    #define _detail_wild_ ((DET_in4.g))
    #define _detailgloss_ ((DET_in4.a))
    #define _prtpncompin_ ((PRT_in4.rgba))
    /* The most urgent item to unpack is the detail texture data because at its minimum
    level, detail provides dithering to hide DXT quantization; but such dithering needs
    to be applied before non-linear transformations. Keep in mind that all four rgba
    channels of the detail texture will be scaled to use the full 0-1 range. Minimum
    detail application to a channel will be where full range matches 1 channel step. */
    ///////////////////////////////////////////////////////////////////////////
    //CORE SHADER A.I. --MATERIAL FAMILY DETECTION:
    //characterize the material to determine how to interpret shininess, detail, etc.:
    float ismetal_ch1 = is_metal_decode( _specdiffbal_ );
    //"nonzerok" is short for "has dielectric k greater than 1.2 or so"
    float nonzerok_ch1 = nonzerok_decode( _dielectrkin_ );
    //dielectric blend to shininess relevance factor:
    float relevance_factor = DBSRF( _dielblendin_, _shininessin_ );
    ///////////////////////////////////////////////////////////////////////////
    //Manage distribution of detail texture application:
    float bump_det_fac1, nonbump_det_fac1;
    // decide: bumpy detail or textury detail?
    detail_blend_decode( _detailblend_, bump_det_fac1, nonbump_det_fac1 );
    // metallic vs non-metallic textury detail deciding fate of detail.green:
    float dielectricblend_detail = ismetal_ch1 * nonbump_det_fac1;
    float diffuse_detail = nonbump_det_fac1 - dielectricblend_detail;
    // metallic shininess detail mostly deciding fate of detail.alpha:
    float adjusted_gloss = nonbump_det_fac1 * make_signed(_detailgloss_);
    float gloss_detail = ismetal_ch1 * adjusted_gloss;
    // for non-metals, dilectric balance vs shininess relevance spells fate of detail.alpha:
    dielectricblend_detail += ( (adjusted_gloss - gloss_detail) * relevance_factor );
    //Apply details and damage:
    float damage = get_damage;
    float integrity = inv_damage;
    // to normal:
    vec2 dUdV_in2 = dUdV_first_decode(_normalmapin_);
    dUdV_in2 += ( dUdV_first_decode(_damage_dUdV_) * damage );
    dUdV_in2 += ( dUdV_first_decode(_detail_dUdV_) * bump_det_fac1 );
    // to diff/spec balance and glow:
    float diffuse_jitter = diffuse_detail * make_signed(_detail_wild_);
    float specdiffbal_in1 = _specdiffbal_ + diffuse_jitter;
    vec3 glow_in3 = _glowcolorin_*0.5 + vec3( diffuse_jitter );
    // to shininess:
    float s_gloss_det = make_signed(_detailgloss_);
    float shininess_in = _shininessin_ + gloss_detail*s_gloss_det;
    // to dielectric blend:
    float dielectricblend_in1 = _dielblendin_ + dielectricblend_detail*s_gloss_det;
    // to ambient occlusion:
    float AO_darkener1 = lerp( get_damage, 1.0, _damageAOdrk_ );
    float ao_mat1 = _ambientoccl_ * AO_darkener1;
    //Non-linear transformations, rangings, and any unpacking left:
    // diffuse, alpha and specular:
    vec3 spec_mat3 = _matcolor_in_ * _specdiffbal_;
    vec3 diff_mat3 = _matcolor_in_ - spec_mat3;
    vec3 glow_mat3 = glow_in3 * glow_in3 * inv_damage; //de-gamma & damage fade
    // PRT
    vec3 diff_prtp, diff_prtn, spec_prtp, spec_prtn;
    prt_decode( _prtpncompin_, _ambientoccl_, diff_prtp, diff_prtn, spec_prtp, spec_prtn );
    // compute final normal
    vec3 tmp3 = dUdV_final_decode( dUdV_in2 );
    vec3 normal_v3 = imatmul( tangent_v3, cotangent_v3, vnormal_v3, tmp3 );
    // computed vectors
    vec3 reflection_v3 = -reflect(eye_v3,normal_v3);
    // we'll modulate shininess by prt shadow of reflection vector; reason being we don't want
    // specular self-occlusion to darken too much (what it reflects instead of the envmap is not
    // guaranteed to be black; but fading to some arbitrary shade of grey won't wor; I tried it...
    float specAOfactor = prt_spec_shadow(world_to_object(reflection_v3), spec_prtp, spec_prtn, 1.0, 2.0);
    shininess_in *= sqrt(specAOfactor);
    // shininess CTRL goes to metallic spec for metals; dielectric gloss for non-metals;
    // and the defaults are min for both; except when dielectric k is 0/trivial we want to
    // max out shininess for fgloss, as it will be used for dual specularity metals
    vec2 lin_gloss2, gloss_lod2, glosses2;

    distribute_gloss( ismetal_ch1, nonzerok_ch1, shininess_in, lin_gloss2 );
    gloss_lod2 = lin_gloss_2_LOD( lin_gloss2 );
    glosses2 = lin_gloss_2_exp( lin_gloss2 );
    //
    // dielectric stuff:
    float dielec_blend_mat1 = dielectricblend_decode( dielectricblend_in1 );
    float dielectric_k_mat1 = dielectric_decode( _dielectrkin_ );
    // LOD for ambient lighting:
    float ambient_lod1 = ambient_LOD( dielectric_k_mat1 );
    //texture fetches (dependent on normal)
    vec3 ambenv_il3 = envMappingLOD( normal_v3, ambient_lod1 ); //ambient env mapping
    vec3 MSenv_il3 = envMappingLOD( reflection_v3, gloss_lod2.x ); //metallic spec env mapping
    vec3 FSenv_il3 = envMappingLOD( reflection_v3, gloss_lod2.y ); //fresnel spec env mapping
    //END OF UNPACKING
    ///////////////////////////////////////////////////////////////////////////
    //PER-LIGHT COMPUTATIONS
    // initialize accumulators
    vec3 DL_acc3, MS_acc3, FS_acc3;
    DL_acc3 = MS_acc3 = FS_acc3 = vec3( 0.0 );
    // then loop:
    if( light_enabled[0] != 0 )
      lite0
      (
        normal_v3,vnormal_v3,reflection_v3,
        dielec_blend_mat1,dielectric_k_mat1,glosses2,
        DL_acc3,MS_acc3,FS_acc3,
        spec_prtp, spec_prtn
      );
    if( light_enabled[1] != 0 )
      lite1
      (
        normal_v3,vnormal_v3,reflection_v3,
        dielec_blend_mat1,dielectric_k_mat1,glosses2,
        DL_acc3,MS_acc3,FS_acc3,
        spec_prtp, spec_prtn
      );
    //FINAL BLEND
    //////vec3 reflection_v3 = -reflect(eye_v3,vnormal_v3);
    vec3 prt_ambient = prt_gi(diff_prtp, diff_prtn);
    vec4 result4;
    result4.rgb = final_blend
    (
      DL_acc3, MS_acc3, FS_acc3, ambenv_il3, MSenv_il3, FSenv_il3,
      eye_v3, vnormal_v3, reflection_v3, glow_mat3, diff_mat3, spec_mat3,
      dielec_blend_mat1, dielectric_k_mat1, /*prt_ao(prtp,prtn),*/ gloss_lod2.x,
      /*diff_prtp, diff_prtn,*/ specAOfactor, prt_ambient, _ambientoccl_
    );
    result4.a = _matalpha_in_;
    //ALPHA and CLOAK
    result4.rgb *= _matalpha_in_; //mul by 1-bit alpha interpolated
    result4 *= cloak_alpha;
    //WRITE
    gl_FragColor = result4;
}
