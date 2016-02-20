#version 120

uniform mat4 u_rotate;
uniform mat4 u_translate;
uniform mat4 u_scale;
uniform vec4 u_rotationCenter;

void main()
{ 
	gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = gl_ModelViewProjectionMatrix * ((u_rotate*((u_translate*u_scale*gl_Vertex)-u_rotationCenter))+u_rotationCenter);
}