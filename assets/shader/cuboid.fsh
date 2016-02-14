#version 120

uniform sampler2D u_texture;

void main()
{
    vec4 col = texture2D(u_texture, vec2(-gl_TexCoord[0].s, gl_TexCoord[0].t));
	gl_FragColor = col;
}