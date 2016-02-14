#version 120

uniform mat4 u_rotate;
uniform mat4 u_translate;
uniform mat4 u_scale;

void main()
{ 
	gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = gl_ModelViewProjectionMatrix * ((u_translate*u_rotate*u_scale)*gl_Vertex);
}