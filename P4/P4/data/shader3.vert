#define PROCESSING_TEXTURE_SHADER

uniform mat4 transform;
uniform mat4 texMatrix;

attribute vec4 position;
attribute vec4 color;
attribute vec3 normal;
attribute vec2 texCoord;

varying vec4 vertColor;
varying vec4 vertTexCoord;

uniform sampler2D texture;

void main() {
  vertColor = color;
  vertTexCoord = texMatrix * vec4(texCoord, 1.0, 1.0);
  
  vec4 diffuse_color = texture2D(texture, vertTexCoord.xy);
  float grey = (diffuse_color.r * 0.3 + diffuse_color.g * 0.6 + diffuse_color.b * 0.1);

  vec4 pos = position + vec4(grey * normal * 200.0, 0.0);
  //vec4 pos = position;
  gl_Position = transform * pos;
}
