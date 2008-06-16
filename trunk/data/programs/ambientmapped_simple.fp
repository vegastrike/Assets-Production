uniform sampler2D diffuseMap;
uniform sampler2D envMap;
uniform vec4 cloaking;
uniform vec4 damage;
uniform vec4 envColor;

vec3 ambientMapping(in vec3 normal)
{
   return texture2DLod(envMap, gl_TexCoord[1].zw, 8.0).rgb * 2.0;
}

void main() 
{
  // Sample textures
  vec4 diffusemap  = texture2D(diffuseMap, gl_TexCoord[0].xy);
  vec4 diffuse = gl_Color;
  diffuse.rgb += ambientMapping(gl_TexCoord[2].xyz);
  
  gl_FragColor = diffusemap * diffuse;
  gl_FragColor.rgb += gl_SecondaryColor.rgb;
  gl_FragColor *= cloaking.rrrg;
}
