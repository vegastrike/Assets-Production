uniform sampler2D diffuseMap;
uniform samplerCube envMap;
uniform vec4 cloaking;
uniform vec4 damage;
uniform vec4 envColor;

/*vec3 ambientMapping(in vec3 normal)
{
   return texture2DLod(envMap, gl_TexCoord[1].zw, 8.0).rgb * 2.0;
}*/
vec3 reflectMapping()
{
   return textureCube(envMap, gl_TexCoord[1].xyz).rgb;
}
vec3 ambientMapping()
{
   return textureCubeLod(envMap, gl_TexCoord[2].xyz, 8.0).rgb;
}

void main() 
{
  // Sample textures
  vec3 diffusemap  = texture2D(diffuseMap, gl_TexCoord[0].xy).rgb;
  float diffusemax = max( diffusemap.b, max( diffusemap.r, diffusemap.g ) );
  float speculrmax = max( 0.0, 0.9-diffusemax);
  float speculrlod = 7.7 * speculrmax;
  vec3 speculrmap = vec3( speculrmax*0.77 );
  vec4 diffusecol = gl_Color;
  diffusecol.rgb += ambientMapping();
  vec4 result.rgb = diffusemap * diffusecol;
  result.rgb += speculrmap * reflectMapping( speculrlod );
  result.rgb += gl_SecondaryColor.rgb;
  result.a = diffusemap.a;
  result *= cloaking.rrrg;
  gl_FragColor = result;
/*
  gl_FragColor = diffusemap * diffusecol;
  gl_FragColor.rgb += gl_SecondaryColor.rgb;
  gl_FragColor *= cloaking.rrrg;
*/
}
