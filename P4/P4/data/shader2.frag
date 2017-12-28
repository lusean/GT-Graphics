#define PROCESSING_COLOR_SHADER

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

varying vec4 vertColor;
varying vec4 vertTexCoord;

void main() {
  // z(i+1) = z(i)^2 + c
  // z(0) = (0, 0)
  // z(1) = z(0)^2 + c
  // z(2) = z(1)^2 + c
  
  vec4 color = vec4(0.0, 0.7, 0.2, 1.0);
  float cx = vertTexCoord.x * 3.0 - 2.1;
  float cy = vertTexCoord.y * 3.0 - 1.5;
  
  // z(0)
  float zReal = 0.0;
  float zImag = 0.0;
  // 20 iterations
  for (int i = 0; i < 20; i++) {
	float newReal = (zReal * zReal) - (zImag * zImag);
	float newImag = 2.0 * zReal * zImag;
	zReal = newReal + cx;
	zImag = newImag + cy;
	float r = sqrt((zReal * zReal) + (zImag * zImag));
	// white color in radius 2, red color out
    if (r < 2.0) {
	  color = vec4(1.0, 1.0, 1.0, 1.0);
	} else {
	  color = vec4(0.0, 0.7, 0.2, 1.0);
	  break;
	}
  }
  gl_FragColor = vec4(color.rgb, 1.0);
}

