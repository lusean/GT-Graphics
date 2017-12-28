#define PROCESSING_TEXTURE_SHADER

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

uniform sampler2D texture;

varying vec4 vertColor;
varying vec4 vertTexCoord;

void main() {
  vec4 diffuse_color = texture2D(texture, vertTexCoord.xy);
  
  // grayscale
  float midColor = 0.3 * diffuse_color.r + 0.6 * diffuse_color.g + 0.1 * diffuse_color.b;
  
  // laplacian filter
  vec2 leftPixel = vec2(vertTexCoord.x - 0.005, vertTexCoord.y);
  vec2 rightPixel = vec2(vertTexCoord.x + 0.005, vertTexCoord.y);
  vec2 topPixel = vec2(vertTexCoord.x, vertTexCoord.y + 0.005);
  vec2 botPixel = vec2(vertTexCoord.x, vertTexCoord.y - 0.005);
  
  vec4 left = texture2D(texture, leftPixel.xy);
  vec4 right = texture2D(texture, rightPixel.xy);
  vec4 top = texture2D(texture, topPixel.xy);
  vec4 bot = texture2D(texture, botPixel.xy);
  
  float leftColor = 0.3 * left.r + 0.6 * left.g + 0.1 * left.b;
  float rightColor = 0.3 * right.r + 0.6 * right.g + 0.1 * right.b;
  float topColor = 0.3 * top.r + 0.6 * top.g + 0.1 * top.b;
  float botColor = 0.3 * bot.r + 0.6 * bot.g + 0.1 * bot.b;
  
  // sum of surrounding minus 4 * center
  float laplacian = (leftColor + rightColor + topColor + botColor) - (4 * midColor);
  vec4 color = vec4(laplacian, laplacian, laplacian, 1.0);
  
  gl_FragColor = vec4(color.rgb * 10, 1.0);
  
  //gl_FragColor = vec4(diffuse_color.rgb, 1.0);
}

