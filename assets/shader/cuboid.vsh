#version 120

uniform vec4 scale;
uniform vec4 translation;

void main()
{ 
    gl_Position = gl_ModelViewProjectionMatrix * (gl_Vertex*scale + translation);
}